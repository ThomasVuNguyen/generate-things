import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_vehicle_names_batch(prompt_template, count=200):
    """
    Generate a batch of vehicle names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of vehicles to generate in this batch
    
    Returns:
        list: List of vehicle names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        vehicles = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    vehicles.append(clean_name.lower())
        
        print(f"Generated {len(vehicles)} vehicles from this batch")
        return vehicles
        
    except Exception as e:
        print(f"Error generating vehicles in batch: {e}")
        return []


def generate_vehicle_names_multi_batch(target_count=1000):
    """
    Generate vehicle names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of vehicles to generate
    
    Returns:
        list: List of vehicle names
    """
    print(f"Generating {target_count} diverse vehicle names using multiple specialized prompts...")
    
    # Define different prompt templates for different vehicle categories
    prompts = [
        {
            "name": "Cars & Automobiles",
            "template": """Generate exactly {count} car and automobile names.

Requirements:
- Only single-word vehicle names (no spaces, hyphens, or compound words)
- Focus on types of cars and automobiles
- Include: sedan, coupe, hatchback, suv, truck, van, convertible, wagon, pickup, crossover
- NO brand names (like "Toyota", "BMW"), NO model names (like "Camry", "Mustang")
- NO duplicates, focus on vehicle types and categories

Return ONLY the vehicle names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Motorcycles & Bikes",
            "template": """Generate exactly {count} motorcycle and bicycle names.

Requirements:
- Only single-word vehicle names (no spaces, hyphens, or compound words)
- Focus on types of motorcycles and bicycles
- Include: motorcycle, scooter, moped, bicycle, bike, cruiser, sportbike, dirtbike, chopper, touring
- NO brand names, NO model names, NO duplicates
- Focus on vehicle types and categories

Return ONLY the vehicle names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Boats & Watercraft",
            "template": """Generate exactly {count} boat and watercraft names.

Requirements:
- Only single-word vehicle names (no spaces, hyphens, or compound words)
- Focus on types of boats and watercraft
- Include: boat, yacht, sailboat, speedboat, canoe, kayak, raft, dinghy, ferry, submarine
- NO brand names, NO model names, NO duplicates
- Focus on vehicle types and categories

Return ONLY the vehicle names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Aircraft & Aviation",
            "template": """Generate exactly {count} aircraft and aviation vehicle names.

Requirements:
- Only single-word vehicle names (no spaces, hyphens, or compound words)
- Focus on types of aircraft and aviation vehicles
- Include: airplane, helicopter, jet, glider, drone, balloon, airship, fighter, bomber, cargo
- NO brand names, NO model names, NO duplicates
- Focus on vehicle types and categories

Return ONLY the vehicle names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Trains & Rail Vehicles",
            "template": """Generate exactly {count} train and rail vehicle names.

Requirements:
- Only single-word vehicle names (no spaces, hyphens, or compound words)
- Focus on types of trains and rail vehicles
- Include: train, locomotive, subway, tram, trolley, monorail, bullet, freight, passenger, metro
- NO brand names, NO model names, NO duplicates
- Focus on vehicle types and categories

Return ONLY the vehicle names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Construction & Heavy Vehicles",
            "template": """Generate exactly {count} construction and heavy vehicle names.

Requirements:
- Only single-word vehicle names (no spaces, hyphens, or compound words)
- Focus on types of construction and heavy vehicles
- Include: bulldozer, excavator, crane, forklift, tractor, dump, loader, grader, roller, mixer
- NO brand names, NO model names, NO duplicates
- Focus on vehicle types and categories

Return ONLY the vehicle names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_vehicles = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        vehicles = generate_vehicle_names_batch(prompt_info['template'], batch_size)
        all_vehicles.extend(vehicles)
        print(f"Total vehicles so far: {len(all_vehicles)}")
    
    return all_vehicles


def filter_single_word_vehicles(vehicles):
    """
    Filter vehicles to ensure they are single words only.
    
    Args:
        vehicles (list): List of vehicle names
    
    Returns:
        list: Filtered list of single-word vehicles
    """
    filtered = []
    for vehicle in vehicles:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(vehicle.split()) == 1 and '-' not in vehicle and '_' not in vehicle:
            filtered.append(vehicle)
    
    return filtered


def save_vehicles_list(vehicles, filename="list.json"):
    """
    Save the vehicles list to a JSON file.
    
    Args:
        vehicles (list): List of vehicle names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(vehicles, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save vehicle names."""
    print("=== Enhanced Vehicle Name Generator ===")
    print("Generating 1000+ diverse single-word vehicle names using multiple specialized prompts...")
    print()
    
    # Generate vehicles using multiple specialized prompts
    vehicles = generate_vehicle_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word vehicles only...")
    filtered_vehicles = filter_single_word_vehicles(vehicles)
    
    print(f"After filtering: {len(filtered_vehicles)} single-word vehicles")
    
    # Remove duplicates while preserving order
    unique_vehicles = []
    seen = set()
    for vehicle in filtered_vehicles:
        if vehicle not in seen:
            unique_vehicles.append(vehicle)
            seen.add(vehicle)
    
    print(f"After removing duplicates: {len(unique_vehicles)} unique vehicles")
    
    # Take exactly 1000 (or as many as we have)
    final_vehicles = unique_vehicles[:1000]
    
    # Save to file
    filepath = save_vehicles_list(final_vehicles)
    
    print(f"\n✓ Generated {len(final_vehicles)} common single-word vehicle names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 vehicles:")
    for i, vehicle in enumerate(final_vehicles[:20], 1):
        print(f"  {i:2d}. {vehicle}")
    
    if len(final_vehicles) > 20:
        print(f"  ... and {len(final_vehicles) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(vehicles)}")
    print(f"  After filtering: {len(filtered_vehicles)}")
    print(f"  After deduplication: {len(unique_vehicles)}")
    print(f"  Final count: {len(final_vehicles)}")


if __name__ == "__main__":
    main()
