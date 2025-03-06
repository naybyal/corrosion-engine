import os
import json
import logging
from typing import List, Dict, Any
import networkx as nx

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_metadata(
    symbols: List[Dict[str, Any]], 
    segment_files: Dict[str, str], 
    output_dir: str = "output"
) -> str:
    """
    Generates metadata linking segments with extracted symbols, ensuring dependency ordering.
    Duplicates are filtered so that each symbol appears only once.
    """
    os.makedirs(output_dir, exist_ok=True)
    metadata: Dict[str, Any] = {"segments": []}

    # Remove duplicate symbols (keyed by symbol name)
    unique_symbols = {symbol["name"]: symbol for symbol in symbols if "name" in symbol}
    
    # Build dependency graph for unique symbols
    graph = nx.DiGraph()
    for symbol in unique_symbols.values():
        symbol_name = symbol["name"]
        graph.add_node(symbol_name)
        for dependency in symbol.get("dependencies", []):
            # Only add dependency if the dependency is one of our unique symbols
            if dependency in unique_symbols:
                graph.add_edge(symbol_name, dependency)

    # Topological sorting to ensure dependency order
    try:
        sorted_symbols = list(nx.topological_sort(graph))
    except nx.NetworkXUnfeasible:
        cycles = list(nx.simple_cycles(graph))
        logging.warning(f"Dependency graph contains cycles: {cycles}. Using fallback ordering.")
        sorted_symbols = sorted(unique_symbols.keys())

    # Create metadata entries for each sorted symbol
    for symbol_name in sorted_symbols:
        if symbol_name in segment_files:
            segment_entry = {
                "segment_id": symbol_name,
                "file": segment_files[symbol_name],
                "rust_file": f"{symbol_name}.rs",
                "contained_symbols": [symbol_name],
                "dependencies": list(graph.successors(symbol_name))
            }
            metadata["segments"].append(segment_entry)
        else:
            logging.warning(f"Symbol '{symbol_name}' does not have a corresponding segment file.")

    metadata_file = os.path.join(output_dir, "metadata.json")
    try:
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)
        logging.info(f"Metadata successfully written to {metadata_file}")
    except IOError as e:
        logging.error(f"Failed to write metadata to {metadata_file}: {e}")
        raise

    return metadata_file
