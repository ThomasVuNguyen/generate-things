import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_supply_names_batch(prompt_template, count=100):
    """
    Generate a batch of supply names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of supplys to generate in this batch
    
    Returns:
        list: List of supply names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        supplys = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    supplys.append(clean_name.lower())
        
        print(f"Generated {len(supplys)} supplys from this batch")
        return supplys
        
    except Exception as e:
        print(f"Error generating supplys in batch: {e}")
        return []


def generate_supply_names_multi_batch(target_count=500):
    """
    Generate supply names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of supplys to generate
    
    Returns:
        list: List of supply names
    """
    print(f"Generating {target_count} diverse supply names using multiple specialized prompts...")
    
    # Define different prompt templates for different supply categories
    prompts = [
        {
            "name": "Balls & Sports Supplys",
            "template": """Generate exactly {count} ball and sports supply names.

Requirements:
- Only single-word supply names (no spaces, hyphens, or compound words)
- Focus on balls and sports supplys
- Include: ball, football, baseball, basketball, soccer_ball, tennis_ball
- NO brand names, NO duplicates

Return ONLY the supply names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Action Figures & Dolls",
            "template": """Generate exactly {count} action figure and doll names.

Requirements:
- Only single-word supply names (no spaces, hyphens, or compound words)
- Focus on action figures and dolls
- Include: doll, figure, action_figure, robot, stuffed_animal
- NO brand names, NO duplicates

Return ONLY the supply names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Building Supplys",
            "template": """Generate exactly {count} building supply names.

Requirements:
- Only single-word supply names (no spaces, hyphens, or compound words)
- Focus on building supplys
- Include: block, brick, lego, building_block, puzzle_piece
- NO brand names, NO duplicates

Return ONLY the supply names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Vehicle Supplys",
            "template": """Generate exactly {count} vehicle supply names.

Requirements:
- Only single-word supply names (no spaces, hyphens, or compound words)
- Focus on vehicle supplys
- Include: car, truck, airplane, helicopter, train, boat
- NO brand names, NO duplicates

Return ONLY the supply names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Traditional & Classic Supplys",
            "template": """Generate exactly {count} traditional and classic supply names.

Requirements:
- Only single-word supply names (no spaces, hyphens, or compound words)
- Focus on traditional and classic supplys
- Include: top, yo_yo, kite, top, frisbee, jacks, marbles
- NO brand names, NO duplicates

Return ONLY the supply names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_supplys = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        supplys = generate_supply_names_batch(prompt_info['template'], batch_size)
        all_supplys.extend(supplys)
        print(f"Total supplys so far: {len(all_supplys)}")
    
    return all_supplys


def filter_single_word_supplys(supplys):
    """
    Filter supplys to ensure they are single words only.
    
    Args:
        supplys (list): List of supply names
    
    Returns:
        list: Filtered list of single-word supplys
    """
    filtered = []
    for supply in supplys:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(supply.split()) == 1 and '-' not in supply and '_' not in supply:
            filtered.append(supply)
    
    return filtered


def save_supply_list(supplys, filename="list.json", merge_existing=True):
    """
    Save the supplys list to a JSON file.
    
    Args:
        supplys (list): List of supply names
        filename (str): Output filename
        merge_existing (bool): If True, merge with existing list; if False, replace it
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    # Merge with existing items if requested
    if merge_existing and os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing_supplys = json.load(f)
                # Combine and deduplicate
                all_supplys = list(dict.fromkeys(existing_supplys + supplys))  # Preserves order
                supplys = all_supplys
                print(f"Merged with {len(existing_supplys)} existing items")
            except json.JSONDecodeError:
                print("Could not read existing file, overwriting...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(supplys, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save supply names."""
    print("=== Enhanced Office Supply Name Generator ===")
    print("Generating 500+ diverse single-word supply names using multiple specialized prompts...")
    print()
    
    # Generate supplys using multiple specialized prompts
    supplys = generate_supply_names_multi_batch(target_count=500)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word supplys only...")
    filtered_supplys = filter_single_word_supplys(supplys)
    
    print(f"After filtering: {len(filtered_supplys)} single-word supplys")
    
    # Remove duplicates while preserving order
    unique_supplys = []
    seen = set()
    for supply in filtered_supplys:
        if supply not in seen:
            unique_supplys.append(supply)
            seen.add(supply)
    
    print(f"After removing duplicates: {len(unique_supplys)} unique supplys")
    
    # Take the available items
    final_supplys = unique_supplys[:500]
    
    # Save to file
    filepath = save_supply_list(final_supplys)
    
    print(f"\n✓ Generated {len(final_supplys)} common single-word supply names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 supplys:")
    for i, supply in enumerate(final_supplys[:20], 1):
        print(f"  {i:2d}. {supply}")
    
    if len(final_supplys) > 20:
        print(f"  ... and {len(final_supplys) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(supplys)}")
    print(f"  After filtering: {len(filtered_supplys)}")
    print(f"  After deduplication: {len(unique_supplys)}")
    print(f"  Final count: {len(final_supplys)}")


if __name__ == "__main__":
    main()

