import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_mythical_creature_names_batch(prompt_template, count=200):
    """
    Generate a batch of mythical creature names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of mythical creatures to generate in this batch
    
    Returns:
        list: List of mythical creature names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        creatures = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    creatures.append(clean_name.lower())
        
        print(f"Generated {len(creatures)} mythical creatures from this batch")
        return creatures
        
    except Exception as e:
        print(f"Error generating mythical creatures in batch: {e}")
        return []


def generate_mythical_creature_names_multi_batch(target_count=1000):
    """
    Generate mythical creature names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of mythical creatures to generate
    
    Returns:
        list: List of mythical creature names
    """
    print(f"Generating {target_count} diverse mythical creature names using multiple specialized prompts...")
    
    # Define different prompt templates for different mythical creature categories
    prompts = [
        {
            "name": "Dragons & Serpents",
            "template": """Generate exactly {count} dragon and serpent mythical creature names.

Requirements:
- Only single-word creature names (no spaces, hyphens, or compound words)
- Focus on dragons and serpent-like creatures
- Include: dragon, wyvern, basilisk, hydra, naga, drake, wyrm, serpent, chimera, phoenix
- NO brand names, NO specific character names, NO duplicates
- Focus on dragon and serpent mythical creatures

Return ONLY the creature names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Magical Beasts",
            "template": """Generate exactly {count} magical beast mythical creature names.

Requirements:
- Only single-word creature names (no spaces, hyphens, or compound words)
- Focus on magical and fantastical beasts
- Include: unicorn, griffin, pegasus, centaur, minotaur, sphinx, manticore, hippogriff, kraken, leviathan
- NO brand names, NO specific character names, NO duplicates
- Focus on magical and fantastical beasts

Return ONLY the creature names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Elemental & Nature Spirits",
            "template": """Generate exactly {count} elemental and nature spirit mythical creature names.

Requirements:
- Only single-word creature names (no spaces, hyphens, or compound words)
- Focus on elemental and nature-based creatures
- Include: elemental, sprite, fairy, nymph, dryad, sylph, salamander, gnome, elf, dwarf
- NO brand names, NO specific character names, NO duplicates
- Focus on elemental and nature spirit creatures

Return ONLY the creature names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Undead & Dark Creatures",
            "template": """Generate exactly {count} undead and dark mythical creature names.

Requirements:
- Only single-word creature names (no spaces, hyphens, or compound words)
- Focus on undead and dark creatures
- Include: vampire, zombie, ghost, wraith, banshee, lich, skeleton, revenant, specter, shade
- NO brand names, NO specific character names, NO duplicates
- Focus on undead and dark mythical creatures

Return ONLY the creature names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Celestial & Divine Beings",
            "template": """Generate exactly {count} celestial and divine mythical creature names.

Requirements:
- Only single-word creature names (no spaces, hyphens, or compound words)
- Focus on celestial and divine beings
- Include: angel, demon, cherub, seraph, archangel, deity, god, goddess, titan, celestial
- NO brand names, NO specific character names, NO duplicates
- Focus on celestial and divine mythical beings

Return ONLY the creature names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Cultural & Folkloric Creatures",
            "template": """Generate exactly {count} cultural and folkloric mythical creature names.

Requirements:
- Only single-word creature names (no spaces, hyphens, or compound words)
- Focus on creatures from various cultures and folklore
- Include: troll, goblin, orc, elf, dwarf, giant, ogre, kobold, imp, pixie
- NO brand names, NO specific character names, NO duplicates
- Focus on cultural and folkloric mythical creatures

Return ONLY the creature names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_creatures = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        creatures = generate_mythical_creature_names_batch(prompt_info['template'], batch_size)
        all_creatures.extend(creatures)
        print(f"Total creatures so far: {len(all_creatures)}")
    
    return all_creatures


def filter_single_word_creatures(creatures):
    """
    Filter mythical creatures to ensure they are single words only.
    
    Args:
        creatures (list): List of mythical creature names
    
    Returns:
        list: Filtered list of single-word creatures
    """
    filtered = []
    for creature in creatures:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(creature.split()) == 1 and '-' not in creature and '_' not in creature:
            filtered.append(creature)
    
    return filtered


def save_creatures_list(creatures, filename="list.json"):
    """
    Save the mythical creatures list to a JSON file.
    
    Args:
        creatures (list): List of mythical creature names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(creatures, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save mythical creature names."""
    print("=== Enhanced Mythical Creature Name Generator ===")
    print("Generating 1000+ diverse single-word mythical creature names using multiple specialized prompts...")
    print()
    
    # Generate mythical creatures using multiple specialized prompts
    creatures = generate_mythical_creature_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word creatures only...")
    filtered_creatures = filter_single_word_creatures(creatures)
    
    print(f"After filtering: {len(filtered_creatures)} single-word creatures")
    
    # Remove duplicates while preserving order
    unique_creatures = []
    seen = set()
    for creature in filtered_creatures:
        if creature not in seen:
            unique_creatures.append(creature)
            seen.add(creature)
    
    print(f"After removing duplicates: {len(unique_creatures)} unique creatures")
    
    # Take exactly 1000 (or as many as we have)
    final_creatures = unique_creatures[:1000]
    
    # Save to file
    filepath = save_creatures_list(final_creatures)
    
    print(f"\n✓ Generated {len(final_creatures)} common single-word mythical creature names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 creatures:")
    for i, creature in enumerate(final_creatures[:20], 1):
        print(f"  {i:2d}. {creature}")
    
    if len(final_creatures) > 20:
        print(f"  ... and {len(final_creatures) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(creatures)}")
    print(f"  After filtering: {len(filtered_creatures)}")
    print(f"  After deduplication: {len(unique_creatures)}")
    print(f"  Final count: {len(final_creatures)}")


if __name__ == "__main__":
    main()
