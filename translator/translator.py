import os
import json
import logging
import time
import hashlib
from typing import Dict
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

translation_cache: Dict[str, str] = {}

def validate_api_key() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logging.error("GEMINI_API_KEY is not set. Please set the environment variable.")
        raise EnvironmentError("GEMINI_API_KEY not found.")

def build_prompt(c_code: str) -> str:
    """
    Builds a structured prompt for translating C code to Rust.
    The prompt instructs the API to skip duplicate definitions if already present.
    """
    prompt = f"""You are an expert programmer in both C and Rust. 
Your task is to translate the provided C code into a single, cohesive Rust module.
Please follow these guidelines:
  - Do not produce duplicate definitions. If a type or function appears multiple times, output it only once.
  - Produce only the Rust code with no extra commentary.
  - Combine all functions, structs, and other definitions into one self-contained file.

C Code:
{c_code}

Rust Code:"""
    return prompt

def extract_rust_code(response_text: str) -> str:
    """
    Cleans up the API response to extract Rust code.
    Removes code block markers and filters out unwanted comment lines.
    """
    rust_code = response_text.strip()
    if rust_code.startswith("```rust"):
        rust_code = rust_code[len("```rust"):].strip()
    elif rust_code.startswith("```"):
        rust_code = rust_code[len("```"):].strip()
    
    if rust_code.endswith("```"):
        rust_code = rust_code[:-len("```")].strip()
    
    cleaned_lines = [line for line in rust_code.split('\n') if line.strip() and not line.strip().startswith("//")]
    return '\n'.join(cleaned_lines)

def translate_to_rust(c_code: str, max_retries: int = 3, backoff_factor: float = 1.5) -> str:
    """
    Translates C code to Rust using the Gemini API with retries and caching.
    """
    validate_api_key()
    cache_key = hashlib.sha256(c_code.encode('utf-8')).hexdigest()
    if cache_key in translation_cache:
        logging.info("Translation cache hit.")
        return translation_cache[cache_key]
    
    prompt = build_prompt(c_code)
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')
    
    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempt {attempt}: Translating segment...")
            response = model.generate_content(prompt)
            rust_code = extract_rust_code(response.text)
            translation_cache[cache_key] = rust_code
            return rust_code
        except Exception as e:
            logging.error(f"Translation attempt {attempt} failed: {str(e)}")
            if attempt < max_retries:
                sleep_time = backoff_factor ** attempt
                logging.info(f"Retrying in {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
            else:
                logging.error("Max retries reached. Returning error message.")
                return f"// Translation failed: {str(e)}"

def read_metadata(metadata_file: str) -> list:
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    return metadata.get("segments", [])

def read_segment(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()

def process_segments(metadata_file: str) -> Dict[str, str]:
    segments = read_metadata(metadata_file)
    translated_segments: Dict[str, str] = {}

    for segment in segments:
        c_code = read_segment(segment["file"])
        rust_code = translate_to_rust(c_code)
        translated_segments[segment["segment_id"]] = rust_code

    return translated_segments

if __name__ == "__main__":
    metadata_file = "metadata.json"
    rust_segments = process_segments(metadata_file)
    for segment_id, rust_code in rust_segments.items():
        logging.info(f"Segment {segment_id} translation:\n{rust_code}\n")
