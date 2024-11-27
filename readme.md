# Project Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Virtual Environment Setup

### Setting up the environment
```bash
# Create a new virtual environment
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

## Chrome Driver Architecture Notes
The Chrome driver architecture (ARM vs x86) won't pose a problem for your setup because:
1. The driver is downloaded dynamically based on your system's architecture
2. When running locally on your Mac (ARM), it will download the ARM-compatible driver
3. When deployed to EC2 (x86), it will download the x86-compatible driver
4. Selenium manager handles this compatibility automatically

## Best Practices
- Always activate the virtual environment before working on the project
- Keep `requirements.txt` updated using `pip freeze > requirements.txt`
- Commit `requirements.txt` to version control, but not the `venv` directory

## Troubleshooting
If you encounter issues:
1. Ensure you're using the correct Python version
2. Verify the virtual environment is activated
3. Try removing and recreating the virtual environment
4. Check Chrome and Chrome driver versions match

## Common Commands Reference
```bash
# Update pip in virtual environment
pip install --upgrade pip

# Generate requirements.txt
pip freeze > requirements.txt

# Update all packages
pip install -r requirements.txt --upgrade
```