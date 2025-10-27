#!/bin/bash

PORT=1306

echo "Auto-scanning images/ directory..."

# Automatically generate HTML from images
python3 generate_html.py 2>/dev/null || echo "Note: No images found yet. Run ./render.sh first."

echo ""
echo "Starting web server on port $PORT..."

# Kill any existing process on port 1306
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "Killing existing process on port $PORT..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Start the web server
echo "Starting HTTP server on port $PORT..."
echo "Opening http://localhost:$PORT in your browser..."

# Use Python's built-in HTTP server in the background
python3 -m http.server $PORT &

# Store the PID
SERVER_PID=$!

# Wait a moment for the server to start
sleep 2

# Open the browser (try different commands for different OS)
if command -v xdg-open > /dev/null; then
    xdg-open "http://localhost:$PORT" &
elif command -v open > /dev/null; then
    open "http://localhost:$PORT" &
fi

echo ""
echo "✓ Server started on http://localhost:$PORT"
echo "✓ Press Ctrl+C to stop the server"
echo ""

# Wait for the server process
wait $SERVER_PID

