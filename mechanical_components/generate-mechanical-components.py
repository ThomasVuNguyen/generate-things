import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_mechanical_names_batch(prompt_template, count=100):
    """
    Generate a batch of mechanical component names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of mechanical components to generate in this batch
    
    Returns:
        list: List of mechanical component names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        components = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    components.append(clean_name.lower())
        
        print(f"Generated {len(components)} mechanical components from this batch")
        return components
        
    except Exception as e:
        print(f"Error generating mechanical components in batch: {e}")
        return []


def generate_mechanical_names_multi_batch(target_count=500):
    """
    Generate mechanical component names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of mechanical components to generate
    
    Returns:
        list: List of mechanical component names
    """
    print(f"Generating {target_count} diverse mechanical component names using multiple specialized prompts...")
    
    # Define different prompt templates for different mechanical component categories
    prompts = [
        {
            "name": "Gears & Transmissions",
            "template": """Generate exactly {count} gear and transmission component names.

Requirements:
- Only single-word mechanical component names (no spaces, hyphens, or compound words)
- Focus on gears and transmission components
- Include: gear, sprocket, pulley, cam, crankshaft, bearing
- NO brand names, NO duplicates

Return ONLY the component names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Fasteners & Hardware",
            "template": """Generate exactly {count} fastener and hardware component names.

Requirements:
- Only single-word mechanical component names (no spaces, hyphens, or compound words)
- Focus on fasteners and hardware
- Include: bolt, nut, screw, rivet, washer, clip, pin
- NO brand names, NO duplicates

Return ONLY the component names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Moving Parts & Springs",
            "template": """Generate exactly {count} moving part and spring component names.

Requirements:
- Only single-word mechanical component names (no spaces, hyphens, or compound words)
- Focus on moving parts and springs
- Include: spring, piston, valve, rod, actuator
- NO brand names, NO duplicates

Return ONLY the component names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Structural & Support Components",
            "template": """Generate exactly {count} structural and support component names.

Requirements:
- Only single-word mechanical component names (no spaces, hyphens, or compound words)
- Focus on structural and support components
- Include: bracket, beam, plate, flange, spacer, bushing
- NO brand names, NO duplicates

Return ONLY the component names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Connectors & Joints",
            "template": """Generate exactly {count} connector and joint component names.

Requirements:
- Only single-word mechanical component names (no spaces, hyphens, or compound words)
- Focus on connectors and joints
- Include: coupling, adapter, joint, clamp, connector, coupling
- NO brand names, NO duplicates

Return ONLY the component names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_components = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        components = generate_mechanical_names_batch(prompt_info['template'], batch_size)
        all_components.extend(components)
        print(f"Total mechanical components so far: {len(all_components)}")
    
    return all_components


def filter_single_word_components(components):
    """
    Filter mechanical components to ensure they are single words only.
    
    Args:
        components (list): List of component names
    
    Returns:
        list: Filtered list of single-word components
    """
    filtered = []
    for component in components:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(component.split()) == 1 and '-' not in component and '_' not in component:
            filtered.append(component)
    
    return filtered


def save_components_list(components, filename="list.json"):
    """
    Save the components list to a JSON file.
    
    Args:
        components (list): List of component names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(components, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save mechanical component names."""
    print("=== Enhanced Mechanical Component Name Generator ===")
    print("Generating 500+ diverse single-word mechanical component names using multiple specialized prompts...")
    print()
    
    # Generate components using multiple specialized prompts
    components = generate_mechanical_names_multi_batch(target_count=500)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word components only...")
    filtered_components = filter_single_word_components(components)
    
    print(f"After filtering: {len(filtered_components)} single-word components")
    
    # Remove duplicates while preserving order
    unique_components = []
    seen = set()
    for component in filtered_components:
        if component not in seen:
            unique_components.append(component)
            seen.add(component)
    
    print(f"After removing duplicates: {len(unique_components)} unique components")
    
    # Take the available items
    final_components = unique_components[:500]
    
    # Save to file
    filepath = save_components_list(final_components)
    
    print(f"\n✓ Generated {len(final_components)} common single-word mechanical component names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 components:")
    for i, component in enumerate(final_components[:20], 1):
        print(f"  {i:2d}. {component}")
    
    if len(final_components) > 20:
        print(f"  ... and {len(final_components) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(components)}")
    print(f"  After filtering: {len(filtered_components)}")
    print(f"  After deduplication: {len(unique_components)}")
    print(f"  Final count: {len(final_components)}")


if __name__ == "__main__":
    main()

