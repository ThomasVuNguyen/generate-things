import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_art_names_batch(prompt_template, count=100):
    """
    Generate a batch of art names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of arts to generate in this batch
    
    Returns:
        list: List of art names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        arts = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    arts.append(clean_name.lower())
        
        print(f"Generated {len(arts)} arts from this batch")
        return arts
        
    except Exception as e:
        print(f"Error generating arts in batch: {e}")
        return []


def generate_art_names_multi_batch(target_count=500):
    """
    Generate art names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of arts to generate
    
    Returns:
        list: List of art names
    """
    print(f"Generating {target_count} diverse art names using multiple specialized prompts...")
    
    # Define different prompt templates for different art categories
    prompts = [
        {
            "name": "Balls & Sports Arts",
            "template": """Generate exactly {count} ball and sports art names.

Requirements:
- Only single-word art names (no spaces, hyphens, or compound words)
- Focus on balls and sports arts
- Include: ball, football, baseball, basketball, soccer_ball, tennis_ball
- NO brand names, NO duplicates

Return ONLY the art names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Action Figures & Dolls",
            "template": """Generate exactly {count} action figure and doll names.

Requirements:
- Only single-word art names (no spaces, hyphens, or compound words)
- Focus on action figures and dolls
- Include: doll, figure, action_figure, robot, stuffed_animal
- NO brand names, NO duplicates

Return ONLY the art names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Building Arts",
            "template": """Generate exactly {count} building art names.

Requirements:
- Only single-word art names (no spaces, hyphens, or compound words)
- Focus on building arts
- Include: block, brick, lego, building_block, puzzle_piece
- NO brand names, NO duplicates

Return ONLY the art names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Vehicle Arts",
            "template": """Generate exactly {count} vehicle art names.

Requirements:
- Only single-word art names (no spaces, hyphens, or compound words)
- Focus on vehicle arts
- Include: car, truck, airplane, helicopter, train, boat
- NO brand names, NO duplicates

Return ONLY the art names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Traditional & Classic Arts",
            "template": """Generate exactly {count} traditional and classic art names.

Requirements:
- Only single-word art names (no spaces, hyphens, or compound words)
- Focus on traditional and classic arts
- Include: top, yo_yo, kite, top, frisbee, jacks, marbles
- NO brand names, NO duplicates

Return ONLY the art names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_arts = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        arts = generate_art_names_batch(prompt_info['template'], batch_size)
        all_arts.extend(arts)
        print(f"Total arts so far: {len(all_arts)}")
    
    return all_arts


def filter_single_word_arts(arts):
    """
    Filter arts to ensure they are single words only.
    
    Args:
        arts (list): List of art names
    
    Returns:
        list: Filtered list of single-word arts
    """
    filtered = []
    for art in arts:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(art.split()) == 1 and '-' not in art and '_' not in art:
            filtered.append(art)
    
    return filtered


def save_art_list(arts, filename="list.json", merge_existing=True):
    """
    Save the arts list to a JSON file.
    
    Args:
        arts (list): List of art names
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
                existing_arts = json.load(f)
                # Combine and deduplicate
                all_arts = list(dict.fromkeys(existing_arts + arts))  # Preserves order
                arts = all_arts
                print(f"Merged with {len(existing_arts)} existing items")
            except json.JSONDecodeError:
                print("Could not read existing file, overwriting...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(arts, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save art names."""
    print("=== Enhanced Decorative Art Name Generator ===")
    print("Generating 500+ diverse single-word art names using multiple specialized prompts...")
    print()
    
    # Generate arts using multiple specialized prompts
    arts = generate_art_names_multi_batch(target_count=500)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word arts only...")
    filtered_arts = filter_single_word_arts(arts)
    
    print(f"After filtering: {len(filtered_arts)} single-word arts")
    
    # Remove duplicates while preserving order
    unique_arts = []
    seen = set()
    for art in filtered_arts:
        if art not in seen:
            unique_arts.append(art)
            seen.add(art)
    
    print(f"After removing duplicates: {len(unique_arts)} unique arts")
    
    # Take the available items
    final_arts = unique_arts[:500]
    
    # Save to file
    filepath = save_art_list(final_arts)
    
    print(f"\n✓ Generated {len(final_arts)} common single-word art names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 arts:")
    for i, art in enumerate(final_arts[:20], 1):
        print(f"  {i:2d}. {art}")
    
    if len(final_arts) > 20:
        print(f"  ... and {len(final_arts) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(arts)}")
    print(f"  After filtering: {len(filtered_arts)}")
    print(f"  After deduplication: {len(unique_arts)}")
    print(f"  Final count: {len(final_arts)}")


if __name__ == "__main__":
    main()

