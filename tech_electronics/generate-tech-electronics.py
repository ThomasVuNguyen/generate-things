import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_tech_names_batch(prompt_template, count=200):
    """
    Generate a batch of tech/electronics names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of tech items to generate in this batch
    
    Returns:
        list: List of tech/electronics names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        tech_items = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    tech_items.append(clean_name.lower())
        
        print(f"Generated {len(tech_items)} tech items from this batch")
        return tech_items
        
    except Exception as e:
        print(f"Error generating tech items in batch: {e}")
        return []


def generate_tech_names_multi_batch(target_count=1000):
    """
    Generate tech/electronics names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of tech items to generate
    
    Returns:
        list: List of tech/electronics names
    """
    print(f"Generating {target_count} diverse tech/electronics names using multiple specialized prompts...")
    
    # Define different prompt templates for different tech categories
    prompts = [
        {
            "name": "Computers & Devices",
            "template": """Generate exactly {count} computer and device names.

Requirements:
- Only single-word tech names (no spaces, hyphens, or compound words)
- Focus on computers and computing devices
- Include: computer, laptop, tablet, desktop, server, workstation, terminal, mainframe, minicomputer, microcomputer
- NO brand names, NO model names, NO duplicates
- Focus on computer and computing device types

Return ONLY the tech names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Mobile & Communication",
            "template": """Generate exactly {count} mobile and communication device names.

Requirements:
- Only single-word tech names (no spaces, hyphens, or compound words)
- Focus on mobile and communication devices
- Include: phone, smartphone, tablet, pager, walkie, radio, transmitter, receiver, modem, router
- NO brand names, NO model names, NO duplicates
- Focus on mobile and communication device types

Return ONLY the tech names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Audio & Video Equipment",
            "template": """Generate exactly {count} audio and video equipment names.

Requirements:
- Only single-word tech names (no spaces, hyphens, or compound words)
- Focus on audio and video devices
- Include: speaker, microphone, camera, recorder, player, amplifier, mixer, monitor, projector, display
- NO brand names, NO model names, NO duplicates
- Focus on audio and video equipment types

Return ONLY the tech names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Gaming & Entertainment",
            "template": """Generate exactly {count} gaming and entertainment device names.

Requirements:
- Only single-word tech names (no spaces, hyphens, or compound words)
- Focus on gaming and entertainment devices
- Include: console, controller, joystick, headset, keyboard, mouse, gamepad, arcade, pinball, slot
- NO brand names, NO model names, NO duplicates
- Focus on gaming and entertainment device types

Return ONLY the tech names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Networking & Connectivity",
            "template": """Generate exactly {count} networking and connectivity device names.

Requirements:
- Only single-word tech names (no spaces, hyphens, or compound words)
- Focus on networking and connectivity devices
- Include: router, switch, hub, bridge, gateway, firewall, repeater, extender, adapter, converter
- NO brand names, NO model names, NO duplicates
- Focus on networking and connectivity device types

Return ONLY the tech names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Storage & Peripherals",
            "template": """Generate exactly {count} storage and peripheral device names.

Requirements:
- Only single-word tech names (no spaces, hyphens, or compound words)
- Focus on storage and peripheral devices
- Include: drive, disk, memory, storage, printer, scanner, copier, fax, backup, archive
- NO brand names, NO model names, NO duplicates
- Focus on storage and peripheral device types

Return ONLY the tech names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_tech_items = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        tech_items = generate_tech_names_batch(prompt_info['template'], batch_size)
        all_tech_items.extend(tech_items)
        print(f"Total tech items so far: {len(all_tech_items)}")
    
    return all_tech_items


def filter_single_word_tech_items(tech_items):
    """
    Filter tech items to ensure they are single words only.
    
    Args:
        tech_items (list): List of tech/electronics names
    
    Returns:
        list: Filtered list of single-word tech items
    """
    filtered = []
    for tech_item in tech_items:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(tech_item.split()) == 1 and '-' not in tech_item and '_' not in tech_item:
            filtered.append(tech_item)
    
    return filtered


def save_tech_items_list(tech_items, filename="list.json"):
    """
    Save the tech items list to a JSON file.
    
    Args:
        tech_items (list): List of tech/electronics names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(tech_items, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save tech/electronics names."""
    print("=== Enhanced Tech & Electronics Name Generator ===")
    print("Generating 1000+ diverse single-word tech/electronics names using multiple specialized prompts...")
    print()
    
    # Generate tech items using multiple specialized prompts
    tech_items = generate_tech_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word tech items only...")
    filtered_tech_items = filter_single_word_tech_items(tech_items)
    
    print(f"After filtering: {len(filtered_tech_items)} single-word tech items")
    
    # Remove duplicates while preserving order
    unique_tech_items = []
    seen = set()
    for tech_item in filtered_tech_items:
        if tech_item not in seen:
            unique_tech_items.append(tech_item)
            seen.add(tech_item)
    
    print(f"After removing duplicates: {len(unique_tech_items)} unique tech items")
    
    # Take exactly 1000 (or as many as we have)
    final_tech_items = unique_tech_items[:1000]
    
    # Save to file
    filepath = save_tech_items_list(final_tech_items)
    
    print(f"\n✓ Generated {len(final_tech_items)} common single-word tech/electronics names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 tech items:")
    for i, tech_item in enumerate(final_tech_items[:20], 1):
        print(f"  {i:2d}. {tech_item}")
    
    if len(final_tech_items) > 20:
        print(f"  ... and {len(final_tech_items) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(tech_items)}")
    print(f"  After filtering: {len(filtered_tech_items)}")
    print(f"  After deduplication: {len(unique_tech_items)}")
    print(f"  Final count: {len(final_tech_items)}")


if __name__ == "__main__":
    main()
