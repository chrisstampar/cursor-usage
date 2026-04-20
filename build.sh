#!/bin/bash
set -e

if [ ! -f "venv/bin/activate" ]; then
  echo "Missing venv. Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Convert generated icon to ICNS
echo "Converting icon..."
python scripts/convert_icon.py "assets/icon.png" "assets/icon.icns"

# Build the app using py2app
echo "Building the app..."
rm -rf build dist
python setup.py py2app -A

# Ensure it's not currently running before overwriting
echo "Closing existing instance (if any)..."
pkill -f "CursorUsage.app" || true
sleep 1

# Move it to /Applications
echo "Moving to /Applications..."
rm -rf /Applications/CursorUsage.app
cp -R dist/CursorUsage.app /Applications/

# Launch the newly built app
echo "Launching CursorUsage.app..."
open -a /Applications/CursorUsage.app

echo "Success!"