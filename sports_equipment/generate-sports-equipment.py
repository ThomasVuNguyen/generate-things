import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_sports_equipment_names_batch(prompt_template, count=100):
    """Generate a batch of sports equipment names."""
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        items = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:
                    items.append(clean_name.lower())
        
        print(f"Generated {len(items)} items from this batch")
        return items
        
    except Exception as e:
        print(f"Error generating items in batch: {e}")
        return []


def generate_sports_equipment_names_multi_batch(target_count=500):
    """Generate sports equipment names using multiple specialized prompts."""
    print(f"Generating {target_count} diverse sports equipment names...")
    
    prompts = [
        ("Ball Sports Equipment", """Generate exactly {count} ball sports equipment names. Include: basketball, football, soccer_ball, baseball, tennis_ball. NO brand names, NO duplicates. Return ONLY the names, one per line."""),
        ("Racquet Sports Equipment", """Generate exactly {count} racquet sports equipment names. Include: tennis_racket, badminton_racket, squash_racket, paddle. NO brand names, NO duplicates. Return ONLY the names, one per line."""),
        ("Protective Gear", """Generate exactly {count} protective sports gear names. Include: helmet, padding, guard, protector. NO brand names, NO duplicates. Return ONLY the names, one per line."""),
        ("Winter Sports Equipment", """Generate exactly {count} winter sports equipment names. Include: ski, snowboard, skate, sled. NO brand names, NO duplicates. Return ONLY the names, one per line."""),
        ("Water Sports Equipment", """Generate exactly {count} water sports equipment names. Include: paddle, board, fin, snorkel. NO brand names, NO duplicates. Return ONLY the names, one per line.""")
    ]
    
    all_items = []
    batch_size = max(50, target_count // len(prompts))
    
    for i, (name, template) in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {name}")
        items = generate_sports_equipment_names_batch(template, batch_size)
        all_items.extend(items)
        print(f"Total items so far: {len(all_items)}")
    
    return all_items


def filter_single_word_items(items):
    """Filter items to ensure they are single words only."""
    filtered = []
    for item in items:
        if len(item.split()) == 1 and '-' not in item and '_' not in item:
            filtered.append(item)
    return filtered


def save_sports_equipment_list(items, filename="list.json", merge_existing=True):
    """Save the items list to a JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    if merge_existing and os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing_items = json.load(f)
                all_items = list(dict.fromkeys(existing_items + items))
                items = all_items
                print(f"Merged with {len(existing_items)} existing items")
            except json.JSONDecodeError:
                print("Could not read existing file, overwriting...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    print("=== Sports Equipment Name Generator ===")
    print("Generating 500+ diverse single-word sports equipment names...")
    print()
    
    items = generate_sports_equipment_names_multi_batch(target_count=500)
    
    print(f"\nFiltering to single-word items only...")
    filtered_items = filter_single_word_items(items)
    print(f"After filtering: {len(filtered_items)} single-word items")
    
    unique_items = []
    seen = set()
    for item in filtered_items:
        if item not in seen:
            unique_items.append(item)
            seen.add(item)
    
    print(f"After removing duplicates: {len(unique_items)} unique items")
    
    final_items = unique_items[:500]
    filepath = save_sports_equipment_list(final_items)
    
    print(f"\n✓ Generated {len(final_items)} sports equipment names")
    print(f"✓ Saved to: {filepath}")
    print(f"\nFirst 20 items:")
    for i, item in enumerate(final_items[:20], 1):
        print(f"  {i:2d}. {item}")


if __name__ == "__main__":
    main()

