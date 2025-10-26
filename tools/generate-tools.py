import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_tool_names_batch(prompt_template, count=200):
    """
    Generate a batch of tool names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of tools to generate in this batch
    
    Returns:
        list: List of tool names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        tools = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    tools.append(clean_name.lower())
        
        print(f"Generated {len(tools)} tools from this batch")
        return tools
        
    except Exception as e:
        print(f"Error generating tools in batch: {e}")
        return []


def generate_tool_names_multi_batch(target_count=1000):
    """
    Generate tool names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of tools to generate
    
    Returns:
        list: List of tool names
    """
    print(f"Generating {target_count} diverse tool names using multiple specialized prompts...")
    
    # Define different prompt templates for different tool categories
    prompts = [
        {
            "name": "Hand Tools",
            "template": """Generate exactly {count} hand tool names.

Requirements:
- Only single-word tool names (no spaces, hyphens, or compound words)
- Focus on manual hand tools
- Include: hammer, screwdriver, wrench, pliers, saw, chisel, file, drill, level, square
- NO power tools, NO brand names, NO duplicates
- Focus on traditional hand-operated tools

Return ONLY the tool names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Power Tools",
            "template": """Generate exactly {count} power tool names.

Requirements:
- Only single-word tool names (no spaces, hyphens, or compound words)
- Focus on electric and power-operated tools
- Include: drill, saw, grinder, sander, router, planer, jigsaw, circular, reciprocating, impact
- NO brand names, NO model names, NO duplicates
- Focus on power-operated tools and equipment

Return ONLY the tool names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Measuring & Precision Tools",
            "template": """Generate exactly {count} measuring and precision tool names.

Requirements:
- Only single-word tool names (no spaces, hyphens, or compound words)
- Focus on measuring and precision instruments
- Include: ruler, tape, caliper, micrometer, protractor, compass, level, square, gauge, meter
- NO brand names, NO model names, NO duplicates
- Focus on measurement and precision tools

Return ONLY the tool names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Gardening & Outdoor Tools",
            "template": """Generate exactly {count} gardening and outdoor tool names.

Requirements:
- Only single-word tool names (no spaces, hyphens, or compound words)
- Focus on gardening and outdoor work tools
- Include: shovel, rake, hoe, pruner, trowel, spade, fork, shears, cultivator, edger
- NO brand names, NO model names, NO duplicates
- Focus on gardening and outdoor work tools

Return ONLY the tool names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Medical & Scientific Tools",
            "template": """Generate exactly {count} medical and scientific tool names.

Requirements:
- Only single-word tool names (no spaces, hyphens, or compound words)
- Focus on medical and scientific instruments
- Include: scalpel, forceps, microscope, stethoscope, syringe, thermometer, pipette, centrifuge, spectrometer, telescope
- NO brand names, NO model names, NO duplicates
- Focus on medical and scientific instruments

Return ONLY the tool names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Craft & Specialty Tools",
            "template": """Generate exactly {count} craft and specialty tool names.

Requirements:
- Only single-word tool names (no spaces, hyphens, or compound words)
- Focus on craft and specialty tools
- Include: brush, palette, easel, loom, lathe, forge, anvil, mold, press, cutter
- NO brand names, NO model names, NO duplicates
- Focus on craft and specialty tools

Return ONLY the tool names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_tools = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        tools = generate_tool_names_batch(prompt_info['template'], batch_size)
        all_tools.extend(tools)
        print(f"Total tools so far: {len(all_tools)}")
    
    return all_tools


def filter_single_word_tools(tools):
    """
    Filter tools to ensure they are single words only.
    
    Args:
        tools (list): List of tool names
    
    Returns:
        list: Filtered list of single-word tools
    """
    filtered = []
    for tool in tools:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(tool.split()) == 1 and '-' not in tool and '_' not in tool:
            filtered.append(tool)
    
    return filtered


def save_tools_list(tools, filename="list.json"):
    """
    Save the tools list to a JSON file.
    
    Args:
        tools (list): List of tool names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(tools, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save tool names."""
    print("=== Enhanced Tool Name Generator ===")
    print("Generating 1000+ diverse single-word tool names using multiple specialized prompts...")
    print()
    
    # Generate tools using multiple specialized prompts
    tools = generate_tool_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word tools only...")
    filtered_tools = filter_single_word_tools(tools)
    
    print(f"After filtering: {len(filtered_tools)} single-word tools")
    
    # Remove duplicates while preserving order
    unique_tools = []
    seen = set()
    for tool in filtered_tools:
        if tool not in seen:
            unique_tools.append(tool)
            seen.add(tool)
    
    print(f"After removing duplicates: {len(unique_tools)} unique tools")
    
    # Take exactly 1000 (or as many as we have)
    final_tools = unique_tools[:1000]
    
    # Save to file
    filepath = save_tools_list(final_tools)
    
    print(f"\n✓ Generated {len(final_tools)} common single-word tool names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 tools:")
    for i, tool in enumerate(final_tools[:20], 1):
        print(f"  {i:2d}. {tool}")
    
    if len(final_tools) > 20:
        print(f"  ... and {len(final_tools) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(tools)}")
    print(f"  After filtering: {len(filtered_tools)}")
    print(f"  After deduplication: {len(unique_tools)}")
    print(f"  Final count: {len(final_tools)}")


if __name__ == "__main__":
    main()
