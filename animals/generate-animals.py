import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_animal_names(count=1000):
    """
    Generate a list of common animal names using the Kimi model in one go.
    
    Args:
        count (int): Total number of animals to generate
    
    Returns:
        list: List of animal names
    """
    print(f"Generating {count} diverse animal names in one go...")
    
    prompt = f"""Generate a list of exactly {count} diverse animal names.

Requirements:
- Only single-word animal names (no spaces, hyphens, or compound words)
- Include a wide variety of animals from different categories
- Include both common and less common animals
- Include mammals, birds, fish, reptiles, amphibians, insects, arachnids, mollusks
- NO extinct animals (dinosaurs, etc.)
- NO animal breeds (like "Golden Retriever", "Persian Cat")
- NO scientific names
- NO regional variants or subspecies
- NO mythical or fictional animals
- Make sure each animal name is unique (no duplicates)

Focus on diverse categories:
- Marine animals: shark, whale, dolphin, octopus, squid, jellyfish, starfish, crab, lobster, shrimp
- Birds: eagle, hawk, owl, parrot, penguin, flamingo, peacock, toucan, hummingbird, woodpecker
- Reptiles: snake, lizard, turtle, crocodile, alligator, gecko, iguana, chameleon
- Amphibians: frog, toad, salamander, newt
- Insects: butterfly, bee, ant, beetle, dragonfly, grasshopper, cricket, moth, wasp, fly
- Arachnids: spider, scorpion, tick, mite
- Mammals: bat, squirrel, chipmunk, raccoon, skunk, opossum, beaver, otter, seal, walrus
- And many more diverse species from around the world

Return ONLY the animal names, one per line, no numbers, no explanations, no additional text."""

    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        animals = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    animals.append(clean_name.lower())
        
        print(f"Generated {len(animals)} animals from API response")
        return animals
        
    except Exception as e:
        print(f"Error generating animals: {e}")
        return []


def filter_single_word_animals(animals):
    """
    Filter animals to ensure they are single words only.
    
    Args:
        animals (list): List of animal names
    
    Returns:
        list: Filtered list of single-word animals
    """
    filtered = []
    for animal in animals:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(animal.split()) == 1 and '-' not in animal and '_' not in animal:
            filtered.append(animal)
    
    return filtered


def save_animals_list(animals, filename="list.json"):
    """
    Save the animals list to a JSON file.
    
    Args:
        animals (list): List of animal names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(animals, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save animal names."""
    print("=== Animal Name Generator ===")
    print("Generating 1000 common single-word animal names...")
    print()
    
    # Generate animals in one go
    animals = generate_animal_names(count=1000)
    
    # Filter to ensure single words only
    print("\nFiltering to single-word animals only...")
    filtered_animals = filter_single_word_animals(animals)
    
    print(f"After filtering: {len(filtered_animals)} single-word animals")
    
    # Remove duplicates while preserving order
    unique_animals = []
    seen = set()
    for animal in filtered_animals:
        if animal not in seen:
            unique_animals.append(animal)
            seen.add(animal)
    
    print(f"After removing duplicates: {len(unique_animals)} unique animals")
    
    # Take exactly 1000 (or as many as we have)
    final_animals = unique_animals[:1000]
    
    # Save to file
    filepath = save_animals_list(final_animals)
    
    print(f"\n✓ Generated {len(final_animals)} common single-word animal names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 animals:")
    for i, animal in enumerate(final_animals[:20], 1):
        print(f"  {i:2d}. {animal}")
    
    if len(final_animals) > 20:
        print(f"  ... and {len(final_animals) - 20} more")


if __name__ == "__main__":
    main()
