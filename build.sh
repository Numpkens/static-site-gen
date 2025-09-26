#!/bin/bash

# This script builds the site for GitHub Pages deployment.

# 1. Clean up old build files
rm -rf docs
# 2. Run the main script, passing the basepath as a CLI argument.
#    Replace 'REPO_NAME' with your actual repository name!
python3 src/main.py "/static-site-gen/"
