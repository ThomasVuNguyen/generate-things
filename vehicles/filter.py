import json
import sys
import os

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def is_actual_vehicle(name):
    """
    Use AI to determine if a name represents an actual vehicle
    (not an animal, building, or other non-vehicle).

    Args:
        name (str): The name to check

    Returns:
        bool: True if it's an actual vehicle, False otherwise
    """
    prompt = f"""Is "{name}" the name of an actual vehicle?
Answer with just "yes" or "no".
Do NOT count:
- Animals (like "horse", "camel", "elephant")
- Buildings (like "house", "tower", "bridge")
- Food items (like "apple", "bread", "milk")
- People or body parts
- Abstract concepts (like "speed", "motion", "travel")
- Tools that are not vehicles (like "hammer", "saw", "drill")

DO count:
- Cars and automobiles (like "sedan", "truck", "van")
- Motorcycles and bikes (like "motorcycle", "bicycle", "scooter")
- Boats and watercraft (like "boat", "yacht", "canoe")
- Aircraft (like "airplane", "helicopter", "drone")
- Trains and rail vehicles (like "train", "subway", "tram")
- Construction vehicles (like "bulldozer", "excavator", "crane")

Answer:"""

    try:
        response = chat_with_kimi(prompt, stream=False)
        answer = response.strip().lower()
        return "yes" in answer
    except Exception as e:
        print(f"Error checking '{name}': {e}")
        return False


def filter_vehicles_list(input_file, output_file=None):
    """
    Filter the vehicles list to only include actual vehicles.

    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to save filtered results (optional)

    Returns:
        list: List of actual vehicles
    """
    # Load the list (using utf-8-sig to handle BOM)
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        vehicle_names = json.load(f)

    actual_vehicles = []

    print(f"Filtering {len(vehicle_names)} entries...")

    for i, name in enumerate(vehicle_names):
        print(f"Checking [{i+1}/{len(vehicle_names)}]: {name}...", end=" ")

        if is_actual_vehicle(name):
            actual_vehicles.append(name)
            print(" Vehicle")
        else:
            print(" Not a vehicle")

    print(f"\nFound {len(actual_vehicles)} actual vehicles out of {len(vehicle_names)} entries")

    # Save to output file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(actual_vehicles, f, indent=4, ensure_ascii=False)
        print(f"Saved to {output_file}")

    return actual_vehicles


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "list.json")
    output_file = os.path.join(script_dir, "filtered_vehicles.json")

    filter_vehicles_list(input_file, output_file)
