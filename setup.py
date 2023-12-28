import sys
import subprocess
import pkg_resources


def check_requirements():
    """Check if all requirements from requirements.txt are installed."""
    with open("requirements.txt") as f:
        required_packages = f.read().splitlines()

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}

    for package in required_packages:
        package_name = package.split("==")[0] if "==" in package else package
        if package_name not in installed_packages:
            print(f"{package_name} not installed. Attempting to install...")
            subprocess.call(f"pip install {package}", shell=True)


def check_install_command(command, install_command):
    """Check if a command is available, and if not, attempt to install it."""
    if subprocess.call(
        ["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ):
        print(f"{command} not found. Attempting to install...")
        subprocess.call(install_command, shell=True)


def main():
    # Check for all requirements
    check_requirements()

    # Check for Graphviz
    if sys.platform.startswith("linux"):
        check_install_command("dot", "sudo apt-get install graphviz")
    elif sys.platform == "darwin":
        check_install_command("dot", "brew install graphviz")
    elif sys.platform == "win32":
        print("Please install Graphviz from https://graphviz.org/download/")


if __name__ == "__main__":
    main()
