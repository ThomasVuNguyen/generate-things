import json
import sys
import os

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def is_actual_building(name):
    """
    Use AI to determine if a name represents an actual building or architectural structure
    (not a vehicle, animal, or other non-building).

    Args:
        name (str): The name to check

    Returns:
        bool: True if it's an actual building, False otherwise
    """
    prompt = f"""Is "{name}" the name of an actual building or architectural structure?
Answer with just "yes" or "no".
Do NOT count:
- Vehicles (like "car", "boat", "plane", "train")
- Animals (like "cat", "dog", "bird", "fish")
- Food items (like "apple", "bread", "milk")
- Tools (like "hammer", "saw", "drill")
- People or body parts
- Abstract concepts (like "space", "time", "design")
- Natural features (like "mountain", "river", "tree")

DO count:
- Residential buildings (like "house", "mansion", "apartment")
- Commercial buildings (like "office", "store", "hotel")
- Public buildings (like "school", "hospital", "library")
- Religious buildings (like "church", "temple", "mosque")
- Historical buildings (like "castle", "palace", "cathedral")
- Modern buildings (like "skyscraper", "tower", "arena")
- Infrastructure (like "bridge", "tunnel", "lighthouse")

Answer:"""

    try:
        response = chat_with_kimi(prompt, stream=False)
        answer = response.strip().lower()
        return "yes" in answer
    except Exception as e:
        print(f"Error checking '{name}': {e}")
        return False


def filter_buildings_list(input_file, output_file=None):
    """
    Filter the buildings list to only include actual buildings.

    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to save filtered results (optional)

    Returns:
        list: List of actual buildings
    """
    # Load the list (using utf-8-sig to handle BOM)
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        building_names = json.load(f)

    actual_buildings = []

    print(f"Filtering {len(building_names)} entries...")

    for i, name in enumerate(building_names):
        print(f"Checking [{i+1}/{len(building_names)}]: {name}...", end=" ")

        if is_actual_building(name):
            actual_buildings.append(name)
            print(" Building")
        else:
            print(" Not a building")

    print(f"\nFound {len(actual_buildings)} actual buildings out of {len(building_names)} entries")

    # Save to output file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(actual_buildings, f, indent=4, ensure_ascii=False)
        print(f"Saved to {output_file}")

    return actual_buildings


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "list.json")
    output_file = os.path.join(script_dir, "filtered_buildings.json")

    filter_buildings_list(input_file, output_file)
