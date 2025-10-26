import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_fruit_names(count=1000):
    """
    Generate a list of common fruit names using the Kimi model in one go.
    
    Args:
        count (int): Total number of fruits to generate
    
    Returns:
        list: List of fruit names
    """
    print(f"Generating {count} diverse fruit names in one go...")
    
    prompt = f"""Generate a list of exactly {count} diverse fruit names.

Requirements:
- Only single-word fruit names (no spaces, hyphens, or compound words)
- Include a wide variety of fruits from different categories
- Include both common and less common fruits
- Include tropical fruits, temperate fruits, berries, citrus fruits, stone fruits, pome fruits
- NO vegetables (tomato, cucumber, etc.)
- NO nuts (almond, walnut, etc.)
- NO spices or herbs
- NO scientific names
- NO regional variants or subspecies
- NO processed fruit products (jam, juice, etc.)
- Make sure each fruit name is unique (no duplicates)

Focus on diverse categories:
- Citrus fruits: orange, lemon, lime, grapefruit, tangerine, mandarin, pomelo, kumquat
- Berries: strawberry, blueberry, raspberry, blackberry, cranberry, gooseberry, elderberry, mulberry
- Tropical fruits: mango, pineapple, papaya, coconut, banana, guava, passionfruit, dragonfruit, lychee
- Stone fruits: peach, plum, cherry, apricot, nectarine, avocado
- Pome fruits: apple, pear, quince
- Melons: watermelon, cantaloupe, honeydew, muskmelon
- Grapes and vine fruits: grape, kiwi
- And many more diverse fruits from around the world

Return ONLY the fruit names, one per line, no numbers, no explanations, no additional text."""

    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        fruits = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    fruits.append(clean_name.lower())
        
        print(f"Generated {len(fruits)} fruits from API response")
        return fruits
        
    except Exception as e:
        print(f"Error generating fruits: {e}")
        return []


def filter_single_word_fruits(fruits):
    """
    Filter fruits to ensure they are single words only.
    
    Args:
        fruits (list): List of fruit names
    
    Returns:
        list: Filtered list of single-word fruits
    """
    filtered = []
    for fruit in fruits:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(fruit.split()) == 1 and '-' not in fruit and '_' not in fruit:
            filtered.append(fruit)
    
    return filtered


def save_fruits_list(fruits, filename="list.json"):
    """
    Save the fruits list to a JSON file.
    
    Args:
        fruits (list): List of fruit names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(fruits, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save fruit names."""
    print("=== Fruit Name Generator ===")
    print("Generating 1000 common single-word fruit names...")
    print()
    
    # Generate fruits in one go
    fruits = generate_fruit_names(count=1000)
    
    # Filter to ensure single words only
    print("\nFiltering to single-word fruits only...")
    filtered_fruits = filter_single_word_fruits(fruits)
    
    print(f"After filtering: {len(filtered_fruits)} single-word fruits")
    
    # Remove duplicates while preserving order
    unique_fruits = []
    seen = set()
    for fruit in filtered_fruits:
        if fruit not in seen:
            unique_fruits.append(fruit)
            seen.add(fruit)
    
    print(f"After removing duplicates: {len(unique_fruits)} unique fruits")
    
    # Take exactly 1000 (or as many as we have)
    final_fruits = unique_fruits[:1000]
    
    # Save to file
    filepath = save_fruits_list(final_fruits)
    
    print(f"\n✓ Generated {len(final_fruits)} common single-word fruit names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 fruits:")
    for i, fruit in enumerate(final_fruits[:20], 1):
        print(f"  {i:2d}. {fruit}")
    
    if len(final_fruits) > 20:
        print(f"  ... and {len(final_fruits) - 20} more")


if __name__ == "__main__":
    main()
