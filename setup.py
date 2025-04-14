import os
import sys
import subprocess
from pathlib import Path
import venv
import argparse

def create_virtualenv(env_path: Path):
    """Create a new virtual environment."""
    print(f"Creating virtual environment at {env_path}...")
    venv.create(env_path, with_pip=True)
    return env_path

def install_requirements(env_path: Path, requirements_file: str):
    """Install requirements from the specified file."""
    print(f"Installing requirements from {requirements_file}...")
    
    # Get the pip executable from the virtual environment
    pip_path = env_path / "bin" / "pip"
    if sys.platform == "win32":
        pip_path = env_path / "Scripts" / "pip.exe"
    
    subprocess.run([str(pip_path), "install", "-r", requirements_file], check=True)

def main():
    parser = argparse.ArgumentParser(description="Setup the voice assistant environment")
    parser.add_argument("--env", choices=["development", "production"], default="development",
                      help="Environment to setup (default: development)")
    args = parser.parse_args()
    
    # Create environment directory
    env_dir = Path(f"venv_{args.env}")
    if not env_dir.exists():
        create_virtualenv(env_dir)
    
    # Install requirements
    requirements_file = f"requirements/{args.env}.txt"
    install_requirements(env_dir, requirements_file)
    
    print(f"\nEnvironment setup complete! To activate the {args.env} environment:")
    if sys.platform == "win32":
        print(f"  {env_dir}\\Scripts\\activate")
    else:
        print(f"  source {env_dir}/bin/activate")

if __name__ == "__main__":
    main() 