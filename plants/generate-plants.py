import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_plant_names_batch(prompt_template, count=100):
    """
    Generate a batch of plant names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of plants to generate in this batch
    
    Returns:
        list: List of plant names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        plants = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    plants.append(clean_name.lower())
        
        print(f"Generated {len(plants)} plants from this batch")
        return plants
        
    except Exception as e:
        print(f"Error generating plants in batch: {e}")
        return []


def generate_plant_names_multi_batch(target_count=500):
    """
    Generate plant names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of plants to generate
    
    Returns:
        list: List of plant names
    """
    print(f"Generating {target_count} diverse plant names using multiple specialized prompts...")
    
    # Define different prompt templates for different plant categories
    prompts = [
        {
            "name": "Houseplants & Indoor Plants",
            "template": """Generate exactly {count} houseplant and indoor plant names.

Requirements:
- Only single-word plant names (no spaces, hyphens, or compound words)
- Focus on houseplants and indoor plants
- Include: aloe, fern, ivy, jade, pothos, spider_plant, snake_plant
- NO scientific names, NO duplicates

Return ONLY the plant names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Trees & Large Plants",
            "template": """Generate exactly {count} tree and large plant names.

Requirements:
- Only single-word plant names (no spaces, hyphens, or compound words)
- Focus on trees and large plants
- Include: oak, maple, pine, willow, birch, elm, ash, cherry, apple_tree
- NO scientific names, NO duplicates

Return ONLY the plant names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Flowers & Flowering Plants",
            "template": """Generate exactly {count} flower and flowering plant names.

Requirements:
- Only single-word plant names (no spaces, hyphens, or compound words)
- Focus on flowers and flowering plants
- Include: rose, daisy, tulip, lily, orchid, daffodil, sunflower
- NO scientific names, NO duplicates

Return ONLY the plant names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Herbs & Spices",
            "template": """Generate exactly {count} herb and spice plant names.

Requirements:
- Only single-word plant names (no spaces, hyphens, or compound words)
- Focus on herbs and spices
- Include: basil, mint, thyme, oregano, rosemary, sage, parsley
- NO scientific names, NO duplicates

Return ONLY the plant names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Succulents & Cacti",
            "template": """Generate exactly {count} succulent and cactus names.

Requirements:
- Only single-word plant names (no spaces, hyphens, or compound words)
- Focus on succulents and cacti
- Include: aloe, jade, echeveria, haworthia, sedum, cactus
- NO scientific names, NO duplicates

Return ONLY the plant names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_plants = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        plants = generate_plant_names_batch(prompt_info['template'], batch_size)
        all_plants.extend(plants)
        print(f"Total plants so far: {len(all_plants)}")
    
    return all_plants


def filter_single_word_plants(plants):
    """
    Filter plants to ensure they are single words only.
    
    Args:
        plants (list): List of plant names
    
    Returns:
        list: Filtered list of single-word plants
    """
    filtered = []
    for plant in plants:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(plant.split()) == 1 and '-' not in plant and '_' not in plant:
            filtered.append(plant)
    
    return filtered


def save_plants_list(plants, filename="list.json"):
    """
    Save the plants list to a JSON file.
    
    Args:
        plants (list): List of plant names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(plants, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save plant names."""
    print("=== Enhanced Plant Name Generator ===")
    print("Generating 500+ diverse single-word plant names using multiple specialized prompts...")
    print()
    
    # Generate plants using multiple specialized prompts
    plants = generate_plant_names_multi_batch(target_count=500)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word plants only...")
    filtered_plants = filter_single_word_plants(plants)
    
    print(f"After filtering: {len(filtered_plants)} single-word plants")
    
    # Remove duplicates while preserving order
    unique_plants = []
    seen = set()
    for plant in filtered_plants:
        if plant not in seen:
            unique_plants.append(plant)
            seen.add(plant)
    
    print(f"After removing duplicates: {len(unique_plants)} unique plants")
    
    # Take the available items
    final_plants = unique_plants[:500]
    
    # Save to file
    filepath = save_plants_list(final_plants)
    
    print(f"\n✓ Generated {len(final_plants)} common single-word plant names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 plants:")
    for i, plant in enumerate(final_plants[:20], 1):
        print(f"  {i:2d}. {plant}")
    
    if len(final_plants) > 20:
        print(f"  ... and {len(final_plants) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(plants)}")
    print(f"  After filtering: {len(filtered_plants)}")
    print(f"  After deduplication: {len(unique_plants)}")
    print(f"  Final count: {len(final_plants)}")


if __name__ == "__main__":
    main()

