import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_pokemon_names(count=1000):
    """
    Generate a list of Pokemon names using the Kimi model in one go.
    
    Args:
        count (int): Total number of Pokemon to generate
    
    Returns:
        list: List of Pokemon names
    """
    print(f"Generating {count} diverse Pokemon names in one go...")
    
    prompt = f"""Generate a list of exactly {count} Pokemon names.

Requirements:
- Only single-word Pokemon names (no spaces, hyphens, or compound words)
- Include Pokemon from all generations (Gen 1-9)
- Include both common and rare Pokemon
- Include legendary and mythical Pokemon
- Include starter Pokemon
- Include evolved forms and pre-evolutions
- Include regional variants where appropriate
- Names should be recognizable Pokemon names
- No duplicates
- Return only the names, one per line, no numbering or formatting

Examples of good Pokemon names:
pikachu, charizard, blastoise, venusaur, mewtwo, mew, lugia, hooh, celebi, rayquaza, groudon, kyogre, dialga, palkia, giratina, arceus, reshiram, zekrom, kyurem, xerneas, yveltal, zygarde, solgaleo, lunala, necrozma, zacian, zamazenta, eternatus, kubfu, urshifu, calyrex, regieleki, regidrago, glastrier, spectrier, bulbasaur, ivysaur, charmander, charmeleon, squirtle, wartortle, caterpie, metapod, butterfree, weedle, kakuna, beedrill, pidgey, pidgeotto, pidgeot, rattata, raticate, spearow, fearow, ekans, arbok, sandshrew, sandslash, nidoran, nidorina, nidoqueen, nidorino, nidoking, clefairy, clefable, vulpix, ninetales, jigglypuff, wigglytuff, zubat, golbat, oddish, gloom, vileplume, paras, parasect, venonat, venomoth, diglett, dugtrio, meowth, persian, psyduck, golduck, mankey, primeape, growlithe, arcanine, poliwag, poliwhirl, poliwrath, abra, kadabra, alakazam, machop, machoke, machamp, bellsprout, weepinbell, victreebel, tentacool, tentacruel, geodude, graveler, golem, ponyta, rapidash, slowpoke, slowbro, magnemite, magneton, farfetchd, doduo, dodrio, seel, dewgong, grimer, muk, shellder, cloyster, gastly, haunter, gengar, onix, drowzee, hypno, krabby, kingler, voltorb, electrode, exeggcute, exeggutor, cubone, marowak, hitmonlee, hitmonchan, lickitung, koffing, weezing, rhyhorn, rhydon, chansey, tangela, kangaskhan, horsea, seadra, goldeen, seaking, staryu, starmie, mr_mime, scyther, jynx, electabuzz, magmar, pinsir, tauros, magikarp, gyarados, lapras, ditto, eevee, vaporeon, jolteon, flareon, porygon, omanyte, omastar, kabuto, kabutops, aerodactyl, snorlax, articuno, zapdos, moltres, dratini, dragonair, dragonite

Generate exactly {count} Pokemon names:"""

    try:
        response = chat_with_kimi(prompt)
        
        # Parse the response to extract Pokemon names
        lines = response.strip().split('\n')
        pokemon_names = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('//'):
                # Clean up the line to extract just the Pokemon name
                pokemon_name = re.sub(r'^[\d\.\-\s]+', '', line).strip()
                pokemon_name = pokemon_name.lower()
                
                # Validate that it looks like a Pokemon name
                if pokemon_name and pokemon_name.isalpha() and len(pokemon_name) > 2:
                    pokemon_names.append(pokemon_name)
        
        print(f"Generated {len(pokemon_names)} Pokemon names")
        return pokemon_names
        
    except Exception as e:
        print(f"Error generating Pokemon names: {e}")
        return []


def save_pokemon_list(pokemon_names, filename="list.json"):
    """
    Save the Pokemon names to a JSON file.
    
    Args:
        pokemon_names (list): List of Pokemon names
        filename (str): Output filename
    """
    try:
        # Set default path if using default filename
        if filename == "list.json":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(script_dir, "list.json")
        
        with open(filename, 'w') as f:
            json.dump(pokemon_names, f, indent=2)
        print(f"Saved {len(pokemon_names)} Pokemon names to {filename}")
    except Exception as e:
        print(f"Error saving Pokemon list: {e}")


def main():
    """Main function to generate and save Pokemon names."""
    print("Pokemon Name Generator")
    print("=" * 50)
    
    # Generate Pokemon names
    pokemon_names = generate_pokemon_names(1000)
    
    if pokemon_names:
        # Save to file
        save_pokemon_list(pokemon_names)
        
        # Display first 20 names as preview
        print("\nFirst 20 Pokemon names:")
        for i, name in enumerate(pokemon_names[:20], 1):
            print(f"{i:2d}. {name}")
        
        if len(pokemon_names) > 20:
            print(f"... and {len(pokemon_names) - 20} more")
    else:
        print("No Pokemon names were generated.")


if __name__ == "__main__":
    main()
