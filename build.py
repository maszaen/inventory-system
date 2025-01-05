import os
import shutil
import subprocess
from datetime import datetime


def print_directory_tree(startpath, level=0):
    """Print directory tree structure"""
    for item in os.listdir(startpath):
        if item in ["build", "dist", "__pycache__", ".git"]:
            continue
        path = os.path.join(startpath, item)
        print("  " * level + "|--", item)
        if os.path.isdir(path):
            print_directory_tree(path, level + 1)


def build_app():
    try:
        # Get absolute path to the directory containing build.py
        current_dir = os.path.abspath(os.path.dirname(__file__))
        print("\nDebug Information:")
        print(f"Current directory: {current_dir}")

        print("\nDirectory structure:")
        print_directory_tree(current_dir)

        # Check main.py location
        main_path = os.path.join(current_dir, "src", "main.py")
        print(f"\nChecking main.py at: {main_path}")
        print(f"main.py exists: {os.path.exists(main_path)}")

        if not os.path.exists(main_path):
            # Try to find main.py
            print("\nSearching for main.py...")
            for root, dirs, files in os.walk(current_dir):
                if "main.py" in files:
                    found_path = os.path.join(root, "main.py")
                    print(f"Found main.py at: {found_path}")

        # Define directories
        build_dir = os.path.join(current_dir, "build")
        dist_dir = os.path.join(current_dir, "dist")
        output_dir = os.path.join(current_dir, "output")
        spec_file = os.path.join(current_dir, "inventory.spec")

        # Clean previous builds
        for dir in [build_dir, dist_dir, output_dir]:
            if os.path.exists(dir):
                shutil.rmtree(dir)
        os.makedirs(output_dir)

        # Run PyInstaller
        print("\nRunning PyInstaller...")
        result = subprocess.run(
            ["pyinstaller", spec_file], capture_output=True, text=True, cwd=current_dir
        )

        if result.stdout:
            print("\nPyInstaller Output:")
            print(result.stdout)

        if result.stderr:
            print("\nPyInstaller Errors:")
            print(result.stderr)

        if result.returncode != 0:
            raise Exception(f"PyInstaller failed with return code {result.returncode}")

    except Exception as e:
        print(f"\nError during build: {str(e)}")
        raise


if __name__ == "__main__":
    build_app()
