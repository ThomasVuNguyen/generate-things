import json
import sys
import os

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def is_actual_household_item(name):
    """
    Use AI to determine if a name represents an actual household item
    (not a food item, animal, or other non-household item).

    Args:
        name (str): The name to check

    Returns:
        bool: True if it's an actual household item, False otherwise
    """
    prompt = f"""Is "{name}" the name of an actual household item?
Answer with just "yes" or "no".
Do NOT count:
- Food items (like "apple", "bread", "milk", "cheese")
- Animals (like "cat", "dog", "bird", "fish")
- Plants (like "tree", "flower", "grass")
- People or body parts
- Abstract concepts (like "love", "time", "space")
- Vehicles (like "car", "bike", "plane")
- Buildings or rooms (like "house", "kitchen", "bedroom")

DO count:
- Kitchen items (like "plate", "bowl", "spoon", "pot")
- Furniture (like "chair", "table", "bed", "sofa")
- Electronics (like "phone", "computer", "television")
- Cleaning supplies (like "broom", "mop", "soap")
- Personal care items (like "toothbrush", "towel", "mirror")
- Decorative items (like "vase", "candle", "picture")
- Tools and utensils (like "hammer", "scissors", "knife")

Answer:"""

    try:
        response = chat_with_kimi(prompt, stream=False)
        answer = response.strip().lower()
        return "yes" in answer
    except Exception as e:
        print(f"Error checking '{name}': {e}")
        return False


def filter_household_items_list(input_file, output_file=None):
    """
    Filter the household items list to only include actual household items.

    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to save filtered results (optional)

    Returns:
        list: List of actual household items
    """
    # Load the list (using utf-8-sig to handle BOM)
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        item_names = json.load(f)

    actual_items = []

    print(f"Filtering {len(item_names)} entries...")

    for i, name in enumerate(item_names):
        print(f"Checking [{i+1}/{len(item_names)}]: {name}...", end=" ")

        if is_actual_household_item(name):
            actual_items.append(name)
            print(" Household item")
        else:
            print(" Not a household item")

    print(f"\nFound {len(actual_items)} actual household items out of {len(item_names)} entries")

    # Save to output file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(actual_items, f, indent=4, ensure_ascii=False)
        print(f"Saved to {output_file}")

    return actual_items


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "list.json")
    output_file = os.path.join(script_dir, "filtered_household_items.json")

    filter_household_items_list(input_file, output_file)
