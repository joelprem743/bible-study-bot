import streamlit as st
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'main', 'python'))

try:
    from enhanced_ui import main
    main()
except Exception as e:
    st.error(f"Error starting Bible Study Bot: {e}")
    st.info("Please check the file structure and ensure all dependencies are installed.")