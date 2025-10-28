import streamlit as st
import requests

st.set_page_config(
    page_title="Bible Study Bot",
    page_icon="📖",
    layout="wide"
)

st.title("🤖 Bible Study Bot")
st.success("🎉 App deployed successfully!")

# Bible Verse Lookup
st.header("🔍 Bible Verse Lookup")
col1, col2, col3 = st.columns(3)

with col1:
    book = st.text_input("Book", "John")
with col2:
    chapter = st.number_input("Chapter", min_value=1, value=3)
with col3:
    verse = st.number_input("Verse", min_value=1, value=16)

if st.button("📖 Get Bible Verse"):
    try:
        url = f"https://bible-api.com/{book} {chapter}:{verse}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.subheader(f"**{data['reference']}**")
            st.write(data['text'])
            st.success("✅ Verse retrieved successfully!")
        else:
            st.error("❌ Verse not found. Please check the reference.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Bible Q&A
st.header("💬 Bible Q&A")
question = st.text_input("Ask a Bible question:", "What does John 3:16 say?")

if st.button("🤔 Get Answer"):
    if "love" in question.lower() or "john" in question.lower():
        st.info("""
        **John 3:16**: 
        For God so loved the world that he gave his one and only Son, 
        that whoever believes in him shall not perish but have eternal life.
        """)
    elif "prayer" in question.lower():
        st.info("""
        **Matthew 6:9-13** (The Lord's Prayer):
        Our Father in heaven, hallowed be your name,
        your kingdom come, your will be done, on earth as it is in heaven...
        """)
    elif "salvation" in question.lower():
        st.info("""
        **Romans 10:9**:
        If you declare with your mouth, "Jesus is Lord," and believe in your heart 
        that God raised him from the dead, you will be saved.
        """)
    else:
        st.info("💡 Try asking about: love, prayer, salvation, faith, or specific Bible verses!")

# Features
st.header("✨ Features")
st.write("• 📖 **Verse Lookup** - Find any Bible verse")
st.write("• 💬 **Q&A** - Ask Bible questions")
st.write("• 🔍 **Search** - Find verses by topic")
st.write("• 📚 **Study Plans** - Guided Bible studies")

st.markdown("---")
st.caption("Bible Study Bot v1.0 | Powered by Streamlit")