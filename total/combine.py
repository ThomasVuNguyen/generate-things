#!/usr/bin/env python3
"""
Combine all dataset JSON files into a single Synthetic-Objects.json
"""

import json
import os

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

def extract_items(dataset_data, name_key):
    """Extract items from dataset with specified name key"""
    items = []
    for entry in dataset_data:
        if name_key in entry and "openscad_code" in entry:
            items.append({
                "name": entry[name_key],
                "code": entry["openscad_code"]
            })
    return items

def main():
    # Get the parent directory (workspace root)
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    combined_data = []
    
    # Process each category
    for category, filename in DATASET_FILES.items():
        filepath = os.path.join(workspace_root, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found, skipping...")
            continue
        
        print(f"Processing {category}...")
        
        # Load dataset
        try:
            dataset_data = load_dataset(filepath)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
        
        # Extract items
        name_key = CATEGORY_TO_KEY[category]
        items = extract_items(dataset_data, name_key)
        
        # Add to combined data
        for item in items:
            combined_data.append({
                "name": item["name"],
                "category": category,
                "code": item["code"]
            })
        
        print(f"  Added {len(items)} items from {category}")
    
    # Save combined dataset
    output_path = os.path.join(workspace_root, "Synthetic-Objects.json")
    with open(output_path, 'w') as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"\nTotal items: {len(combined_data)}")
    print(f"Combined dataset saved to: {output_path}")

if __name__ == "__main__":
    main()

