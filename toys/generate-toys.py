import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_toy_names_batch(prompt_template, count=100):
    """
    Generate a batch of toy names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of toys to generate in this batch
    
    Returns:
        list: List of toy names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        toys = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    toys.append(clean_name.lower())
        
        print(f"Generated {len(toys)} toys from this batch")
        return toys
        
    except Exception as e:
        print(f"Error generating toys in batch: {e}")
        return []


def generate_toy_names_multi_batch(target_count=500):
    """
    Generate toy names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of toys to generate
    
    Returns:
        list: List of toy names
    """
    print(f"Generating {target_count} diverse toy names using multiple specialized prompts...")
    
    # Define different prompt templates for different toy categories
    prompts = [
        {
            "name": "Balls & Sports Toys",
            "template": """Generate exactly {count} ball and sports toy names.

Requirements:
- Only single-word toy names (no spaces, hyphens, or compound words)
- Focus on balls and sports toys
- Include: ball, football, baseball, basketball, soccer_ball, tennis_ball
- NO brand names, NO duplicates

Return ONLY the toy names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Action Figures & Dolls",
            "template": """Generate exactly {count} action figure and doll names.

Requirements:
- Only single-word toy names (no spaces, hyphens, or compound words)
- Focus on action figures and dolls
- Include: doll, figure, action_figure, robot, stuffed_animal
- NO brand names, NO duplicates

Return ONLY the toy names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Building Toys",
            "template": """Generate exactly {count} building toy names.

Requirements:
- Only single-word toy names (no spaces, hyphens, or compound words)
- Focus on building toys
- Include: block, brick, lego, building_block, puzzle_piece
- NO brand names, NO duplicates

Return ONLY the toy names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Vehicle Toys",
            "template": """Generate exactly {count} vehicle toy names.

Requirements:
- Only single-word toy names (no spaces, hyphens, or compound words)
- Focus on vehicle toys
- Include: car, truck, airplane, helicopter, train, boat
- NO brand names, NO duplicates

Return ONLY the toy names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Traditional & Classic Toys",
            "template": """Generate exactly {count} traditional and classic toy names.

Requirements:
- Only single-word toy names (no spaces, hyphens, or compound words)
- Focus on traditional and classic toys
- Include: top, yo_yo, kite, top, frisbee, jacks, marbles
- NO brand names, NO duplicates

Return ONLY the toy names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_toys = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        toys = generate_toy_names_batch(prompt_info['template'], batch_size)
        all_toys.extend(toys)
        print(f"Total toys so far: {len(all_toys)}")
    
    return all_toys


def filter_single_word_toys(toys):
    """
    Filter toys to ensure they are single words only.
    
    Args:
        toys (list): List of toy names
    
    Returns:
        list: Filtered list of single-word toys
    """
    filtered = []
    for toy in toys:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(toy.split()) == 1 and '-' not in toy and '_' not in toy:
            filtered.append(toy)
    
    return filtered


def save_toys_list(toys, filename="list.json", merge_existing=True):
    """
    Save the toys list to a JSON file.
    
    Args:
        toys (list): List of toy names
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
                existing_toys = json.load(f)
                # Combine and deduplicate
                all_toys = list(dict.fromkeys(existing_toys + toys))  # Preserves order
                toys = all_toys
                print(f"Merged with {len(existing_toys)} existing items")
            except json.JSONDecodeError:
                print("Could not read existing file, overwriting...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(toys, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save toy names."""
    print("=== Enhanced Toy Name Generator ===")
    print("Generating 500+ diverse single-word toy names using multiple specialized prompts...")
    print()
    
    # Generate toys using multiple specialized prompts
    toys = generate_toy_names_multi_batch(target_count=500)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word toys only...")
    filtered_toys = filter_single_word_toys(toys)
    
    print(f"After filtering: {len(filtered_toys)} single-word toys")
    
    # Remove duplicates while preserving order
    unique_toys = []
    seen = set()
    for toy in filtered_toys:
        if toy not in seen:
            unique_toys.append(toy)
            seen.add(toy)
    
    print(f"After removing duplicates: {len(unique_toys)} unique toys")
    
    # Take the available items
    final_toys = unique_toys[:500]
    
    # Save to file
    filepath = save_toys_list(final_toys)
    
    print(f"\n✓ Generated {len(final_toys)} common single-word toy names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 toys:")
    for i, toy in enumerate(final_toys[:20], 1):
        print(f"  {i:2d}. {toy}")
    
    if len(final_toys) > 20:
        print(f"  ... and {len(final_toys) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(toys)}")
    print(f"  After filtering: {len(filtered_toys)}")
    print(f"  After deduplication: {len(unique_toys)}")
    print(f"  Final count: {len(final_toys)}")


if __name__ == "__main__":
    main()

