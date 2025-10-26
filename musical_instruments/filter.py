import json
import sys
import os

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def is_actual_musical_instrument(name):
    """
    Use AI to determine if a name represents an actual musical instrument
    (not a tool, vehicle, or other non-instrument).

    Args:
        name (str): The name to check

    Returns:
        bool: True if it's an actual musical instrument, False otherwise
    """
    prompt = f"""Is "{name}" the name of an actual musical instrument?
Answer with just "yes" or "no".
Do NOT count:
- Tools (like "hammer", "saw", "drill")
- Vehicles (like "car", "boat", "plane")
- Buildings (like "house", "tower", "bridge")
- Food items (like "apple", "bread", "milk")
- Animals (like "cat", "dog", "bird")
- People or body parts
- Abstract concepts (like "music", "sound", "rhythm")

DO count:
- String instruments (like "guitar", "violin", "harp")
- Wind instruments (like "flute", "trumpet", "saxophone")
- Percussion instruments (like "drum", "cymbal", "xylophone")
- Keyboard instruments (like "piano", "organ", "synthesizer")
- Electronic instruments (like "theremin", "sampler", "sequencer")
- Traditional/world instruments (like "didgeridoo", "koto", "tabla")

Answer:"""

    try:
        response = chat_with_kimi(prompt, stream=False)
        answer = response.strip().lower()
        return "yes" in answer
    except Exception as e:
        print(f"Error checking '{name}': {e}")
        return False


def filter_musical_instruments_list(input_file, output_file=None):
    """
    Filter the musical instruments list to only include actual musical instruments.

    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to save filtered results (optional)

    Returns:
        list: List of actual musical instruments
    """
    # Load the list (using utf-8-sig to handle BOM)
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        instrument_names = json.load(f)

    actual_instruments = []

    print(f"Filtering {len(instrument_names)} entries...")

    for i, name in enumerate(instrument_names):
        print(f"Checking [{i+1}/{len(instrument_names)}]: {name}...", end=" ")

        if is_actual_musical_instrument(name):
            actual_instruments.append(name)
            print(" Musical instrument")
        else:
            print(" Not a musical instrument")

    print(f"\nFound {len(actual_instruments)} actual musical instruments out of {len(instrument_names)} entries")

    # Save to output file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(actual_instruments, f, indent=4, ensure_ascii=False)
        print(f"Saved to {output_file}")

    return actual_instruments


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "list.json")
    output_file = os.path.join(script_dir, "filtered_musical_instruments.json")

    filter_musical_instruments_list(input_file, output_file)
