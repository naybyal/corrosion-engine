import os
import logging
import json
from preprocessor.preprocess import preprocess_c_file
from preprocessor.segmentation import extract_symbols, build_dependency_graph, segment_code
from preprocessor.metadata import generate_metadata
from translator.translator import process_segments

OUTPUT_DIR = "output"
RUST_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "rust")
FINAL_RUST_FILE = os.path.join(RUST_OUTPUT_DIR, "output.rs")
METADATA_FILE = os.path.join(OUTPUT_DIR, "metadata.json")

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def write_rust_file(segment_id, rust_code, metadata):
    """Writes translated Rust code and updates metadata.json with Rust file path."""
    rust_file_name = f"{segment_id}.rs"  
    rust_file_path = os.path.join(RUST_OUTPUT_DIR, rust_file_name)

    os.makedirs(RUST_OUTPUT_DIR, exist_ok=True)
    with open(rust_file_path, "w") as f:
        f.write(rust_code)

    logging.info(f"Written Rust code for {segment_id} to {rust_file_path}")

    for segment in metadata["segments"]:
        if segment["segment_id"] == segment_id:
            segment["rust_file"] = rust_file_name
            break

    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

def combine_rust_segments(metadata_file, output_file):
    """Combines all Rust segments into one output.rs file based on metadata.json."""
    logging.info("Combining Rust segments into one file...")

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    combined_rust_code = ""

    for segment in metadata["segments"]:
        rust_file_name = segment.get("rust_file", "")
        rust_file_path = os.path.join(RUST_OUTPUT_DIR, rust_file_name)

        if rust_file_name and os.path.exists(rust_file_path):
            with open(rust_file_path, "r") as f:
                combined_rust_code += f.read() + "\n\n"
        else:
            logging.warning(f"Rust file for segment {segment['segment_id']} not found: {rust_file_path}")

    os.makedirs(RUST_OUTPUT_DIR, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(combined_rust_code)

    logging.info(f"Combined Rust code written to {output_file}")

def main(input_file):
    logging.info("Preprocessing C file...")
    preprocessed_file = preprocess_c_file(input_file)

    logging.info("Extracting symbols...")
    symbols = extract_symbols(preprocessed_file)

    logging.info("Building dependency graph...")
    dependency_graph = build_dependency_graph(symbols)

    logging.info("Segmenting code...")
    # segments = segment_code(preprocessed_file, symbols, dependency_graph)
    segments = segment_code(preprocessed_file, symbols)

    logging.info("Generating metadata...")
    metadata_file = generate_metadata(symbols, segments)

    logging.info(f"Preprocessing complete. Segments stored in {OUTPUT_DIR}")
    logging.info(f"Metadata file saved at {metadata_file}")

    rust_segments = process_segments(metadata_file)

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    for segment in metadata["segments"]:
        segment_id = segment["segment_id"]
        rust_code = rust_segments.get(segment_id, "// Error: Rust translation missing")
        write_rust_file(segment_id, rust_code, metadata)

    combine_rust_segments(metadata_file, FINAL_RUST_FILE)

if __name__ == "__main__":
    input_file = "main.c"
    main(input_file)
