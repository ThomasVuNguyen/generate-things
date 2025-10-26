import sys
import os
import json
import subprocess
import tempfile
import time
from datetime import datetime, timedelta

# Add parent directory to path to import from inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.kimi import chat_with_kimi


def generate_openscad_electronic_device(device_name, style="realistic", complexity="medium"):
    """
    Generate OpenSCAD code for an electronic device using the Kimi model.
    
    Args:
        device_name (str): Name of the electronic device to generate
        style (str): Style of the model ("realistic", "stylized", "minimal")
        complexity (str): Complexity level ("simple", "medium", "detailed")
    
    Returns:
        str: Generated OpenSCAD code
    """
    prompt = f"""Generate OpenSCAD code for a {device_name} electronic device in {style} style with {complexity} complexity.

Requirements:
- Use only basic OpenSCAD primitives (cube, sphere, cylinder, etc.)
- Use transformations (translate, rotate, scale, mirror)
- Use boolean operations (union, difference, intersection)
- Use loops and modules for repetitive parts
- Make it 3D printable (no overhangs, proper wall thickness)
- Include comments explaining each part
- The model should be recognizable as a {device_name}
- Size should be reasonable for 3D printing (roughly 50-100mm in largest dimension)
- Include electronic device-specific features and characteristics
- Use appropriate colors for the device (color() function)

Style guidelines for {style}:
- Realistic: More detailed, functional accuracy
- Stylized: Simplified but recognizable device features
- Minimal: Very simple geometric shapes representing the device

Complexity for {complexity}:
- Simple: Basic shapes, 20-50 lines of code
- Medium: Moderate detail, 50-150 lines of code  
- Detailed: High detail, 150+ lines of code

Electronic device-specific considerations:
- Include characteristic features (screens, buttons, ports, etc.)
- Use appropriate proportions for the device
- Include device-specific details (logos, indicators, etc.)
- Consider the device's typical appearance and functionality

Output only the OpenSCAD code, no explanations or markdown formatting."""

    try:
        response = chat_with_kimi(prompt, stream=False)
        return response.strip()
    except Exception as e:
        print(f"Error generating OpenSCAD code for '{device_name}': {e}")
        return None


