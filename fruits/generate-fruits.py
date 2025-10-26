import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_fruit_names_batch(prompt_template, count=200):
    """
    Generate a batch of fruit names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of fruits to generate in this batch
    
    Returns:
        list: List of fruit names
    """
    prompt = prompt_template.format(count=count)
    
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
        
        print(f"Generated {len(fruits)} fruits from this batch")
        return fruits
        
    except Exception as e:
        print(f"Error generating fruits in batch: {e}")
        return []


def generate_fruit_names_multi_batch(target_count=1000):
    """
    Generate fruit names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of fruits to generate
    
    Returns:
        list: List of fruit names
    """
    print(f"Generating {target_count} diverse fruit names using multiple specialized prompts...")
    
    # Define different prompt templates for different fruit categories
    prompts = [
        {
            "name": "Common Temperate Fruits",
            "template": """Generate exactly {count} common temperate fruit names.

Requirements:
- Only single-word fruit names (no spaces, hyphens, or compound words)
- Focus on fruits commonly grown in temperate climates
- Include: apples, pears, peaches, plums, cherries, apricots, nectarines, grapes, berries
- NO vegetables, nuts, spices, or scientific names
- NO duplicates

Return ONLY the fruit names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Tropical & Exotic Fruits",
            "template": """Generate exactly {count} tropical and exotic fruit names.

Requirements:
- Only single-word fruit names (no spaces, hyphens, or compound words)
- Focus on tropical and exotic fruits from around the world
- Include: mango, pineapple, papaya, coconut, banana, guava, passionfruit, dragonfruit, lychee, rambutan, durian, jackfruit
- NO vegetables, nuts, spices, or scientific names
- NO duplicates

Return ONLY the fruit names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Citrus Fruits",
            "template": """Generate exactly {count} citrus fruit names.

Requirements:
- Only single-word fruit names (no spaces, hyphens, or compound words)
- Focus on citrus fruits and their varieties
- Include: orange, lemon, lime, grapefruit, tangerine, mandarin, clementine, pomelo, kumquat, yuzu
- NO vegetables, nuts, spices, or scientific names
- NO duplicates

Return ONLY the fruit names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Berries & Small Fruits",
            "template": """Generate exactly {count} berry and small fruit names.

Requirements:
- Only single-word fruit names (no spaces, hyphens, or compound words)
- Focus on berries and small fruits
- Include: strawberry, blueberry, raspberry, blackberry, cranberry, gooseberry, elderberry, mulberry, currant
- NO vegetables, nuts, spices, or scientific names
- NO duplicates

Return ONLY the fruit names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Melons & Large Fruits",
            "template": """Generate exactly {count} melon and large fruit names.

Requirements:
- Only single-word fruit names (no spaces, hyphens, or compound words)
- Focus on melons and large fruits
- Include: watermelon, cantaloupe, honeydew, muskmelon, pumpkin (as fruit), squash varieties
- NO vegetables, nuts, spices, or scientific names
- NO duplicates

Return ONLY the fruit names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Rare & Uncommon Fruits",
            "template": """Generate exactly {count} rare and uncommon fruit names.

Requirements:
- Only single-word fruit names (no spaces, hyphens, or compound words)
- Focus on rare, uncommon, or lesser-known fruits from around the world
- Include fruits from South America, Africa, Asia, and other regions
- NO vegetables, nuts, spices, or scientific names
- NO duplicates

Return ONLY the fruit names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_fruits = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        fruits = generate_fruit_names_batch(prompt_info['template'], batch_size)
        all_fruits.extend(fruits)
        print(f"Total fruits so far: {len(all_fruits)}")
    
    return all_fruits


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
    print("=== Enhanced Fruit Name Generator ===")
    print("Generating 1000+ diverse single-word fruit names using multiple specialized prompts...")
    print()
    
    # Generate fruits using multiple specialized prompts
    fruits = generate_fruit_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word fruits only...")
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
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(fruits)}")
    print(f"  After filtering: {len(filtered_fruits)}")
    print(f"  After deduplication: {len(unique_fruits)}")
    print(f"  Final count: {len(final_fruits)}")


if __name__ == "__main__":
    main()
