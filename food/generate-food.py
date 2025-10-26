import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_food_names_batch(prompt_template, count=200):
    """
    Generate a batch of food names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of foods to generate in this batch
    
    Returns:
        list: List of food names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        foods = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    foods.append(clean_name.lower())
        
        print(f"Generated {len(foods)} foods from this batch")
        return foods
        
    except Exception as e:
        print(f"Error generating foods in batch: {e}")
        return []


def generate_food_names_multi_batch(target_count=1000):
    """
    Generate food names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of foods to generate
    
    Returns:
        list: List of food names
    """
    print(f"Generating {target_count} diverse food names using multiple specialized prompts...")
    
    # Define different prompt templates for different food categories
    prompts = [
        {
            "name": "Main Dishes & Proteins",
            "template": """Generate exactly {count} main dish and protein food names.

Requirements:
- Only single-word food names (no spaces, hyphens, or compound words)
- Focus on main dishes and protein foods
- Include: steak, chicken, fish, pork, beef, lamb, turkey, duck, salmon, tuna
- NO brand names, NO specific dish names, NO duplicates
- Focus on main dish and protein food types

Return ONLY the food names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Grains & Starches",
            "template": """Generate exactly {count} grain and starch food names.

Requirements:
- Only single-word food names (no spaces, hyphens, or compound words)
- Focus on grains and starches
- Include: rice, wheat, barley, oats, corn, potato, pasta, bread, quinoa, millet
- NO brand names, NO specific dish names, NO duplicates
- Focus on grain and starch food types

Return ONLY the food names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Vegetables & Legumes",
            "template": """Generate exactly {count} vegetable and legume food names.

Requirements:
- Only single-word food names (no spaces, hyphens, or compound words)
- Focus on vegetables and legumes
- Include: carrot, broccoli, spinach, bean, pea, lentil, onion, garlic, pepper, tomato
- NO brand names, NO specific dish names, NO duplicates
- Focus on vegetable and legume food types

Return ONLY the food names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Dairy & Eggs",
            "template": """Generate exactly {count} dairy and egg food names.

Requirements:
- Only single-word food names (no spaces, hyphens, or compound words)
- Focus on dairy and egg products
- Include: milk, cheese, butter, yogurt, cream, egg, curd, whey, casein, lactose
- NO brand names, NO specific dish names, NO duplicates
- Focus on dairy and egg food types

Return ONLY the food names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Desserts & Sweets",
            "template": """Generate exactly {count} dessert and sweet food names.

Requirements:
- Only single-word food names (no spaces, hyphens, or compound words)
- Focus on desserts and sweet foods
- Include: cake, pie, cookie, candy, chocolate, ice, cream, pudding, tart, muffin
- NO brand names, NO specific dish names, NO duplicates
- Focus on dessert and sweet food types

Return ONLY the food names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Beverages & Drinks",
            "template": """Generate exactly {count} beverage and drink names.

Requirements:
- Only single-word drink names (no spaces, hyphens, or compound words)
- Focus on beverages and drinks
- Include: water, juice, tea, coffee, soda, beer, wine, milk, cider, ale
- NO brand names, NO specific drink names, NO duplicates
- Focus on beverage and drink types

Return ONLY the drink names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_foods = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        foods = generate_food_names_batch(prompt_info['template'], batch_size)
        all_foods.extend(foods)
        print(f"Total foods so far: {len(all_foods)}")
    
    return all_foods


def filter_single_word_foods(foods):
    """
    Filter foods to ensure they are single words only.
    
    Args:
        foods (list): List of food names
    
    Returns:
        list: Filtered list of single-word foods
    """
    filtered = []
    for food in foods:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(food.split()) == 1 and '-' not in food and '_' not in food:
            filtered.append(food)
    
    return filtered


def save_foods_list(foods, filename="list.json"):
    """
    Save the foods list to a JSON file.
    
    Args:
        foods (list): List of food names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(foods, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save food names."""
    print("=== Enhanced Food Name Generator ===")
    print("Generating 1000+ diverse single-word food names using multiple specialized prompts...")
    print()
    
    # Generate foods using multiple specialized prompts
    foods = generate_food_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word foods only...")
    filtered_foods = filter_single_word_foods(foods)
    
    print(f"After filtering: {len(filtered_foods)} single-word foods")
    
    # Remove duplicates while preserving order
    unique_foods = []
    seen = set()
    for food in filtered_foods:
        if food not in seen:
            unique_foods.append(food)
            seen.add(food)
    
    print(f"After removing duplicates: {len(unique_foods)} unique foods")
    
    # Take exactly 1000 (or as many as we have)
    final_foods = unique_foods[:1000]
    
    # Save to file
    filepath = save_foods_list(final_foods)
    
    print(f"\n✓ Generated {len(final_foods)} common single-word food names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 foods:")
    for i, food in enumerate(final_foods[:20], 1):
        print(f"  {i:2d}. {food}")
    
    if len(final_foods) > 20:
        print(f"  ... and {len(final_foods) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(foods)}")
    print(f"  After filtering: {len(filtered_foods)}")
    print(f"  After deduplication: {len(unique_foods)}")
    print(f"  Final count: {len(final_foods)}")


if __name__ == "__main__":
    main()
