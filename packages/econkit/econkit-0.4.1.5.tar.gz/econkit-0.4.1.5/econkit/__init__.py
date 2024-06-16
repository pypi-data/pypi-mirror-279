# __init__.py

# Import Version
from .version import __version__

# Import Other Modules
from .econkit import econometrics, finance

# Version Check and Update Function
import subprocess
import sys
import requests
import importlib
import os
from distutils.version import LooseVersion

def check_and_install_libraries(requirements_path='requirements.txt'):
    def check_and_install(package):
        try:
            importlib.import_module(package)
            print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} is not installed.")
            response = input(f"Do you want to install {package}? (yes/no): ").strip().lower()
            if response == 'yes':
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{package} has been installed.")
            else:
                print(f"{package} is required for this library to work properly.")

    if not os.path.exists(requirements_path):
        print(f"requirements.txt file not found at {requirements_path}")
        return

    with open(requirements_path, 'r') as file:
        lines = file.readlines()
    
    required_packages = [line.strip().split('==')[0] for line in lines if line.strip() and not line.startswith('#')]
    
    for package in required_packages:
        check_and_install(package)

def check_for_latest_version():
    try:
        current_version = __version__
        response = requests.get('https://pypi.org/pypi/econkit/json')
        latest_version = response.json()['info']['version']
        
        if LooseVersion(current_version) < LooseVersion(latest_version):
            print(f"A new version of econkit is available: {latest_version}")
            update = input("Do you want to update now? (yes/no): ").strip().lower()
            if update == 'yes':
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "econkit"])
                print("Library updated. Please restart your application.")
    except Exception as e:
        print(f"Error checking for library update: {e}")

# Check and install required libraries
check_and_install_libraries()

# Initialize the version check at the end of the file
check_for_latest_version()
