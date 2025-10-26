import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_artifact_names_batch(prompt_template, count=200):
    """
    Generate a batch of historical artifact names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of artifacts to generate in this batch
    
    Returns:
        list: List of historical artifact names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        artifacts = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    artifacts.append(clean_name.lower())
        
        print(f"Generated {len(artifacts)} artifacts from this batch")
        return artifacts
        
    except Exception as e:
        print(f"Error generating artifacts in batch: {e}")
        return []


def generate_artifact_names_multi_batch(target_count=1000):
    """
    Generate historical artifact names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of artifacts to generate
    
    Returns:
        list: List of historical artifact names
    """
    print(f"Generating {target_count} diverse historical artifact names using multiple specialized prompts...")
    
    # Define different prompt templates for different artifact categories
    prompts = [
        {
            "name": "Ancient Weapons & Armor",
            "template": """Generate exactly {count} ancient weapon and armor artifact names.

Requirements:
- Only single-word artifact names (no spaces, hyphens, or compound words)
- Focus on ancient weapons and armor
- Include: sword, shield, spear, bow, arrow, helmet, armor, dagger, axe, mace
- NO brand names, NO specific historical names, NO duplicates
- Focus on ancient weapon and armor types

Return ONLY the artifact names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Pottery & Ceramics",
            "template": """Generate exactly {count} pottery and ceramic artifact names.

Requirements:
- Only single-word artifact names (no spaces, hyphens, or compound words)
- Focus on pottery and ceramic artifacts
- Include: vase, urn, bowl, cup, plate, jar, pot, amphora, krater, kylix
- NO brand names, NO specific historical names, NO duplicates
- Focus on pottery and ceramic artifact types

Return ONLY the artifact names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Jewelry & Ornaments",
            "template": """Generate exactly {count} jewelry and ornament artifact names.

Requirements:
- Only single-word artifact names (no spaces, hyphens, or compound words)
- Focus on jewelry and ornamental artifacts
- Include: ring, necklace, bracelet, earring, pendant, brooch, crown, tiara, amulet, talisman
- NO brand names, NO specific historical names, NO duplicates
- Focus on jewelry and ornament artifact types

Return ONLY the artifact names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Religious & Ceremonial Objects",
            "template": """Generate exactly {count} religious and ceremonial artifact names.

Requirements:
- Only single-word artifact names (no spaces, hyphens, or compound words)
- Focus on religious and ceremonial artifacts
- Include: altar, shrine, temple, statue, idol, relic, cross, rosary, censer, chalice
- NO brand names, NO specific historical names, NO duplicates
- Focus on religious and ceremonial artifact types

Return ONLY the artifact names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Tools & Implements",
            "template": """Generate exactly {count} tool and implement artifact names.

Requirements:
- Only single-word artifact names (no spaces, hyphens, or compound words)
- Focus on historical tools and implements
- Include: hammer, chisel, saw, drill, awl, needle, loom, spindle, quern, mortar
- NO brand names, NO specific historical names, NO duplicates
- Focus on historical tool and implement types

Return ONLY the artifact names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Manuscripts & Documents",
            "template": """Generate exactly {count} manuscript and document artifact names.

Requirements:
- Only single-word artifact names (no spaces, hyphens, or compound words)
- Focus on manuscripts and document artifacts
- Include: scroll, codex, manuscript, tablet, papyrus, parchment, vellum, charter, deed, writ
- NO brand names, NO specific historical names, NO duplicates
- Focus on manuscript and document artifact types

Return ONLY the artifact names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_artifacts = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        artifacts = generate_artifact_names_batch(prompt_info['template'], batch_size)
        all_artifacts.extend(artifacts)
        print(f"Total artifacts so far: {len(all_artifacts)}")
    
    return all_artifacts


def filter_single_word_artifacts(artifacts):
    """
    Filter historical artifacts to ensure they are single words only.
    
    Args:
        artifacts (list): List of historical artifact names
    
    Returns:
        list: Filtered list of single-word artifacts
    """
    filtered = []
    for artifact in artifacts:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(artifact.split()) == 1 and '-' not in artifact and '_' not in artifact:
            filtered.append(artifact)
    
    return filtered


def save_artifacts_list(artifacts, filename="list.json"):
    """
    Save the historical artifacts list to a JSON file.
    
    Args:
        artifacts (list): List of historical artifact names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(artifacts, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save historical artifact names."""
    print("=== Enhanced Historical Artifact Name Generator ===")
    print("Generating 1000+ diverse single-word historical artifact names using multiple specialized prompts...")
    print()
    
    # Generate artifacts using multiple specialized prompts
    artifacts = generate_artifact_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word artifacts only...")
    filtered_artifacts = filter_single_word_artifacts(artifacts)
    
    print(f"After filtering: {len(filtered_artifacts)} single-word artifacts")
    
    # Remove duplicates while preserving order
    unique_artifacts = []
    seen = set()
    for artifact in filtered_artifacts:
        if artifact not in seen:
            unique_artifacts.append(artifact)
            seen.add(artifact)
    
    print(f"After removing duplicates: {len(unique_artifacts)} unique artifacts")
    
    # Take exactly 1000 (or as many as we have)
    final_artifacts = unique_artifacts[:1000]
    
    # Save to file
    filepath = save_artifacts_list(final_artifacts)
    
    print(f"\n✓ Generated {len(final_artifacts)} common single-word historical artifact names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 artifacts:")
    for i, artifact in enumerate(final_artifacts[:20], 1):
        print(f"  {i:2d}. {artifact}")
    
    if len(final_artifacts) > 20:
        print(f"  ... and {len(final_artifacts) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(artifacts)}")
    print(f"  After filtering: {len(filtered_artifacts)}")
    print(f"  After deduplication: {len(unique_artifacts)}")
    print(f"  Final count: {len(final_artifacts)}")


if __name__ == "__main__":
    main()
