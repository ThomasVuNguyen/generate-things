import requests
import json
import sys

def generate_fruit_openscad(fruit_type: str) -> str:
    with open("config.json") as f:
        config = json.load(f)
    
    prompt = f"Generate OpenSCAD code for a {fruit_type}. Use proper syntax, include colors, make it 3D printable."
    
    response = requests.post(
        f"{config['ollama']['url']}/api/generate",
        json={
            "model": config["ollama"]["default_model"],
            "prompt": prompt,
            "stream": False
        }
    )
    
    result = response.json()
    return result.get("response", str(result))

def main():
    fruit_type = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"{fruit_type}.scad"
    
    code = generate_fruit_openscad(fruit_type)
    
    with open(output_file, 'w') as f:
        f.write(code)
    
    print(f"Generated {fruit_type} and saved to {output_file}")

if __name__ == "__main__":
    main()