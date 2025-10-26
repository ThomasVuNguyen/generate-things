import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_building_names_batch(prompt_template, count=200):
    """
    Generate a batch of building names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of buildings to generate in this batch
    
    Returns:
        list: List of building names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        buildings = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    buildings.append(clean_name.lower())
        
        print(f"Generated {len(buildings)} buildings from this batch")
        return buildings
        
    except Exception as e:
        print(f"Error generating buildings in batch: {e}")
        return []


def generate_building_names_multi_batch(target_count=1000):
    """
    Generate building names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of buildings to generate
    
    Returns:
        list: List of building names
    """
    print(f"Generating {target_count} diverse building names using multiple specialized prompts...")
    
    # Define different prompt templates for different building categories
    prompts = [
        {
            "name": "Residential Buildings",
            "template": """Generate exactly {count} residential building names.

Requirements:
- Only single-word building names (no spaces, hyphens, or compound words)
- Focus on types of residential buildings
- Include: house, mansion, cottage, apartment, condo, townhouse, villa, cabin, bungalow, duplex
- NO specific building names (like "Empire State"), NO brand names, NO duplicates
- Focus on building types and architectural styles

Return ONLY the building names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Commercial Buildings",
            "template": """Generate exactly {count} commercial building names.

Requirements:
- Only single-word building names (no spaces, hyphens, or compound words)
- Focus on types of commercial buildings
- Include: office, store, mall, restaurant, hotel, bank, warehouse, factory, market, plaza
- NO specific building names, NO brand names, NO duplicates
- Focus on building types and commercial structures

Return ONLY the building names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Public & Institutional Buildings",
            "template": """Generate exactly {count} public and institutional building names.

Requirements:
- Only single-word building names (no spaces, hyphens, or compound words)
- Focus on types of public and institutional buildings
- Include: school, hospital, library, museum, church, temple, mosque, courthouse, capitol, stadium
- NO specific building names, NO brand names, NO duplicates
- Focus on building types and public structures

Return ONLY the building names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Historical & Architectural Styles",
            "template": """Generate exactly {count} historical and architectural building names.

Requirements:
- Only single-word building names (no spaces, hyphens, or compound words)
- Focus on historical and architectural building types
- Include: castle, palace, fortress, cathedral, abbey, monastery, pagoda, pyramid, colosseum, amphitheater
- NO specific building names, NO brand names, NO duplicates
- Focus on historical building types and architectural styles

Return ONLY the building names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Modern & Contemporary Buildings",
            "template": """Generate exactly {count} modern and contemporary building names.

Requirements:
- Only single-word building names (no spaces, hyphens, or compound words)
- Focus on types of modern and contemporary buildings
- Include: skyscraper, tower, complex, center, hub, terminal, station, arena, theater, gallery
- NO specific building names, NO brand names, NO duplicates
- Focus on modern building types and contemporary structures

Return ONLY the building names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Infrastructure & Specialized Buildings",
            "template": """Generate exactly {count} infrastructure and specialized building names.

Requirements:
- Only single-word building names (no spaces, hyphens, or compound words)
- Focus on infrastructure and specialized building types
- Include: bridge, tunnel, dam, lighthouse, windmill, silo, barn, greenhouse, observatory, laboratory
- NO specific building names, NO brand names, NO duplicates
- Focus on infrastructure and specialized building types

Return ONLY the building names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_buildings = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        buildings = generate_building_names_batch(prompt_info['template'], batch_size)
        all_buildings.extend(buildings)
        print(f"Total buildings so far: {len(all_buildings)}")
    
    return all_buildings


def filter_single_word_buildings(buildings):
    """
    Filter buildings to ensure they are single words only.
    
    Args:
        buildings (list): List of building names
    
    Returns:
        list: Filtered list of single-word buildings
    """
    filtered = []
    for building in buildings:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(building.split()) == 1 and '-' not in building and '_' not in building:
            filtered.append(building)
    
    return filtered


def save_buildings_list(buildings, filename="list.json"):
    """
    Save the buildings list to a JSON file.
    
    Args:
        buildings (list): List of building names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(buildings, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save building names."""
    print("=== Enhanced Building Name Generator ===")
    print("Generating 1000+ diverse single-word building names using multiple specialized prompts...")
    print()
    
    # Generate buildings using multiple specialized prompts
    buildings = generate_building_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word buildings only...")
    filtered_buildings = filter_single_word_buildings(buildings)
    
    print(f"After filtering: {len(filtered_buildings)} single-word buildings")
    
    # Remove duplicates while preserving order
    unique_buildings = []
    seen = set()
    for building in filtered_buildings:
        if building not in seen:
            unique_buildings.append(building)
            seen.add(building)
    
    print(f"After removing duplicates: {len(unique_buildings)} unique buildings")
    
    # Take exactly 1000 (or as many as we have)
    final_buildings = unique_buildings[:1000]
    
    # Save to file
    filepath = save_buildings_list(final_buildings)
    
    print(f"\n✓ Generated {len(final_buildings)} common single-word building names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 buildings:")
    for i, building in enumerate(final_buildings[:20], 1):
        print(f"  {i:2d}. {building}")
    
    if len(final_buildings) > 20:
        print(f"  ... and {len(final_buildings) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(buildings)}")
    print(f"  After filtering: {len(filtered_buildings)}")
    print(f"  After deduplication: {len(unique_buildings)}")
    print(f"  Final count: {len(final_buildings)}")


if __name__ == "__main__":
    main()
