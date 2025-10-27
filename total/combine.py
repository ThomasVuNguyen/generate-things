#!/usr/bin/env python3
"""
Combine all dataset JSON files into a single Synthetic-Objects.json
"""

import json
import os
import subprocess
import tempfile

# Mapping of category names to their JSON file keys
CATEGORY_TO_KEY = {
    "animals": "animal",
    "fruits": "fruit",
    "buildings": "building",
    "household_items": "household_item",
    "musical_instruments": "musical_instrument",
    "vehicles": "vehicle",
    "food": "food_item",
    "historical_artifacts": "historical_artifact",
    "mythical_creatures": "mythical_creature",
    "tech_electronics": "electronic_device",
    "tools": "tool",
    "pokemon": "pokemon",
    "furniture": "furniture",
    "plants": "plant",
    "mechanical_components": "mechanical_component",
    "toys": "toy",
    "sports_equipment": "sports_equipment",
    "office_supplies": "office_supply",
    "kitchen_appliances": "kitchen_appliance",
    "decorative_art": "decorative_art",
    "natural_objects": "natural_object",
    "basic_shapes": "basic_shape",
    "primitive_shapes": "primitive_shape",
    "shape_combinations": "shape_combination"
}

# Dataset file mapping
DATASET_FILES = {
    "animals": "animal_openscad_dataset.json",
    "fruits": "fruit_openscad_dataset.json",
    "buildings": "building_openscad_dataset.json",
    "household_items": "household_item_openscad_dataset.json",
    "musical_instruments": "musical_instrument_openscad_dataset.json",
    "vehicles": "vehicle_openscad_dataset.json",
    "food": "food_openscad_dataset.json",
    "historical_artifacts": "historical_artifact_openscad_dataset.json",
    "mythical_creatures": "mythical_creature_openscad_dataset.json",
    "tech_electronics": "electronic_device_openscad_dataset.json",
    "tools": "tool_openscad_dataset.json",
    "pokemon": "pokemon_openscad_dataset.json",
    "furniture": "furniture_openscad_dataset.json",
    "plants": "plant_openscad_dataset.json",
    "mechanical_components": "mechanical_component_openscad_dataset.json",
    "toys": "toy_openscad_dataset.json",
    "sports_equipment": "sports_equipment_openscad_dataset.json",
    "office_supplies": "office_supply_openscad_dataset.json",
    "kitchen_appliances": "kitchen_appliance_openscad_dataset.json",
    "decorative_art": "decorative_art_openscad_dataset.json",
    "natural_objects": "natural_object_openscad_dataset.json",
    "basic_shapes": "basic_shape_openscad_dataset.json",
    "primitive_shapes": "primitive_shape_openscad_dataset.json",
    "shape_combinations": "shape_combination_openscad_dataset.json"
}

def load_dataset(filepath):
    """Load a dataset JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def can_render_openscad(code, timeout=5):
    """Test if OpenSCAD code can be rendered successfully"""
    temp_scad = None
    temp_png = None
    try:
        # Create temporary .scad file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.scad', delete=False) as temp_file:
            temp_file.write(code)
            temp_scad = temp_file.name
        
        # Create temporary PNG output path
        with tempfile.NamedTemporaryFile(mode='w', suffix='.png', delete=False) as temp_file:
            temp_png = temp_file.name
        
        # Try to render using OpenSCAD with virtual display
        result = subprocess.run(
            ['xvfb-run', '-a', 'openscad', '--imgsize=100,100', 
             '-o', temp_png, temp_scad],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Check if render succeeded and file exists with content
        success = result.returncode == 0 and os.path.exists(temp_png) and os.path.getsize(temp_png) > 0
        
        # Clean up temp files
        if temp_scad and os.path.exists(temp_scad):
            os.unlink(temp_scad)
        if temp_png and os.path.exists(temp_png):
            os.unlink(temp_png)
        
        return success
    except Exception as e:
        # Clean up on error
        if temp_scad and os.path.exists(temp_scad):
            os.unlink(temp_scad)
        if temp_png and os.path.exists(temp_png):
            os.unlink(temp_png)
        return False

def extract_items(dataset_data, name_key, validate=False):
    """Extract items from dataset with specified name key, optionally validating renders"""
    items = []
    total = len(dataset_data)
    for i, entry in enumerate(dataset_data):
        if name_key in entry and "openscad_code" in entry:
            code = entry["openscad_code"]
            
            # Skip if validation enabled and code cannot be rendered
            if validate:
                if not can_render_openscad(code):
                    continue
            
            items.append({
                "name": entry[name_key],
                "code": code
            })
            
            # Print progress every 50 items
            if (i + 1) % 50 == 0:
                print(f"    Processed {i + 1}/{total} items ({len(items)} valid)")
    
    return items

def main():
    import sys
    
    # Validation is enabled by default, can be disabled with --no-validate
    validate = '--no-validate' not in sys.argv and '-n' not in sys.argv
    
    if validate:
        print("Validation ENABLED (default): Only including renderable OpenSCAD code...")
        print("Use --no-validate to skip validation")
    else:
        print("Validation DISABLED: Including all code")
    
    # Get the parent directory (workspace root)
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    combined_data = []
    total_items = 0
    valid_items = 0
    
    # Process each category
    for category, filename in DATASET_FILES.items():
        filepath = os.path.join(workspace_root, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found, skipping...")
            continue
        
        print(f"\nProcessing {category}...")
        
        # Load dataset
        try:
            dataset_data = load_dataset(filepath)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
        
        # Extract items (with optional validation)
        name_key = CATEGORY_TO_KEY[category]
        items = extract_items(dataset_data, name_key, validate=validate)
        
        # Add to combined data
        for item in items:
            combined_data.append({
                "name": item["name"],
                "category": category,
                "code": item["code"]
            })
        
        total_items += len(dataset_data)
        valid_items += len(items)
        print(f"  {len(items)}/{len(dataset_data)} items added from {category} ({valid_items}/{total_items} total valid)")
    
    # Save combined dataset
    output_path = os.path.join(workspace_root, "Synthetic-Objects.json")
    with open(output_path, 'w') as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Validation: {'ENABLED' if validate else 'DISABLED'}")
    print(f"Total items processed: {total_items}")
    print(f"Valid items included: {len(combined_data)}")
    if total_items > 0:
        success_rate = (len(combined_data) / total_items) * 100
        print(f"Success rate: {success_rate:.1f}%")
    print(f"Combined dataset saved to: {output_path}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

