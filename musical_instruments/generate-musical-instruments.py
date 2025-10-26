import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_musical_instrument_names_batch(prompt_template, count=200):
    """
    Generate a batch of musical instrument names using a specific prompt template.
    
    Args:
        prompt_template (str): The prompt template to use
        count (int): Number of musical instruments to generate in this batch
    
    Returns:
        list: List of musical instrument names
    """
    prompt = prompt_template.format(count=count)
    
    try:
        response = chat_with_kimi(prompt, stream=False)
        
        # Parse the response
        instruments = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and not line.isdigit():  # Skip empty lines and numbers
                # Clean the name (remove any extra characters)
                clean_name = re.sub(r'[^\w\s]', '', line).strip()
                if clean_name and len(clean_name.split()) == 1:  # Single word only
                    instruments.append(clean_name.lower())
        
        print(f"Generated {len(instruments)} musical instruments from this batch")
        return instruments
        
    except Exception as e:
        print(f"Error generating musical instruments in batch: {e}")
        return []


def generate_musical_instrument_names_multi_batch(target_count=1000):
    """
    Generate musical instrument names using multiple specialized prompts to get more variety.
    
    Args:
        target_count (int): Target number of musical instruments to generate
    
    Returns:
        list: List of musical instrument names
    """
    print(f"Generating {target_count} diverse musical instrument names using multiple specialized prompts...")
    
    # Define different prompt templates for different musical instrument categories
    prompts = [
        {
            "name": "String Instruments",
            "template": """Generate exactly {count} string instrument names.

Requirements:
- Only single-word instrument names (no spaces, hyphens, or compound words)
- Focus on string instruments from around the world
- Include: guitar, violin, cello, bass, banjo, mandolin, ukulele, harp, lute, sitar
- NO brand names, NO model names, NO duplicates
- Include both Western and non-Western string instruments

Return ONLY the instrument names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Wind Instruments",
            "template": """Generate exactly {count} wind instrument names.

Requirements:
- Only single-word instrument names (no spaces, hyphens, or compound words)
- Focus on wind instruments from around the world
- Include: flute, trumpet, saxophone, clarinet, oboe, bassoon, trombone, tuba, harmonica, recorder
- NO brand names, NO model names, NO duplicates
- Include both Western and non-Western wind instruments

Return ONLY the instrument names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Percussion Instruments",
            "template": """Generate exactly {count} percussion instrument names.

Requirements:
- Only single-word instrument names (no spaces, hyphens, or compound words)
- Focus on percussion instruments from around the world
- Include: drum, cymbal, tambourine, maracas, triangle, xylophone, timpani, bongo, conga, gong
- NO brand names, NO model names, NO duplicates
- Include both Western and non-Western percussion instruments

Return ONLY the instrument names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Keyboard Instruments",
            "template": """Generate exactly {count} keyboard instrument names.

Requirements:
- Only single-word instrument names (no spaces, hyphens, or compound words)
- Focus on keyboard instruments from around the world
- Include: piano, organ, harpsichord, synthesizer, accordion, melodica, celesta, clavichord
- NO brand names, NO model names, NO duplicates
- Include both acoustic and electronic keyboard instruments

Return ONLY the instrument names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Electronic Instruments",
            "template": """Generate exactly {count} electronic instrument names.

Requirements:
- Only single-word instrument names (no spaces, hyphens, or compound words)
- Focus on electronic and digital instruments
- Include: synthesizer, drum, sampler, sequencer, theremin, vocoder, oscillator, filter, mixer
- NO brand names, NO model names, NO duplicates
- Focus on electronic music instruments and equipment

Return ONLY the instrument names, one per line, no numbers, no explanations."""
        },
        {
            "name": "Traditional & World Instruments",
            "template": """Generate exactly {count} traditional and world instrument names.

Requirements:
- Only single-word instrument names (no spaces, hyphens, or compound words)
- Focus on traditional instruments from different cultures
- Include: didgeridoo, koto, shamisen, tabla, djembe, kalimba, panpipe, bagpipe, hurdy, hurdy-gurdy
- NO brand names, NO model names, NO duplicates
- Include instruments from various world cultures and traditions

Return ONLY the instrument names, one per line, no numbers, no explanations."""
        }
    ]
    
    all_instruments = []
    batch_size = max(50, target_count // len(prompts))  # Distribute target across prompts
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\nBatch {i}/{len(prompts)}: {prompt_info['name']}")
        instruments = generate_musical_instrument_names_batch(prompt_info['template'], batch_size)
        all_instruments.extend(instruments)
        print(f"Total instruments so far: {len(all_instruments)}")
    
    return all_instruments


def filter_single_word_instruments(instruments):
    """
    Filter musical instruments to ensure they are single words only.
    
    Args:
        instruments (list): List of musical instrument names
    
    Returns:
        list: Filtered list of single-word instruments
    """
    filtered = []
    for instrument in instruments:
        # Check if it's a single word (no spaces, hyphens, or underscores)
        if len(instrument.split()) == 1 and '-' not in instrument and '_' not in instrument:
            filtered.append(instrument)
    
    return filtered


def save_instruments_list(instruments, filename="list.json"):
    """
    Save the musical instruments list to a JSON file.
    
    Args:
        instruments (list): List of musical instrument names
        filename (str): Output filename
    
    Returns:
        str: Path to the saved file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(instruments, f, indent=2, ensure_ascii=False)
    
    return filepath


def main():
    """Main function to generate and save musical instrument names."""
    print("=== Enhanced Musical Instrument Name Generator ===")
    print("Generating 1000+ diverse single-word musical instrument names using multiple specialized prompts...")
    print()
    
    # Generate musical instruments using multiple specialized prompts
    instruments = generate_musical_instrument_names_multi_batch(target_count=1000)
    
    # Filter to ensure single words only
    print(f"\nFiltering to single-word instruments only...")
    filtered_instruments = filter_single_word_instruments(instruments)
    
    print(f"After filtering: {len(filtered_instruments)} single-word instruments")
    
    # Remove duplicates while preserving order
    unique_instruments = []
    seen = set()
    for instrument in filtered_instruments:
        if instrument not in seen:
            unique_instruments.append(instrument)
            seen.add(instrument)
    
    print(f"After removing duplicates: {len(unique_instruments)} unique instruments")
    
    # Take exactly 1000 (or as many as we have)
    final_instruments = unique_instruments[:1000]
    
    # Save to file
    filepath = save_instruments_list(final_instruments)
    
    print(f"\n✓ Generated {len(final_instruments)} common single-word musical instrument names")
    print(f"✓ Saved to: {filepath}")
    
    # Show some examples
    print(f"\nFirst 20 instruments:")
    for i, instrument in enumerate(final_instruments[:20], 1):
        print(f"  {i:2d}. {instrument}")
    
    if len(final_instruments) > 20:
        print(f"  ... and {len(final_instruments) - 20} more")
    
    # Show statistics
    print(f"\nStatistics:")
    print(f"  Total generated: {len(instruments)}")
    print(f"  After filtering: {len(filtered_instruments)}")
    print(f"  After deduplication: {len(unique_instruments)}")
    print(f"  Final count: {len(final_instruments)}")


if __name__ == "__main__":
    main()
