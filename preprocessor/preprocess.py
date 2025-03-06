import os
import re
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_user_defined_includes(file_path: str) -> list[str]:
    """Extracts user-defined includes, ignoring system headers."""
    include_pattern = re.compile(r'^\s*#include\s*"(.+?)"', re.MULTILINE)
    includes = []
    base_dir = os.path.dirname(os.path.abspath(file_path))

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except IOError as e:
        logging.error(f"Failed to read {file_path}: {e}")
        return includes

    for match in include_pattern.finditer(content):
        include_path = os.path.join(base_dir, match.group(1))
        if os.path.exists(include_path):
            includes.append(include_path)
        else:
            logging.warning(f"Include file not found: {include_path}")
    return includes

def merge_user_includes(file_path: str, cache: dict = None) -> str:
    """Recursively merges user-defined includes into the main file while avoiding all #include directives."""
    if cache is None:
        cache = {}
    processed = set()

    def merge(fp: str) -> str:
        if fp in processed:
            return ""  # Avoid circular includes
        if fp in cache:
            return cache[fp]

        processed.add(fp)
        try:
            with open(fp, "r") as f:
                content = f.readlines()
        except IOError as e:
            logging.error(f"Error reading {fp}: {e}")
            return ""

        merged_content = []
        user_include_pattern = re.compile(r'^\s*#include\s*"(.+?)"')
        system_include_pattern = re.compile(r'^\s*#include\s*<.+?>')

        for line in content:
            # Process user includes recursively
            user_match = user_include_pattern.match(line)
            if user_match:
                include_file = user_match.group(1)
                include_path = os.path.join(os.path.dirname(fp), include_file)
                if os.path.exists(include_path):
                    merged_content.append(merge(include_path))
                else:
                    logging.warning(f"User include not found: {include_path}")
                continue

            # Skip system includes
            if system_include_pattern.match(line):
                continue

            merged_content.append(line)

        merged_text = "".join(merged_content)
        cache[fp] = merged_text
        return merged_text

    return merge(file_path)

def preprocess_c_file(input_file: str, output_dir: str = "output", gcc_flags: list[str] = None) -> str:
    """
    Preprocesses the C file by merging user-defined includes, expanding macros, and removing all includes.
    Parameters:
      - input_file: Path to the C file.
      - output_dir: Directory to store output files.
      - gcc_flags: Additional flags for the GCC preprocessor.
    """
    os.makedirs(output_dir, exist_ok=True)
    merged_file_path = os.path.join(output_dir, f"merged_{os.path.basename(input_file)}")

    # Merge user-defined includes and remove #include directives
    merged_content = merge_user_includes(input_file)
    try:
        with open(merged_file_path, "w") as f:
            f.write(merged_content)
    except IOError as e:
        logging.error(f"Error writing merged file {merged_file_path}: {e}")
        raise

    # Set default GCC flags if not provided
    if gcc_flags is None:
        gcc_flags = [
            "-nostdinc",       # Prevent system includes
            "-ffreestanding",  # Disable standard library assumptions
            "-E",              # Preprocess only
            "-dD",             # Output macro definitions
            "-std=c99"
        ]
    
    preprocessed_file = os.path.join(output_dir, "preprocessed.c")
    cmd = ["gcc"] + gcc_flags + [merged_file_path, "-o", preprocessed_file]
    logging.info("Running GCC preprocessor: " + " ".join(cmd))

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode() if e.stderr else "Unknown error"
        logging.error(f"Preprocessing failed:\nCommand: {e.cmd}\nError: {error_message}")
        raise RuntimeError(f"Preprocessing failed:\nCommand: {e.cmd}\nError: {error_message}")

    return preprocessed_file
