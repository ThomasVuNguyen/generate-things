import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_furniture_names_batch(prompt_template, count=100):
    """
    Generate a batch of furniture names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of furniture items to generate in this batch
    
    Returns:
        list: List of furniture names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        furniture_items = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    furniture_items.append(clean_name.lower())
        
        print(f"Generated {len(furniture_items)} furniture items from this batch")
        return furniture_items
        
    except Exception as e:
        print(f"Error generating furniture in batch: {e}")
        return []


def generate_furniture_names_multi_batch(target_count=500):
    """
    Generate furniture names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of furniture items to generate
    
    Returns:
        list: List of furniture names
    """
    print(f"Generating {target_count} diverse furniture names using multiple specialized prompts...")
    
    # Define different prompt templates for different furniture categories
    prompts = [
        {
            "name": "Seating Furniture",
            "template": """Generate exactly {count} seating furniture names.

Requirements:
- Only single-word furniture names (no spaces, hyphens, or compound words)
- Focus on seating furniture
- Include: chair, sofa, bench, stool, ottoman, recliner, stool, armchair
- NO brand names, NO specific styles, NO duplicates

Return ONLY the furniture names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Tables & Surfaces",
            "template": """Generate exactly {count} table and surface furniture names.

Requirements:
- Only single-word furniture names (no spaces, hyphens, or compound words)
- Focus on tables and surface furniture
- Include: desk, table, nightstand, coffee_table, end_table, dining_table
- NO brand names, NO specific styles, NO duplicates

Return ONLY the furniture names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Storage Furniture",
            "template": """Generate exactly {count} storage furniture names.

Requirements:
- Only single-word furniture names (no spaces, hyphens, or compound words)
- Focus on storage furniture
- Include: cabinet, dresser, wardrobe, chest, shelf, hutch, buffet, pantry
- NO brand names, NO specific styles, NO duplicates

Return ONLY the furniture names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Bedroom Furniture",
            "template": """Generate exactly {count} bedroom furniture names.

Requirements:
- Only single-word furniture names (no spaces, hyphens, or compound words)
- Focus on bedroom furniture
- Include: bed, dresser, mirror, nightstand, headboard
- NO brand names, NO specific styles, NO duplicates

Return ONLY the furniture names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Decorative & Accent Pieces",
            "template": """Generate exactly {count} decorative and accent furniture names.

Requirements:
- Only single-word furniture names (no spaces, hyphens, or compound words)
- Focus on decorative and accent furniture
- Include: lamp, plant_stand, display_case, mirror, shelf
- NO brand names, NO specific styles, NO duplicates

Return ONLY the furniture names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_furniture = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        furniture_items = generate_furniture_names_batch(prompt_info['template'], batch_size)
        all_furniture.extend(furniture_items)
        print(f"Total furniture items so far: {len(all_furniture)}")
    
    return all_furniture


def filter_single_word_furniture(furniture_list):
    """
    Filter furniture to ensure they are single words only.
    
    Args:
        furniture_list (list): List of furniture names
    
    Returns:
        list: Filtered list of single-word furniture
    """
    filtered = []
    for furniture in furniture_list:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(furniture.split()) == 1 and '-' not in furniture and '_' not in furniture:
            filtered.append(furniture)
    
    return filtered


def save_furniture_list(furniture_list, filename="list.json"):
    """
    Save the furniture list to a JSON file.
    
    Args:
        furniture_list (list): List of furniture names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(furniture_list, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save furniture names."""
    print("=== Enhanced Furniture Name Generator ===")
    print("Generating 500+ diverse single-word furniture names using multiple specialized prompts...")
    print()
    
    # Generate furniture using multiple specialized prompts
    furniture_items = generate_furniture_names_multi_batch(target_count=500)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word furniture items only...")
    filtered_furniture = filter_single_word_furniture(furniture_items)
    
    print(f"After filtering: {len(filtered_furniture)} single-word furniture items")
    
    # Remove duplicates while preserving order
    unique_furniture = []
    seen = set()
    for furniture in filtered_furniture:
        if furniture not in seen:
            unique_furniture.append(furniture)
            seen.add(furniture)
    
    print(f"After removing duplicates: {len(unique_furniture)} unique furniture items")
    
    # Take the available items
    final_furniture = unique_furniture[:500]
    
    # Save to file
    filepath = save_furniture_list(final_furniture)
    
    print(f"\n✓ Generated {len(final_furniture)} common single-word furniture names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 furniture items:")
    for i, furniture in enumerate(final_furniture[:20], 1):
        print(f"  {i:2d}. {furniture}")
    
    if len(final_furniture) > 20:
        print(f"  ... and {len(final_furniture) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(furniture_items)}")
    print(f"  After filtering: {len(filtered_furniture)}")
    print(f"  After deduplication: {len(unique_furniture)}")
    print(f"  Final count: {len(final_furniture)}")


if __name__ == "__main__":
    main()

