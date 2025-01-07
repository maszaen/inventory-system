import os
import sys
import subprocess


def build():
    MAIN_PROJECT = os.path.abspath(os.path.dirname(__file__))
    MAIN_SCRIPT = os.path.join(MAIN_PROJECT, "src", "main.py")
    OUTPUT_DIR = os.path.join(MAIN_PROJECT, "dist")

    nuitka_command = [
        "python",
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        "--windows-console-mode=disable",
        "--enable-plugin=pyside6",
        # Include packages
        "--include-package=src",
        "--include-package=PySide6",
        "--include-package=pymongo",
        "--include-package=bcrypt",
        "--include-package=dotenv",
        "--include-package=xlsxwriter",
        # Include project modules
        "--include-module=src.models",
        "--include-module=src.ui",
        "--include-module=src.utils",
        "--include-module=src.database",
        # Resource handling
        f"--include-data-files={os.path.join(MAIN_PROJECT, 'assets', 'icon.ico')}=assets/icon.ico",
        f"--include-data-dir={os.path.join(MAIN_PROJECT, 'assets')}=assets/",
        f"--include-data-dir={os.path.join(MAIN_PROJECT, 'logs')}=logs/",
        f"--include-data-files={os.path.join(MAIN_PROJECT, 'src', 'config.py')}=src/config.py",
        f"--include-data-files={os.path.join(MAIN_PROJECT, 'src', 'style_config.py')}=src/style_config.py",
        # Icon configurations
        f"--windows-icon-from-ico={os.path.join(MAIN_PROJECT, 'assets', 'icon.ico')}",
        "--windows-company-name=Amikom",
        "--windows-product-name=PyStockFlow",
        "--windows-file-version=2.0.0",
        "--windows-product-version=5.0.0",
        # Output configuration
        f"--output-dir={OUTPUT_DIR}",
        "--output-filename=PyStockFlow.exe",
        "--remove-output",
        "--assume-yes-for-downloads",
        # Main script
        MAIN_SCRIPT,
    ]

    try:
        print("Starting Nuitka build...")
        print("This may take several minutes...")

        result = subprocess.run(
            nuitka_command, capture_output=True, text=True, check=True
        )

        if result.stdout:
            print("\nBuild Output:")
            print(result.stdout)

        if result.stderr:
            print("\nBuild Warnings/Errors:")
            print(result.stderr)

        print("\nBuild completed successfully!")
        print(f"Executable can be found in: {OUTPUT_DIR}")

    except subprocess.CalledProcessError as e:
        print(f"Build failed with error code {e.returncode}")
        print("\nError output:")
        print(e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    build()
