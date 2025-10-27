import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_object_names_batch(prompt_template, count=100):
    """
    Generate a batch of object names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of objects to generate in this batch
    
    Returns:
        list: List of object names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        objects = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    objects.append(clean_name.lower())
        
        print(f"Generated {len(objects)} objects from this batch")
        return objects
        
    except Exception as e:
        print(f"Error generating objects in batch: {e}")
        return []


def generate_object_names_multi_batch(target_count=500):
    """
    Generate object names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of objects to generate
    
    Returns:
        list: List of object names
    """
    print(f"Generating {target_count} diverse object names using multiple specialized prompts...")
    
    # Define different prompt templates for different object categories
    prompts = [
        {
            "name": "Balls & Sports Objects",
            "template": """Generate exactly {count} ball and sports object names.

Requirements:
- Only single-word object names (no spaces, hyphens, or compound words)
- Focus on balls and sports objects
- Include: ball, football, baseball, basketball, soccer_ball, tennis_ball
- NO brand names, NO duplicates

Return ONLY the object names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Action Figures & Dolls",
            "template": """Generate exactly {count} action figure and doll names.

Requirements:
- Only single-word object names (no spaces, hyphens, or compound words)
- Focus on action figures and dolls
- Include: doll, figure, action_figure, robot, stuffed_animal
- NO brand names, NO duplicates

Return ONLY the object names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Building Objects",
            "template": """Generate exactly {count} building object names.

Requirements:
- Only single-word object names (no spaces, hyphens, or compound words)
- Focus on building objects
- Include: block, brick, lego, building_block, puzzle_piece
- NO brand names, NO duplicates

Return ONLY the object names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Vehicle Objects",
            "template": """Generate exactly {count} vehicle object names.

Requirements:
- Only single-word object names (no spaces, hyphens, or compound words)
- Focus on vehicle objects
- Include: car, truck, airplane, helicopter, train, boat
- NO brand names, NO duplicates

Return ONLY the object names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Traditional & Classic Objects",
            "template": """Generate exactly {count} traditional and classic object names.

Requirements:
- Only single-word object names (no spaces, hyphens, or compound words)
- Focus on traditional and classic objects
- Include: top, yo_yo, kite, top, frisbee, jacks, marbles
- NO brand names, NO duplicates

Return ONLY the object names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_objects = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        objects = generate_object_names_batch(prompt_info['template'], batch_size)
        all_objects.extend(objects)
        print(f"Total objects so far: {len(all_objects)}")
    
    return all_objects


def filter_single_word_objects(objects):
    """
    Filter objects to ensure they are single words only.
    
    Args:
        objects (list): List of object names
    
    Returns:
        list: Filtered list of single-word objects
    """
    filtered = []
    for object in objects:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(object.split()) == 1 and '-' not in object and '_' not in object:
            filtered.append(object)
    
    return filtered


def save_object_list(objects, filename="list.json", merge_existing=True):
    """
    Save the objects list to a JSON file.
    
    Args:
        objects (list): List of object names
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
                existing_objects = json.load(f)
                # Combine and deduplicate
                all_objects = list(dict.fromkeys(existing_objects + objects))  # Preserves order
                objects = all_objects
                print(f"Merged with {len(existing_objects)} existing items")
            except json.JSONDecodeError:
                print("Could not read existing file, overwriting...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(objects, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save object names."""
    print("=== Enhanced Natural Object Name Generator ===")
    print("Generating 500+ diverse single-word object names using multiple specialized prompts...")
    print()
    
    # Generate objects using multiple specialized prompts
    objects = generate_object_names_multi_batch(target_count=500)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word objects only...")
    filtered_objects = filter_single_word_objects(objects)
    
    print(f"After filtering: {len(filtered_objects)} single-word objects")
    
    # Remove duplicates while preserving order
    unique_objects = []
    seen = set()
    for object in filtered_objects:
        if object not in seen:
            unique_objects.append(object)
            seen.add(object)
    
    print(f"After removing duplicates: {len(unique_objects)} unique objects")
    
    # Take the available items
    final_objects = unique_objects[:500]
    
    # Save to file
    filepath = save_object_list(final_objects)
    
    print(f"\n✓ Generated {len(final_objects)} common single-word object names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 objects:")
    for i, object in enumerate(final_objects[:20], 1):
        print(f"  {i:2d}. {object}")
    
    if len(final_objects) > 20:
        print(f"  ... and {len(final_objects) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(objects)}")
    print(f"  After filtering: {len(filtered_objects)}")
    print(f"  After deduplication: {len(unique_objects)}")
    print(f"  Final count: {len(final_objects)}")


if __name__ == "__main__":
    main()

