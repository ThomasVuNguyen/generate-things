#!/bin/bash

# Script to render all OpenSCAD code from JSON datasets to images
# This script processes all *_openscad_dataset.json files in the parent directory

set -e

echo "Starting OpenSCAD rendering process..."

# Create directories for output
mkdir -p images
mkdir -p temp

# Find all JSON dataset files
JSON_FILES=$(find .. -maxdepth 1 -name "*_openscad_dataset.json" 2>/dev/null || true)

if [ -z "$JSON_FILES" ]; then
    echo "No JSON dataset files found!"
    exit 1
fi

echo "Found JSON files:"
echo "$JSON_FILES"
echo ""

# Process each JSON file
for json_file in $JSON_FILES; do
    echo "Processing: $json_file"
    
    # Get the base name for the dataset (e.g., "basic_shapes" from "basic_shape_openscad_dataset.json")
    dataset_name=$(basename "$json_file" "_openscad_dataset.json")
    echo "  Dataset: $dataset_name"
    
    # Create a subdirectory for this dataset
    mkdir -p "images/$dataset_name"
    
    # Use Python to parse JSON and render each entry
    python3 << PYTHON_SCRIPT
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

def render_openscad_to_png(code, output_path, timeout=10):
    """Render OpenSCAD code to PNG"""
    temp_scad = None
    try:
        # Create temporary .scad file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.scad', delete=False) as temp_file:
            temp_file.write(code)
            temp_scad = temp_file.name
        
        # Render to PNG using OpenSCAD with virtual display
        # Use smaller image size (800x800) for faster rendering
        result = subprocess.run(
            ['xvfb-run', '-a', 'openscad', '--imgsize=800,800', 
             '-o', output_path, temp_scad],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Clean up temp file
        if temp_scad and os.path.exists(temp_scad):
            os.unlink(temp_scad)
        
        return result.returncode == 0
    except Exception as e:
        if temp_scad and os.path.exists(temp_scad):
            os.unlink(temp_scad)
        return False

def process_json_file(json_path):
    """Process a JSON file and render all entries"""
    dataset_name = Path(json_path).stem.replace('_openscad_dataset', '')
    output_dir = Path('images') / dataset_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    print(f"    Found {len(data)} entries")
    
    for item in data:
        # Get the name/key (could be any field except 'openscad_code')
        name = None
        for key in item.keys():
            if key != 'openscad_code' and key != 'renders':
                name = item[key]
                break
        
        if name is None:
            continue
        
        # Check if rendering is disabled
        if item.get('renders') == False:
            skip_count += 1
            continue
        
        # Get OpenSCAD code
        code = item.get('openscad_code', '')
        if not code:
            continue
        
        # Sanitize filename
        safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_')).rstrip()
        output_path = output_dir / f"{safe_name}.png"
        
        # Render to PNG
        if render_openscad_to_png(code, str(output_path)):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"    Rendered: {success_count} | Failed: {fail_count} | Skipped: {skip_count}")
    return success_count, fail_count, skip_count

# Process the JSON file
process_json_file("$json_file")
PYTHON_SCRIPT

done

# Clean up temp directory
rm -rf temp

echo ""
echo "✓ Rendering complete!"
echo "✓ Images saved in: images/"
echo "✓ Run './run.sh' to view all rendered models in your browser"

