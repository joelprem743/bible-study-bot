# Replace streamlit_app.py with correct content
cat > streamlit_app.py << 'EOF'
import streamlit as st
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'main', 'python'))

try:
    from enhanced_bible_ai import EnhancedBibleAI
    from enhanced_ui import main

    # Run the main app
    if __name__ == "__main__":
        main()
except Exception as e:
    st.error(f"Error starting app: {e}")
    st.info("Please check the file structure and imports.")
EOF