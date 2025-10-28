#!/usr/bin/env python3
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        sys.exit(1)

def main():
    print("🚀 Starting Bible Study Bot...")
    print("📦 Installing requirements...")
    install_requirements()

    print("🌐 Starting Streamlit app...")
    try:
        # Change to the directory where enhanced_ui.py is located
        ui_path = os.path.join(os.path.dirname(__file__), "src", "main", "python", "enhanced_ui.py")
        os.system(f"streamlit run {ui_path}")
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        print("💡 Make sure you're in the correct directory and all files are present.")

if __name__ == "__main__":
    main()