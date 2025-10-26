import json
import sys
import os

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def is_actual_fruit(name):
    """
    Use AI to determine if a name represents an actual fruit
    (not a vegetable, nut, or other non-fruit).

    Args:
        name (str): The name to check

    Returns:
        bool: True if it's an actual fruit, False otherwise
    """
    prompt = f"""Is "{name}" the name of an actual fruit?
Answer with just "yes" or "no".
Do NOT count:
- Vegetables (like "tomato", "cucumber", "pepper", "eggplant")
- Nuts (like "almond", "walnut", "peanut", "cashew")
- Spices or herbs
- Processed fruit products (like "jam", "juice", "wine")
- Seeds or grains

DO count:
- Fresh fruits (like "apple", "banana", "orange", "grape")
- Berries (like "strawberry", "blueberry", "raspberry")
- Tropical fruits (like "mango", "pineapple", "papaya")
- Citrus fruits (like "lemon", "lime", "grapefruit")
- Stone fruits (like "peach", "plum", "cherry")
- Melons (like "watermelon", "cantaloupe")

Answer:"""

    try:
        response = chat_with_kimi(prompt, stream=False)
        answer = response.strip().lower()
        return "yes" in answer
    except Exception as e:
        print(f"Error checking '{name}': {e}")
        return False


def filter_fruits_list(input_file, output_file=None):
    """
    Filter the fruits list to only include actual fruits.

    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to save filtered results (optional)

    Returns:
        list: List of actual fruits
    """
    # Load the list (using utf-8-sig to handle BOM)
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        fruit_names = json.load(f)

    actual_fruits = []

    print(f"Filtering {len(fruit_names)} entries...")

    for i, name in enumerate(fruit_names):
        print(f"Checking [{i+1}/{len(fruit_names)}]: {name}...", end=" ")

        if is_actual_fruit(name):
            actual_fruits.append(name)
            print(" Fruit")
        else:
            print(" Not a fruit")

    print(f"\nFound {len(actual_fruits)} actual fruits out of {len(fruit_names)} entries")

    # Save to output file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(actual_fruits, f, indent=4, ensure_ascii=False)
        print(f"Saved to {output_file}")

    return actual_fruits


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "list.json")
    output_file = os.path.join(script_dir, "filtered_fruits.json")

    filter_fruits_list(input_file, output_file)
