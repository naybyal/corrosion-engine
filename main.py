import os
import json
import logging
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from preprocessor.preprocess import preprocess_c_file
from preprocessor.segmentation import extract_symbols, build_dependency_graph, segment_code
from preprocessor.metadata import generate_metadata
from translator.translator import translate_to_rust, read_metadata, read_segment

# Configure logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def write_rust_file(segment_id: str, rust_code: str, metadata: dict, rust_output_dir: str, metadata_file: str) -> None:
    """
    Writes the translated Rust code for a segment to a file and updates metadata.json.
    """
    rust_file_name = f"{segment_id}.rs"
    rust_file_path = os.path.join(rust_output_dir, rust_file_name)
    
    os.makedirs(rust_output_dir, exist_ok=True)
    try:
        with open(rust_file_path, "w") as f:
            f.write(rust_code)
        logging.info(f"Written Rust code for segment '{segment_id}' to {rust_file_path}")
    except IOError as e:
        logging.error(f"Failed to write Rust file for segment '{segment_id}': {e}")
        return

    # Update metadata for the segment with the Rust file name
    for segment in metadata.get("segments", []):
        if segment.get("segment_id") == segment_id:
            segment["rust_file"] = rust_file_name
            break

    try:
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to update metadata file {metadata_file}: {e}")

def combine_rust_segments(metadata_file: str, rust_output_dir: str, final_output_file: str) -> None:
    """
    Combines all translated Rust segments into one final Rust output file.
    """
    logging.info("Combining Rust segments into one file...")
    try:
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
    except IOError as e:
        logging.error(f"Failed to read metadata file {metadata_file}: {e}")
        return

    combined_rust_code = ""
    for segment in metadata.get("segments", []):
        rust_file_name = segment.get("rust_file", "")
        rust_file_path = os.path.join(rust_output_dir, rust_file_name)
        if rust_file_name and os.path.exists(rust_file_path):
            try:
                with open(rust_file_path, "r") as f:
                    combined_rust_code += f.read() + "\n\n"
            except IOError as e:
                logging.error(f"Error reading {rust_file_path}: {e}")
        else:
            logging.warning(f"Rust file for segment '{segment.get('segment_id')}' not found at {rust_file_path}")

    os.makedirs(rust_output_dir, exist_ok=True)
    try:
        with open(final_output_file, "w") as f:
            f.write(combined_rust_code)
        logging.info(f"Combined Rust code written to {final_output_file}")
    except IOError as e:
        logging.error(f"Failed to write combined Rust file {final_output_file}: {e}")

def parallel_translate_segments(metadata_file: str, max_workers: int = 4) -> dict:
    """
    Translates each C segment to Rust in parallel.
    Returns a dictionary mapping segment IDs to their translated Rust code.
    """
    segments = read_metadata(metadata_file)
    translated_segments = {}

    # Use a ThreadPoolExecutor to translate segments concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_segment = {
            executor.submit(translate_to_rust, read_segment(segment["file"])): segment["segment_id"]
            for segment in segments
        }
        for future in as_completed(future_to_segment):
            segment_id = future_to_segment[future]
            try:
                rust_code = future.result()
                translated_segments[segment_id] = rust_code
                logging.info(f"Segment '{segment_id}' translated successfully.")
            except Exception as e:
                logging.error(f"Translation failed for segment '{segment_id}': {e}")
                translated_segments[segment_id] = f"// Error: {e}"
    return translated_segments

def main(input_file: str, output_dir: str, max_workers: int) -> None:
    start_time = time.time()
    logging.info("Starting C-to-Rust transpilation process...")

    # Define directories and file paths
    rust_output_dir = os.path.join(output_dir, "rust")
    final_rust_file = os.path.join(rust_output_dir, "output.rs")
    metadata_file = os.path.join(output_dir, "metadata.json")

    try:
        logging.info("Preprocessing C file...")
        preprocessed_file = preprocess_c_file(input_file, output_dir)
    except Exception as e:
        logging.error(f"Preprocessing failed: {e}")
        return

    try:
        logging.info("Extracting symbols...")
        symbols = extract_symbols(preprocessed_file)
    except Exception as e:
        logging.error(f"Symbol extraction failed: {e}")
        return

    try:
        logging.info("Building dependency graph...")
        dependency_graph = build_dependency_graph(symbols)
    except Exception as e:
        logging.error(f"Building dependency graph failed: {e}")
        return

    try:
        logging.info("Segmenting code...")
        segments = segment_code(preprocessed_file, symbols, output_dir)
    except Exception as e:
        logging.error(f"Segmentation failed: {e}")
        return

    try:
        logging.info("Generating metadata...")
        metadata_file = generate_metadata(symbols, segments, output_dir)
    except Exception as e:
        logging.error(f"Metadata generation failed: {e}")
        return

    logging.info("Preprocessing complete. Beginning translation...")

    try:
        # Translate segments concurrently using the provided max_workers
        rust_segments = parallel_translate_segments(metadata_file, max_workers=max_workers)
    except Exception as e:
        logging.error(f"Translation process failed: {e}")
        return

    try:
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
    except Exception as e:
        logging.error(f"Failed to read metadata file {metadata_file}: {e}")
        return

    # Write each translated segment to its respective Rust file
    for segment in metadata.get("segments", []):
        segment_id = segment.get("segment_id")
        rust_code = rust_segments.get(segment_id, "// Error: Rust translation missing")
        write_rust_file(segment_id, rust_code, metadata, rust_output_dir, metadata_file)

    # Combine all Rust segments into a single file
    combine_rust_segments(metadata_file, rust_output_dir, final_rust_file)
    
    end_time = time.time()
    logging.info(f"Transpilation completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="C-to-Rust GenAI-based Transpiler")
    parser.add_argument("input_file", help="Path to the input C file")
    parser.add_argument("--output_dir", default="output", help="Directory to store output files")
    parser.add_argument("--max_workers", type=int, default=4, help="Maximum number of parallel workers for translation")
    args = parser.parse_args()

    try:
        main(args.input_file, args.output_dir, args.max_workers)
    except Exception as e:
        logging.error(f"Transpilation process encountered a fatal error: {e}")
