#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Install Node.js (if not available)
if ! command -v node &> /dev/null
then
    echo "Node.js not found, installing..."
    # Render static sites might not have this, but Docker will or we can use another method.
fi

# Export frontend
reflex export --frontend-only --no-zip

# Move static files to the publish directory
# Render expects files in the root or a specified folder
mkdir -p _static
cp -r .web/_static/* _static/
