import streamlit as st
import pandas as pd
import re
import sys
import os

# Add the parent directory to path to import our AI module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.main.python.enhanced_bible_ai import EnhancedBibleAI

# Initialize AI engine
@st.cache_resource
def init_ai():
    return EnhancedBibleAI()

ai_engine = init_ai()

def main():
    st.set_page_config(
        page_title="Bible Study Bot 🤖",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
    <style>
    .verse-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4CAF50;
        background-color: #f9f9f9;
        margin: 0.5rem 0;
    }
    .study-plan-day {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9C27B0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("📖 Bible Study Bot")
        st.markdown("---")

        # Translation selection
        translation = st.selectbox(
            "Choose Translation",
            options=ai_engine.available_translations,
            index=0,
            format_func=lambda x: x.upper()
        )

        # Quick access buttons
        st.subheader("Quick Access")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("💝 Love"):
                st.session_state.current_topic = "love"
            if st.button("🙏 Prayer"):
                st.session_state.current_topic = "prayer"

        with col2:
            if st.button("🌟 Faith"):
                st.session_state.current_topic = "faith"
            if st.button("🕊️ Salvation"):
                st.session_state.current_topic = "salvation"

        # Study plan generator
        st.subheader("Study Plans")
        study_topic = st.text_input("Study Topic", "salvation")
        study_days = st.slider("Days", 3, 14, 7)

        if st.button("Generate Study Plan"):
            st.session_state.study_plan = ai_engine.generate_study_plan(study_topic, study_days)

        st.markdown("---")
        st.markdown("### About")
        st.info("This Bible Study Bot helps you explore Scripture with AI assistance. Ask questions, find verses, and follow study plans!")

    # Main content area
    st.title("🤖 Bible Study Assistant")
    st.markdown("Ask questions, explore verses, or follow a study plan!")

    # Tab interface
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "🔍 Verse Lookup", "📚 Study Plans"])

    with tab1:
        chat_interface(translation)

    with tab2:
        verse_lookup_interface(translation)

    with tab3:
        study_plans_interface()

def chat_interface(translation):
    """Enhanced chat interface"""

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm your Bible study assistant. Ask me anything about Scripture! 📖\n\nTry asking about:\n- Salvation\n- Prayer\n- Love\n- Faith\n- Hope"}
        ]

    # Display chat messages
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message"><strong>Bot:</strong> {message["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask your Bible question..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Generate response
        with st.spinner("Searching Scripture..."):
            response = generate_chat_response(prompt, translation)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Rerun to update the display
        st.rerun()

def generate_chat_response(question: str, translation: str) -> str:
    """Generate response for chat questions"""

    # Common questions patterns
    question_patterns = {
        r'salvation|saved|born again': {
            "verses": ["John 3:16-17", "Romans 10:9-10", "Ephesians 2:8-9"],
            "response": "Here's what the Bible says about salvation:"
        },
        r'pray|prayer': {
            "verses": ["Matthew 6:9-13", "Philippians 4:6-7", "1 Thessalonians 5:17"],
            "response": "The Bible teaches us about prayer:"
        },
        r'love|love others': {
            "verses": ["1 Corinthians 13:4-7", "John 13:34-35", "1 John 4:7-8"],
            "response": "Here are key verses about love:"
        },
        r'faith|believe': {
            "verses": ["Hebrews 11:1", "2 Corinthians 5:7", "Romans 10:17"],
            "response": "The Bible defines faith as:"
        },
        r'hope|future': {
            "verses": ["Jeremiah 29:11", "Romans 15:13", "Hebrews 6:19"],
            "response": "Scripture offers hope through these verses:"
        }
    }

    # Check for pattern matches
    for pattern, data in question_patterns.items():
        if re.search(pattern, question.lower()):
            response = f"{data['response']}\n\n"
            for verse_ref in data['verses']:
                try:
                    # Extract book, chapter, verse
                    parts = verse_ref.split(' ')
                    book = ' '.join(parts[:-1])
                    chapter_verse = parts[-1].split(':')[0]
                    verse = parts[-1].split(':')[1] if ':' in parts[-1] else '1'

                    verse_info = ai_engine.get_verse(book, int(chapter_verse), int(verse), translation)
                    if verse_info:
                        response += f"**{verse_ref}**: {verse_info['text']}\n\n"
                except Exception as e:
                    response += f"**{verse_ref}** - [Look up this verse]\n\n"

            response += "*Would you like me to explain any of these verses further?*"
            return response

    # Fallback response
    return "I'd love to help you explore that topic in Scripture! Could you be more specific about what you're looking for? For example, you could ask about 'what the Bible says about prayer' or 'verses about hope'. Try using the quick access buttons in the sidebar for common topics!"

def verse_lookup_interface(translation):
    """Verse lookup and search interface"""

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Verse Lookup")
        book = st.text_input("Book", "John")
        chapter = st.number_input("Chapter", min_value=1, value=3)
        verse = st.number_input("Verse", min_value=1, value=16)

        if st.button("Lookup Verse"):
            verse_data = ai_engine.get_verse(book, chapter, verse, translation)
            if verse_data:
                st.session_state.current_verse = verse_data
            else:
                st.error("Verse not found. Please check the reference.")

    with col2:
        st.subheader("Search Verses")
        search_query = st.text_input("Search keywords (e.g., love, faith, hope)")

        if st.button("Search Scripture"):
            if search_query:
                results = ai_engine.search_verses(search_query, translation)
                st.session_state.search_results = results
                st.success(f"Found {len(results)} results for '{search_query}'")

    # Display current verse
    if 'current_verse' in st.session_state:
        verse = st.session_state.current_verse
        st.markdown(f"""
        <div class="verse-card">
            <h3>{verse['reference']} ({translation.upper()})</h3>
            <p>{verse['text']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Cross-references
        try:
            book_name = verse['reference'].split(' ')[0]
            chapter_verse = verse['reference'].split(' ')[1]
            chapter = int(chapter_verse.split(':')[0])
            verse_num = int(chapter_verse.split(':')[1])

            cross_refs = ai_engine.get_cross_references(book_name, chapter, verse_num)

            if cross_refs:
                with st.expander("📚 Cross References"):
                    for ref in cross_refs:
                        st.write(f"• {ref}")
        except:
            pass

    # Display search results
    if 'search_results' in st.session_state and st.session_state.search_results:
        st.subheader("Search Results")
        for result in st.session_state.search_results:
            st.markdown(f"""
            <div class="verse-card">
                <h4>{result['reference']}</h4>
                <p>{result['text']}</p>
            </div>
            """, unsafe_allow_html=True)

def study_plans_interface():
    """Study plans interface"""

    st.subheader("Bible Study Plans")

    if 'study_plan' in st.session_state:
        st.success("Here's your personalized study plan!")

        for day_plan in st.session_state.study_plan:
            with st.container():
                st.markdown(f"""
                <div class="study-plan-day">
                    <h4>📅 Day {day_plan['day']}: {day_plan['topic']}</h4>
                </div>
                """, unsafe_allow_html=True)

                st.write("**Verses to study:**")
                for verse_ref in day_plan['verses']:
                    st.write(f"📖 {verse_ref}")

                st.markdown("---")
    else:
        st.info("Generate a study plan using the sidebar! Choose a topic and duration, then click 'Generate Study Plan'.")

if __name__ == "__main__":
    main()