import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_household_item_names_batch(prompt_template, count=200):
    """
    Generate a batch of household item names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of household items to generate in this batch
    
    Returns:
        list: List of household item names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        items = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    items.append(clean_name.lower())
        
        print(f"Generated {len(items)} household items from this batch")
        return items
        
    except Exception as e:
        print(f"Error generating household items in batch: {e}")
        return []


def generate_household_item_names_multi_batch(target_count=1000):
    """
    Generate household item names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of household items to generate
    
    Returns:
        list: List of household item names
    """
    print(f"Generating {target_count} diverse household item names using multiple specialized prompts...")
    
    # Define different prompt templates for different household item categories
    prompts = [
        {
            "name": "Kitchen Items",
            "template": """Generate exactly {count} kitchen household item names.

Requirements:
- Only single-word item names (no spaces, hyphens, or compound words)
- Focus on items commonly found in kitchens
- Include: plate, bowl, cup, mug, glass, spoon, fork, knife, pot, pan, kettle, toaster, blender, mixer
- NO brand names, NO scientific names, NO duplicates
- Focus on everyday kitchen items that people use regularly

Return ONLY the item names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Furniture & Storage",
            "template": """Generate exactly {count} furniture and storage household item names.

Requirements:
- Only single-word item names (no spaces, hyphens, or compound words)
- Focus on furniture and storage items found in homes
- Include: chair, table, desk, bed, sofa, couch, shelf, cabinet, drawer, closet, wardrobe, dresser
- NO brand names, NO scientific names, NO duplicates
- Focus on common furniture pieces and storage solutions

Return ONLY the item names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Electronics & Appliances",
            "template": """Generate exactly {count} electronics and appliance household item names.

Requirements:
- Only single-word item names (no spaces, hyphens, or compound words)
- Focus on electronic devices and appliances found in homes
- Include: phone, computer, laptop, tablet, television, radio, speaker, camera, clock, lamp, fan, heater
- NO brand names, NO scientific names, NO duplicates
- Focus on common electronic devices and home appliances

Return ONLY the item names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Cleaning & Maintenance",
            "template": """Generate exactly {count} cleaning and maintenance household item names.

Requirements:
- Only single-word item names (no spaces, hyphens, or compound words)
- Focus on cleaning supplies and maintenance tools
- Include: broom, mop, vacuum, sponge, towel, rag, brush, soap, detergent, cleaner, tool, hammer, screwdriver
- NO brand names, NO scientific names, NO duplicates
- Focus on cleaning supplies and basic maintenance tools

Return ONLY the item names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Bedroom & Bathroom Items",
            "template": """Generate exactly {count} bedroom and bathroom household item names.

Requirements:
- Only single-word item names (no spaces, hyphens, or compound words)
- Focus on items found in bedrooms and bathrooms
- Include: pillow, blanket, sheet, towel, soap, shampoo, toothbrush, mirror, comb, brush, razor, lotion
- NO brand names, NO scientific names, NO duplicates
- Focus on personal care and bedroom items

Return ONLY the item names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Decorative & Miscellaneous",
            "template": """Generate exactly {count} decorative and miscellaneous household item names.

Requirements:
- Only single-word item names (no spaces, hyphens, or compound words)
- Focus on decorative items and miscellaneous household objects
- Include: vase, candle, frame, picture, plant, book, magazine, toy, game, puzzle, basket, box, bag
- NO brand names, NO scientific names, NO duplicates
- Focus on decorative items and miscellaneous household objects

Return ONLY the item names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_items = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        items = generate_household_item_names_batch(prompt_info['template'], batch_size)
        all_items.extend(items)
        print(f"Total items so far: {len(all_items)}")
    
    return all_items


def filter_single_word_items(items):
    """
    Filter household items to ensure they are single words only.
    
    Args:
        items (list): List of household item names
    
    Returns:
        list: Filtered list of single-word items
    """
    filtered = []
    for item in items:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(item.split()) == 1 and '-' not in item and '_' not in item:
            filtered.append(item)
    
    return filtered


def save_items_list(items, filename="list.json"):
    """
    Save the household items list to a JSON file.
    
    Args:
        items (list): List of household item names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save household item names."""
    print("=== Enhanced Household Item Name Generator ===")
    print("Generating 1000+ diverse single-word household item names using multiple specialized prompts...")
    print()
    
    # Generate household items using multiple specialized prompts
    items = generate_household_item_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word items only...")
    filtered_items = filter_single_word_items(items)
    
    print(f"After filtering: {len(filtered_items)} single-word items")
    
    # Remove duplicates while preserving order
    unique_items = []
    seen = set()
    for item in filtered_items:
        if item not in seen:
            unique_items.append(item)
            seen.add(item)
    
    print(f"After removing duplicates: {len(unique_items)} unique items")
    
    # Take exactly 1000 (or as many as we have)
    final_items = unique_items[:1000]
    
    # Save to file
    filepath = save_items_list(final_items)
    
    print(f"\n✓ Generated {len(final_items)} common single-word household item names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 items:")
    for i, item in enumerate(final_items[:20], 1):
        print(f"  {i:2d}. {item}")
    
    if len(final_items) > 20:
        print(f"  ... and {len(final_items) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(items)}")
    print(f"  After filtering: {len(filtered_items)}")
    print(f"  After deduplication: {len(unique_items)}")
    print(f"  Final count: {len(final_items)}")


if __name__ == "__main__":
    main()
