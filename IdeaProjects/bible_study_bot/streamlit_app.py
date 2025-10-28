import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'main', 'python'))

try:
    from enhanced_ui import main
    main()
except Exception as e:
    st.error(f"Error: {e}")
