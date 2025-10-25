import json
import sys
import os

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def is_actual_animal(name):
    """
    Use AI to determine if a name represents an actual animal species
    (not a breed, dinosaur, or other non-animal).

    Args:
        name (str): The name to check

    Returns:
        bool: True if it's an actual animal, False otherwise
    """
    prompt = f"""Is "{name}" the name of an actual living animal species?
Answer with just "yes" or "no".
Do NOT count:
- Dinosaurs or extinct species
- Dog breeds (like "Beagle", "Poodle")
- Cat breeds (like "Persian", "Siamese")
- Horse breeds (like "Arabian Horse", "Mustang")
- Bird breeds
- Specific domesticated animal breeds

DO count:
- Wild animal species (like "tiger", "elephant", "eagle")
- General animal categories (like "cat", "dog", "horse" without breed specification)

Answer:"""

    try:
        response = chat_with_kimi(prompt, stream=False)
        answer = response.strip().lower()
        return "yes" in answer
    except Exception as e:
        print(f"Error checking '{name}': {e}")
        return False


def filter_animals_list(input_file, output_file=None):
    """
    Filter the animals list to only include actual animals.

    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to save filtered results (optional)

    Returns:
        list: List of actual animals
    """
    # Load the list (using utf-8-sig to handle BOM)
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        animal_names = json.load(f)

    actual_animals = []

    print(f"Filtering {len(animal_names)} entries...")

    for i, name in enumerate(animal_names):
        print(f"Checking [{i+1}/{len(animal_names)}]: {name}...", end=" ")

        if is_actual_animal(name):
            actual_animals.append(name)
            print(" Animal")
        else:
            print(" Not an animal")

    print(f"\nFound {len(actual_animals)} actual animals out of {len(animal_names)} entries")

    # Save to output file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(actual_animals, f, indent=4, ensure_ascii=False)
        print(f"Saved to {output_file}")

    return actual_animals


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "list.json")
    output_file = os.path.join(script_dir, "filtered_animals.json")

    filter_animals_list(input_file, output_file)
