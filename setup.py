"""
Setup script for Vocabolarioum Language Learning Platform
Run this script to set up the project structure and dependencies
"""

import os
import sys
from pathlib import Path
import subprocess

def create_directory_structure():
    """Create necessary directories"""
    print("📁 Creating directory structure...")
    
    directories = [
        "config",
        "utils",
        "pages",
        "data",
        "assets",
        "assets/languages"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ Created {directory}/")
    
    # Create __init__.py files
    init_files = ["utils/__init__.py"]
    for init_file in init_files:
        Path(init_file).touch(exist_ok=True)
        print(f"   ✓ Created {init_file}")
    
    print("✅ Directory structure created successfully!\n")

def setup_virtual_environment():
    """Set up Python virtual environment"""
    print("🐍 Setting up virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("   ⚠️  Virtual environment already exists")
        response = input("   Do you want to recreate it? (y/n): ")
        if response.lower() != 'y':
            print("   Skipping virtual environment setup\n")
            return False
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("   ✓ Virtual environment created")
        print("✅ Virtual environment setup complete!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to create virtual environment: {e}\n")
        return False

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    # Determine pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = Path("venv/Scripts/pip.exe")
    else:  # Unix/Linux/Mac
        pip_path = Path("venv/bin/pip")
    
    if not pip_path.exists():
        print("   ⚠️  Virtual environment not found. Please activate it manually.")
        print("   Windows: venv\\Scripts\\activate")
        print("   Unix/Mac: source venv/bin/activate")
        print("   Then run: pip install -r requirements.txt\n")
        return False
    
    try:
        # Upgrade pip
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        if Path("requirements.txt").exists():
            subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
            print("   ✓ Dependencies installed successfully")
            print("✅ Installation complete!\n")
            return True
        else:
            print("   ⚠️  requirements.txt not found")
            print("   Please create requirements.txt with the necessary packages\n")
            return False
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install dependencies: {e}\n")
        return False

def create_env_template():
    """Create .env template file"""
    print("📝 Creating .env template...")
    
    env_template = """# Vocabolarioum Environment Variables
# Copy this file to .env and fill in your actual values

# Email Configuration (Gmail)
SENDER_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password

# Admin Credentials
ADMIN_USER=admin
ADMIN_PASS=admin123

# Optional: Database Configuration (for future PostgreSQL migration)
# DATABASE_URL=postgresql://user:password@localhost/vocabolarioum
"""
    
    env_file = Path(".env.template")
    
    if env_file.exists():
        print("   ⚠️  .env.template already exists")
    else:
        with open(env_file, "w") as f:
            f.write(env_template)
        print("   ✓ Created .env.template")
    
    print("✅ Environment template created!\n")
    print("   📌 Next step: Copy .env.template to .env and fill in your values\n")

def create_gitignore():
    """Create .gitignore file"""
    print("🚫 Creating .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Streamlit
.streamlit/

# Environment variables
.env

# Database files
data/*.xlsx
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Distribution
dist/
build/
*.egg-info/
"""
    
    gitignore_file = Path(".gitignore")
    
    if gitignore_file.exists():
        print("   ⚠️  .gitignore already exists")
    else:
        with open(gitignore_file, "w") as f:
            f.write(gitignore_content)
        print("   ✓ Created .gitignore")
    
    print("✅ .gitignore created!\n")

def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📋 NEXT STEPS:\n")
    
    print("1. Activate the virtual environment:")
    if os.name == 'nt':
        print("   Windows: venv\\Scripts\\activate")
    else:
        print("   Unix/Mac: source venv/bin/activate")
    
    print("\n2. Configure environment variables:")
    print("   - Copy .env.template to .env")
    print("   - Fill in your Gmail credentials and admin password")
    
    print("\n3. Add language learning materials:")
    print("   - Place your PDF module in assets/languages/module.pdf")
    
    print("\n4. Run the application:")
    print("   streamlit run app.py")
    
    print("\n5. Access the application:")
    print("   - Open browser at http://localhost:8501")
    print("   - Admin login: admin/admin123 (change this!)")
    
    print("\n" + "="*60)
    print("📚 For more information, see README.md")
    print("="*60 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🌍 VOCABOLARIOUM SETUP WIZARD")
    print("="*60 + "\n")
    
    print("This script will set up the Vocabolarioum project structure.\n")
    
    # Create directory structure
    create_directory_structure()
    
    # Setup virtual environment
    venv_created = setup_virtual_environment()
    
    # Install dependencies
    if venv_created:
        install_dependencies()
    else:
        print("⚠️  Skipping dependency installation. Install manually:\n")
        print("   1. Activate virtual environment")
        print("   2. Run: pip install -r requirements.txt\n")
    
    # Create environment template
    create_env_template()
    
    # Create .gitignore
    create_gitignore()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ An error occurred: {e}")
        sys.exit(1)