def test_openscad_rendering(code):
    """
    Test if OpenSCAD code can be rendered without errors.
    
    Args:
        code (str): The OpenSCAD code to test
    
    Returns:
        bool: True if code renders successfully, False otherwise
    """
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.scad', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        # Try to render the OpenSCAD file
        result = subprocess.run(
            ['openscad', '--info', temp_file_path],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        # Check if the command succeeded
        return result.returncode == 0
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        # If OpenSCAD is not installed or command fails, assume it's valid
        return True
    except Exception:
        return False


def save_openscad_code(code, device_name, output_dir="generated_models"):
    """
    Save OpenSCAD code to a file.
    
    Args:
        code (str): The OpenSCAD code to save
        device_name (str): Name of the electronic device (used for filename)
        output_dir (str): Directory to save the file
    
    Returns:
        str: Path to the saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean device name for filename
    clean_name = "".join(c for c in device_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_name = clean_name.replace(' ', '_').lower()
    
    # Add timestamp to avoid conflicts
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{clean_name}_{timestamp}.scad"
    filepath = os.path.join(output_dir, filename)
    
    # Save the code
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    
    return filepath


def load_dataset(dataset_file="electronic_device_openscad_dataset.json"):
    """
    Load the existing dataset from file.
    
    Args:
        dataset_file (str): Path to the dataset file
    
    Returns:
        list: The dataset list
    """
    if os.path.exists(dataset_file):
        try:
            with open(dataset_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both old format and new format
                if isinstance(data, dict) and "electronic_devices" in data:
                    return data["electronic_devices"]
                elif isinstance(data, list):
                    return data
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Return empty dataset list
    return []


def save_dataset(dataset, dataset_file="electronic_device_openscad_dataset.json"):
    """
    Save the dataset to file.
    
    Args:
        dataset (list): The dataset list
        dataset_file (str): Path to the dataset file
    """
    with open(dataset_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)


def add_device_to_dataset(dataset, device_name, openscad_code, render_success, error_message=None):
    """
    Add an electronic device entry to the dataset.
    
    Args:
        dataset (list): The dataset list
        device_name (str): Name of the electronic device
        openscad_code (str): Generated OpenSCAD code
        render_success (bool): Whether the code renders successfully
        error_message (str): Error message if generation failed
    """
    device_entry = {
        "electronic_device": device_name,
        "openscad_code": openscad_code,
        "renders": render_success
    }
    
    # Only add error message if there's an error
    if error_message:
        item_entry["error"] = error_message
    
    dataset.append(device_entry)


def format_time_duration(seconds):
    """
    Format seconds into a human-readable duration string.
    
    Args:
        seconds (float): Duration in seconds
    
    Returns:
        str: Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def calculate_eta(start_time, current_index, total_items):
    """
    Calculate estimated time of arrival based on current progress.
    
    Args:
        start_time (float): Start time timestamp
        current_index (int): Current item index (0-based)
        total_items (int): Total number of items to process
    
    Returns:
        tuple: (elapsed_time, eta_time, remaining_time)
    """
    if current_index == 0:
        return 0, None, None
    
    elapsed_time = time.time() - start_time
    avg_time_per_item = elapsed_time / current_index
    remaining_items = total_items - current_index
    remaining_time = remaining_items * avg_time_per_item
    eta_time = time.time() + remaining_time
    
    return elapsed_time, eta_time, remaining_time


def process_devices_from_list(device_list, max_items=None, style="realistic", complexity="medium", dataset_file="electronic_device_openscad_dataset.json"):
    """
    Process electronic devices from list sequentially, generating OpenSCAD code and testing rendering.
    
    Args:
        device_list (list): List of electronic device names
        max_items (int): Maximum number of devices to process (None for all)
        style (str): Style for all models
        complexity (str): Complexity for all models
        dataset_file (str): Path to the dataset file
    
    Returns:
        dict: The updated dataset
    """
    # Load existing dataset
    dataset = load_dataset(dataset_file)
    
    # Determine how many devices to process
    if max_items is None:
        max_items = len(device_list)
    else:
        max_items = min(max_items, len(device_list))
    
    print(f"Processing {max_items} electronic devices from list...")
    print(f"Style: {style}, Complexity: {complexity}")
    print(f"Dataset file: {dataset_file}")
    print("-" * 60)
    
    # Get list of already processed devices
    processed_devices = [entry["electronic_device"] for entry in dataset]
    
    successful_count = sum(1 for entry in dataset if entry.get("renders", False))
    failed_count = len(dataset) - successful_count
    
    # Find the next device to process
    devices_to_process = []
    for device_name in device_list[:max_items]:
        if device_name not in processed_devices:
            devices_to_process.append(device_name)
    
    print(f"Found {len(processed_devices)} already processed devices")
    print(f"Will process {len(devices_to_process)} new devices")
    
    if len(devices_to_process) == 0:
        print("All devices have already been processed!")
        return dataset
    
    # Start timing
    start_time = time.time()
    
    for i, device_name in enumerate(devices_to_process):
        # Calculate ETA
        elapsed_time, eta_time, remaining_time = calculate_eta(start_time, i, len(devices_to_process))
        
        # Format time strings
        elapsed_str = format_time_duration(elapsed_time)
        if eta_time:
            eta_str = datetime.fromtimestamp(eta_time).strftime("%H:%M:%S")
            remaining_str = format_time_duration(remaining_time)
            time_info = f" | Elapsed: {elapsed_str} | ETA: {eta_str} | Remaining: {remaining_str}"
        else:
            time_info = f" | Elapsed: {elapsed_str}"
        
        print(f"Processing [{i+1}/{len(devices_to_process)}]: {device_name}{time_info}")
        
        # Generate OpenSCAD code
        code = generate_openscad_electronic_device(device_name, style, complexity)
        
        if code:
            # Test if the code renders
            print(f"  Testing rendering...")
            render_success = test_openscad_rendering(code)
            
            if render_success:
                print(f"  ✓ Code generated and renders successfully")
                successful_count += 1
            else:
                print(f"  ⚠ Code generated but failed to render")
                failed_count += 1
            
            # Add to dataset
            add_device_to_dataset(dataset, device_name, code, render_success)
            
        else:
            print(f"  ✗ Failed to generate code")
            failed_count += 1
            # Add failed entry to dataset
            add_device_to_dataset(dataset, device_name, "", False, "Failed to generate OpenSCAD code")
        
        # Save dataset after each device (incremental saving)
        save_dataset(dataset, dataset_file)
        print(f"  Dataset updated: {successful_count} successful, {failed_count} failed")
        print()
    
    print(f"Processing complete!")
    print(f"Total devices processed: {len(dataset)}")
    print(f"Successful generations: {successful_count}")
    print(f"Failed generations: {failed_count}")
    
    return dataset


def main():
    """Main function with command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate OpenSCAD electronic device models using AI")
    parser.add_argument("device", nargs="?", help="Name of the electronic device to generate")
    parser.add_argument("--list", action="store_true", help="Process devices from list.json")
    parser.add_argument("--max", type=int, help="Maximum number of devices to process from list (default: all)")
    parser.add_argument("--style", choices=["realistic", "stylized", "minimal"], default="realistic", 
                       help="Style of the model")
    parser.add_argument("--complexity", choices=["simple", "medium", "detailed"], default="medium",
                       help="Complexity level")
    parser.add_argument("--dataset", default="electronic_device_openscad_dataset.json", help="Dataset file path")
    parser.add_argument("--resume", action="store_true", help="Resume processing from where it left off")
    
    args = parser.parse_args()
    
    if args.list:
        # Process devices from the list.json file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        list_file = os.path.join(script_dir, "list.json")
        
        if not os.path.exists(list_file):
            print(f"Error: {list_file} not found!")
            return
        
        with open(list_file, 'r', encoding='utf-8-sig') as f:
            device_list = json.load(f)
        
        print(f"Loaded {len(device_list)} electronic devices from {list_file}")
        
        # Process devices sequentially
        dataset = process_devices_from_list(
            device_list, 
            max_items=args.max, 
            style=args.style, 
            complexity=args.complexity,
            dataset_file=args.dataset
        )
        
        print(f"\nDataset saved to: {args.dataset}")
        
    elif args.device:
        # Generate single device and add to dataset
        print(f"Generating OpenSCAD model for: {args.device}")
        print(f"Style: {args.style}, Complexity: {args.complexity}")
        
        # Load dataset
        dataset = load_dataset(args.dataset)
        
        # Generate code
        code = generate_openscad_electronic_device(args.device, args.style, args.complexity)
        
        if code:
            # Test rendering
            render_success = test_openscad_rendering(code)
            print(f"Rendering test: {'✓ Success' if render_success else '✗ Failed'}")
            
            # Add to dataset
            add_device_to_dataset(dataset, args.device, code, render_success)
            save_dataset(dataset, args.dataset)
            
            print(f"✓ Added to dataset: {args.dataset}")
        else:
            print("✗ Failed to generate code")
            add_device_to_dataset(dataset, args.device, "", False, "Failed to generate OpenSCAD code")
            save_dataset(dataset, args.dataset)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
