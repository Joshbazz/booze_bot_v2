# Project Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Virtual Environment Setup

### Setting up the environment
```bash
# Create a new virtual environment with venv (recommended)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Verify you're in the virtual environment
which python  # Should point to your venv directory
```

### Installing dependencies
```bash
# Install project dependencies
pip install -r requirements.txt

# Verify installations
pip list
```

### Working with the environment
```bash
# To deactivate the virtual environment when you're done
deactivate

# To remove the virtual environment completely (if needed)
# First deactivate, then:
rm -rf venv
```

## Keeping screen active in background
```bash
# To run a screen and detach, you can create a screen instance
screen -S whiskey_scraper

# Inside the new screen session, activate your virtual environment (if needed) and run your script:
source venv/bin/activate
python src/main.py

# To detach from the screen session without stopping the script, press:
Ctrl + A, then D

# If you need to return to the session later, reattach it using:
screen -r whiskey_scraper
```

### SSH Back Into the EC2 Instance
```bash
# Run the following to SSH back into the EC2 Instance:
ssh -i "~/.ssh/booze_bot_key.pem" ec2-user@ec2-3-133-160-250.us-east-2.compute.amazonaws.com
```