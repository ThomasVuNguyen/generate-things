import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_kitchen_appliance_names_batch(prompt_template, count=100):
    """Generate a batch of kitchen appliance names."""
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        appliances = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:
                    appliances.append(clean_name.lower())
        
        print(f"Generated {len(appliances)} appliances from this batch")
        return appliances
        
    except Exception as e:
        print(f"Error generating appliances in batch: {e}")
        return []


def generate_kitchen_appliance_names_multi_batch(target_count=500):
    """Generate kitchen appliance names using multiple prompts."""
    print(f"Generating {target_count} diverse kitchen appliance names...")
    
    prompts = [
        ("Food Prep Appliances", """Generate exactly {count} food prep appliance names. Include: blender, food_processor, mixer, juicer. NO brand names, NO duplicates. Return ONLY the names, one per line."""),
        ("Cooking Appliances", """Generate exactly {count} cooking appliance names. Include: stove, oven, grill, fryer. NO brand names, NO duplicates. Return ONLY the names, one per line."""),
        ("Beverage Appliances", """Generate exactly {count} beverage appliance names. Include: coffee_maker, kettle, juicer. NO brand names, NO duplicates. Return ONLY the names, one per line."""),
        ("Heating Appliances", """Generate exactly {count} heating appliance names. Include: toaster, microwave, heater. NO brand names, NO duplicates. Return ONLY the names, one per line."""),
        ("Storage Appliances", """Generate exactly {count} storage appliance names. Include: refrigerator, freezer, warmer. NO brand names, NO duplicates. Return ONLY the names, one per line.""")
    ]
    
    all_appliances = []
    batch_size = max(50, target_count // len(prompts))
    
    for i, (name, template) in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {name}")
        appliances = generate_kitchen_appliance_names_batch(template, batch_size)
        all_appliances.extend(appliances)
        print(f"Total appliances so far: {len(all_appliances)}")
    
    return all_appliances


def filter_single_word_appliances(appliances):
    """Filter appliances to ensure they are single words only."""
    filtered = []
    for appliance in appliances:
        if len(appliance.split()) == 1 and '-' not in appliance and '_' not in appliance:
            filtered.append(appliance)
    return filtered


def save_kitchen_appliance_list(appliances, filename="list.json", merge_existing=True):
    """Save the appliances list to a JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    if merge_existing and os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing_appliances = json.load(f)
                all_appliances = list(dict.fromkeys(existing_appliances + appliances))
                appliances = all_appliances
                print(f"Merged with {len(existing_appliances)} existing items")
            except json.JSONDecodeError:
                print("Could not read existing file, overwriting...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(appliances, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    print("=== Kitchen Appliance Name Generator ===")
    print("Generating 500+ diverse single-word kitchen appliance names...")
    print()
    
    appliances = generate_kitchen_appliance_names_multi_batch(target_count=500)
    
    print(f"\nFiltering to single-word appliances only...")
    filtered_appliances = filter_single_word_appliances(appliances)
    print(f"After filtering: {len(filtered_appliances)} single-word appliances")
    
    unique_appliances = []
    seen = set()
    for appliance in filtered_appliances:
        if appliance not in seen:
            unique_appliances.append(appliance)
            seen.add(appliance)
    
    print(f"After removing duplicates: {len(unique_appliances)} unique appliances")
    
    final_appliances = unique_appliances[:500]
    filepath = save_kitchen_appliance_list(final_appliances)
    
    print(f"\n✓ Generated {len(final_appliances)} kitchen appliance names")
    print(f"✓ Saved to: {filepath}")
    print(f"\nFirst 20 appliances:")
    for i, appliance in enumerate(final_appliances[:20], 1):
        print(f"  {i:2d}. {appliance}")


if __name__ == "__main__":
    main()
