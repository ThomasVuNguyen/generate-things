#!/usr/bin/env python3
"""
Generate index.html from rendered images
"""

import os
import json
from pathlib import Path

def generate_html():
    """Generate the HTML page with all images"""
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenSCAD Dataset Visualizer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 3rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .stats {
            background: white;
            padding: 15px 25px;
            border-radius: 10px;
            margin-bottom: 25px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .dataset-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .dataset-title {
            font-size: 1.8rem;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            text-transform: capitalize;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }

        .item-card {
            background: #f8f9fa;
            border-radius: 10px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .item-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }

        .item-image {
            width: 100%;
            height: 200px;
            object-fit: contain;
            background: white;
            padding: 10px;
        }

        .item-title {
            padding: 15px;
            font-weight: 600;
            color: #333;
            text-align: center;
            text-transform: capitalize;
            font-size: 0.95rem;
            word-wrap: break-word;
        }

        .placeholder {
            display: flex;
            align-items: center;
            justify-content: center;
            background: #e9ecef;
            color: #6c757d;
            font-size: 0.9rem;
            height: 200px;
        }

        .error-message {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #c33;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 OpenSCAD Dataset Visualizer</h1>
        
        <div class="stats" id="stats">
            {stats}
        </div>

        {datasets}
    </div>
</body>
</html>
'''
    
    # Scan images directory
    images_dir = Path('images')
    if not images_dir.exists():
        print("Error: images/ directory not found. Please run render.sh first.")
        return
    
    datasets = []
    total_items = 0
    
    # Iterate through each dataset folder
    for dataset_dir in sorted(images_dir.iterdir()):
        if not dataset_dir.is_dir():
            continue
            
        dataset_name = dataset_dir.name
        images = []
        
        # Find all PNG files
        for img_file in sorted(dataset_dir.glob('*.png')):
            img_name = img_file.stem
            title = img_name.replace('_', ' ')
            
            # Use relative path from render directory
            rel_path = str(img_file).replace('\\', '/')
            images.append({
                'src': rel_path,
                'title': title
            })
        
        if images:
            datasets.append({
                'name': dataset_name,
                'images': images
            })
            total_items += len(images)
    
    # Build dataset sections
    datasets_html = ''
    for dataset in datasets:
        grid_html = '<div class="grid">\n'
        for image in dataset['images']:
            grid_html += f'''            <div class="item-card">
                <img src="{image['src']}" alt="{image['title']}" class="item-image" 
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                <div class="placeholder" style="display:none;">Image not available</div>
                <div class="item-title">{image['title']}</div>
            </div>
'''
        grid_html += '        </div>'
        
        datasets_html += f'''
        <div class="dataset-section">
            <div class="dataset-title">{dataset['name'].replace('_', ' ')} ({len(dataset['images'])} items)</div>
{grid_html}
        </div>
'''
    
    # Fill in stats
    stats_text = f'<strong>{len(datasets)} datasets</strong> | <strong>{total_items} total items</strong>'
    
    if not datasets:
        stats_text = 'No datasets found. Please run ./render.sh first.'
        datasets_html = '<div class="error-message">No images found. Please run <code>./render.sh</code> first to generate images.</div>'
    
    # Write the HTML file
    html_content = html.format(stats=stats_text, datasets=datasets_html)
    
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print(f"Generated index.html with {len(datasets)} datasets and {total_items} images")
    print("Open index.html in your browser to view all the rendered OpenSCAD models.")

if __name__ == '__main__':
    generate_html()

