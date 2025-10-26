import json
import sys
import os

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def is_actual_pokemon(name):
    """
    Use AI to determine if a name represents an actual Pokemon
    (not a made-up name or non-Pokemon creature).

    Args:
        name (str): The name to check

    Returns:
        bool: True if it's an actual Pokemon, False otherwise
    """
    prompt = f"""Is "{name}" the name of an actual Pokemon from the Pokemon franchise?
Answer with just "yes" or "no".
Do NOT count:
- Made-up names that sound like Pokemon but aren't real
- Non-Pokemon creatures or animals
- Pokemon that don't exist in the official games/anime
- Fan-made Pokemon
- Regional variants with different names (use base Pokemon name)

Only count official Pokemon from any generation (1-9) that appear in:
- Pokemon video games
- Pokemon anime
- Pokemon trading card game
- Official Pokemon media

Examples of actual Pokemon: pikachu, charizard, mewtwo, lugia, rayquaza, arceus
Examples of NOT Pokemon: dragon, phoenix, unicorn, griffin"""

    try:
        response = chat_with_kimi(prompt)
        return response.strip().lower() == "yes"
    except Exception as e:
        print(f"Error checking if {name} is a Pokemon: {e}")
        return False


def filter_pokemon_list(input_file="list.json", output_file="filtered_list.json"):
    """
    Filter a Pokemon list to remove non-Pokemon names.

    Args:
        input_file (str): Input JSON file with Pokemon names
        output_file (str): Output JSON file for filtered names
    """
    try:
        # Set default paths if using defaults
        if input_file == "list.json":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            input_file = os.path.join(script_dir, "list.json")
        
        if output_file == "filtered_list.json":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(script_dir, "filtered_list.json")
        
        # Load the Pokemon list
        with open(input_file, 'r') as f:
            pokemon_names = json.load(f)
        
        print(f"Loaded {len(pokemon_names)} Pokemon names from {input_file}")
        print("Filtering to keep only actual Pokemon...")
        
        filtered_names = []
        removed_names = []
        
        for i, name in enumerate(pokemon_names, 1):
            print(f"[{i}/{len(pokemon_names)}] Checking {name}...")
            
            if is_actual_pokemon(name):
                filtered_names.append(name)
                print(f"  ✓ {name} is a Pokemon")
            else:
                removed_names.append(name)
                print(f"  ✗ {name} is not a Pokemon")
        
        # Save filtered list
        with open(output_file, 'w') as f:
            json.dump(filtered_names, f, indent=2)
        
        print(f"\nFiltering complete!")
        print(f"Original count: {len(pokemon_names)}")
        print(f"Filtered count: {len(filtered_names)}")
        print(f"Removed: {len(removed_names)}")
        print(f"Filtered list saved to: {output_file}")
        
        if removed_names:
            print(f"\nRemoved names:")
            for name in removed_names:
                print(f"  - {name}")
        
    except Exception as e:
        print(f"Error filtering Pokemon list: {e}")


def main():
    """Main function to filter Pokemon list."""
    print("Pokemon List Filter")
    print("=" * 30)
    
    input_file = input("Enter input file [list.json]: ").strip() or "list.json"
    output_file = input("Enter output file [filtered_list.json]: ").strip() or "filtered_list.json"
    
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found!")
        return
    
    filter_pokemon_list(input_file, output_file)


if __name__ == "__main__":
    main()
