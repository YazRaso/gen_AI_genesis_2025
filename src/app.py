import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Set page config
st.set_page_config(
    page_title="TAI - Indigenous Learning",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def read_markdown_file(markdown_file):
    with open(markdown_file, "r") as f:
        markdown_text = f.read()
    return markdown_text


markdown_path = "bio_lesson_wixa(goated).md"

markdown_text = read_markdown_file(markdown_path)


def ask_question(question):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        st.warning("Missing Google API Key. Please add GOOGLE_API_KEY to your .env file.")
        return

    # Ensure session state exists for question response
    if "question_response" not in st.session_state:
        st.session_state["question_response"] = ""

    # Configure the Gemini API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Generate prompt
    prompt = (f"Answer the following question about {st.session_state.selected_subject} solely "
              f"in {st.session_state.selected_language}, {question} NO ENGLISH WHATSOEVER")

    # Generate response only when the button is clicked
    if st.button("Ask"):
        response = model.generate_content(prompt)
        st.session_state["question_response"] = response.text.strip()  # Store response persistently

    # Display response if it exists
    if st.session_state["question_response"]:
        st.write(st.session_state["question_response"])


def update_answer(index):
    st.session_state.answers[index] = st.session_state[f"answer{index+1}"]


def take_exam_text():
    # Ensure session state for answers exists
    if "answers" not in st.session_state:
        st.session_state.answers = ["", "", ""]

    # Ensure session state for questions exists
    if "questions" not in st.session_state:
        st.session_state.questions = []

    # Ensure session state for feedback exists
    if "feedback_response" not in st.session_state:
        st.session_state.feedback_response = ""

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        st.warning("Missing Google API Key. Please add GOOGLE_API_KEY to your .env file.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Generate questions only if they haven't been generated yet
    if not st.session_state.questions:
        prompt = (f"Ask three questions about {st.session_state.selected_subject} in "
                  f"{st.session_state.selected_language} NO ENGLISH WHATSOEVER")
        response = model.generate_content(prompt)
        prompt_response = response.text.strip()
        st.session_state.questions = prompt_response.split("\n")  # Assuming questions are separated by newlines
        st.write(f"TAI says: {prompt_response}")

    # Display questions from session state
    for i, question in enumerate(st.session_state.questions):
        st.write(f"Question {i+1}: {question}")

    # Create persistent text inputs and update session state
    st.session_state.answers[0] = st.text_input("1.", value=st.session_state.answers[0], key="answer1",
                                                on_change=lambda: update_answer(0))
    st.session_state.answers[1] = st.text_input("2.", value=st.session_state.answers[1], key="answer2",
                                                on_change=lambda: update_answer(1))
    st.session_state.answers[2] = st.text_input("3.", value=st.session_state.answers[2], key="answer3",
                                                on_change=lambda: update_answer(2))

    if st.button(label="✅", key="submit_answers"):
        prompt_to_give = (f"Examine the following answers {st.session_state.answers} to the question, "
                          f"give feedback only in {st.session_state.selected_language} NO ENGLISH WHATSOEVER")

        response = model.generate_content(prompt_to_give)
        st.session_state.feedback_response = response.text.strip()  # Store response in session state

    # Display feedback if it exists
    if st.session_state.feedback_response:
        st.write(st.session_state.feedback_response)



def translate(output_lang=None, text="") -> str:
    """
    Translates text using Google Gemini API

    Args:
        output_lang: Target language code (defaults to session state language)
        text: Text to translate

    Returns:
        str: Translated text
    """
    # If no language selected or text is empty, return original text
    if not output_lang or not text:
        return text

    # Load API key from environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        st.warning("Missing Google API Key. Please add GOOGLE_API_KEY to your .env file.")
        return text

    # Configure the Gemini API
    genai.configure(api_key=api_key)

    try:
        # Create a prompt for translation
        prompt = (f"Translate the following text to {output_lang}. Return "
                  f"only the translated text without explanations or quotation marks: {text} NO ENGLISH WHATSOEVER")

        # Initialize the model
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Generate the translation
        response = model.generate_content(prompt)
        translated_text = response.text.strip()

        return translated_text

    except Exception as e:
        # Log error but return original text
        print(f"Translation error: {str(e)}")
        return text


# Cache translations to avoid repeated API calls for the same content
@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_translate(lang, text):
    if not lang or lang == "English":
        return text
    return translate(output_lang=lang, text=text)


# Custom CSS for styling with improved aesthetics
def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        color: #333;
    }

    .main-header {
        font-size: 60px;
        font-weight: 700;
        text-align: center;
        margin: 30px 0;
        color: #FF6B35;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-family: 'Poppins', sans-serif;
    }

    .language-selector {
        background-color: #FF8C55;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 20px;
        font-size: 22px;
        font-weight: 600;
        width: 100%;
        margin-bottom: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }

    .language-selector:hover {
        background-color: #FF7033;
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    .subject-button {
        background-color: #FF8C55;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 30px;
        font-size: 24px;
        font-weight: 600;
        width: 100%;
        margin-bottom: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .subject-button:hover {
        background-color: #FF7033;
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    .action-button {
        border: none;
        border-radius: 15px;
        padding: 20px;
        font-size: 20px;
        font-weight: 600;
        width: 100%;
        margin-bottom: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .quiz-button {
        background-color: #7DCE82;
        color: white;
    }

    .quiz-button:hover {
        background-color: #64B168;
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    .help-button {
        background-color: #FFD54F;
        color: white;
    }

    .help-button:hover {
        background-color: #FFC93C;
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    .back-button {
        background-color: #6C757D;
        color: white;
    }

    .back-button:hover {
        background-color: #5A6268;
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    .subject-header {
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        margin: 30px 0;
        color: #FF6B35;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-family: 'Poppins', sans-serif;
    }

    .secondary-header {
        font-size: 36px;
        font-weight: 600;
        margin: 25px 0;
        color: #FF8C55;
        font-family: 'Poppins', sans-serif;
    }

    .subject-text {
        font-size: 18px;
        line-height: 1.8;
        margin-bottom: 25px;
        text-align: justify;
        color: #444;
    }

    .content-container {
        background-color: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
        min-height: 600px;
    }

    .sidebar .nav-button {
        background-color: #FF8C55;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }

    .sidebar .nav-button:hover {
        background-color: #FF7033;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 14px;
        color: #6c757d;
        margin-top: 40px;
    }

    /* Icons for subjects */
    .icon-container {
        margin-right: 15px;
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize session state
if 'tab' not in st.session_state:
    st.session_state.tab = 'home'
if 'selected_subject' not in st.session_state:
    st.session_state.selected_subject = None
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = None


# Function to set tab
def set_tab(tab_name):
    st.session_state.tab = tab_name


# Function to set selected subject
def set_subject(subject_name):
    st.session_state.selected_subject = subject_name
    st.session_state.tab = 'subject_detail'


# Function to set selected language
def set_language(language_name):
    st.session_state.selected_language = language_name
    set_tab('subjects')


# Apply custom CSS
apply_custom_css()

# Dictionary for subject icons
SUBJECT_ICONS = {
    'biology': '🧬',
    'mathematics': '📊',
    'geography': '🌎',
    'history': '📜'
}

# Pre-translated texts for common UI elements
UI_TEXTS = {
    "English": {
        "back": "← Back",
        "back_to_topics": "← Back to Topics",
        "study_topics": "Study Topics",
        "language": "Language",
        "lessons": "Lessons",
        "exercises": "Exercises",
        "multimedia": "Multimedia",
        "take_exam": "📝 Take Exam",
        "request_help": "🙋 Request Tutor Help",
        "exam_coming_soon": "The evaluation system will be available soon.",
        "tutor_coming_soon": "The personalized tutoring function will be available soon.",
        "about_TAI": "About TAI",
        "TAI_description": "TAI is an educational platform designed to support the lear"
                              "ning of students from indigenous communities, respecting an"
                              "d preserving their languages and cultures while facilitati"
                              "ng access to quality education.",
        "select_language": "Select your language",
        "home": "🏠 Home",
        "topics": "📚 Topics",
        "help": "Help",
        "help_description": "If you need assistance, you can:",
        "help_options": [
            "Contact your teacher",
            "Visit the resource center",
            "Send a message to support"
        ],
        "navigation": "Navigation",
        # Subject descriptions
        "biology_desc": "Study of living beings and their processes",
        "mathematics_desc": "Numbers, operations and problem solving",
        "geography_desc": "Study of Earth, its characteristics and populations",
        "history_desc": "Past events and their impact on our cultures",
        # Subject content
        "biology_content": markdown_text,
        "mathematics_content": {
            "title1": "Number Systems",
            "content1": "Different cultures have developed different systems for coun"
                        "ting and representing quantities. Today we will study the decimal system and compare it with traditional systems.",
            "title2": "Basic Operations:",
            "list2": [
                "Addition (+): Combines two or more quantities to obtain a total",
                "Subtraction (-): Finds the difference between two quantities",
                "Multiplication (×): Repeated addition of the same number",
                "Division (÷): Distributes a quantity into equal parts"
            ],
            "title3": "Mathematics in Our Daily Life",
            "content3": "Mathematics are present in all activities of our community: in textile weaving, in housing construction, in agriculture and in commercial exchanges."
        },
        "default_content": "The content for this topic is under development. Soon we will have educational material available for you.",
        "exercises_intro": "Here you will find practical exercises to test your knowledge. Select a specific lesson to see related exercises.",
        "practice_exercise": "Practice Exercise",
        "complete_activity": "Complete the following activity and check your answers when finished.",
        "question": "Question:",
        "living_beings_question": "What are the main characteristics of living beings?",
        "multimedia_intro": "In this section you will find videos, audios and interactive materials that will help you to better understand the study topics.",
        "multimedia_material": "Multimedia Material",
        "multimedia_coming_soon": "Multimedia resources will be available soon.",
        "space_for_multimedia": "Space reserved for multimedia content"
    }
}


# Function to get translated text for UI elements
def get_ui_text(key, section=None, index=None):
    # Default to English if no language is selected
    lang = st.session_state.selected_language if st.session_state.selected_language else "English"

    # If we don't have this language pre-translated, translate on the fly
    if lang not in UI_TEXTS:
        # Base on English text
        if section and index is not None:
            # Check if the item is a list
            if isinstance(UI_TEXTS["English"][section][key], list):
                text = UI_TEXTS["English"][section][key][index]
            else:
                # Handle non-list case
                text = UI_TEXTS["English"][section][key]
        elif section:
            text = UI_TEXTS["English"][section]
        else:
            text = UI_TEXTS["English"][key]

        # Translate
        return cached_translate(lang, text)

    # Return from pre-translated texts
    if section and index is not None:
        # Check if the item is a list
        if isinstance(UI_TEXTS[lang][section][key], list):
            return UI_TEXTS[lang][section][key][index]
        else:
            # Handle non-list case
            return UI_TEXTS[lang][section][key]
    elif section:
        return UI_TEXTS[lang][section]
    else:
        return UI_TEXTS[lang][key]


def home_page():
    # Logo and header
    st.markdown('<h1 class="main-header">TAI</h1>', unsafe_allow_html=True)

    # Subtitle - Learning Platform
    learning_platform_text = cached_translate(
        st.session_state.selected_language,
        "Learning Platform for Indigenous Communities"
    )
    st.markdown(
        f'<p style="text-align:center; font-size:22px; margin-bottom:40px;">{learning_platform_text}</p>',
        unsafe_allow_html=True
    )

    # Select language text
    select_language_text = get_ui_text("select_language")
    st.markdown(
        f'<h2 style="text-align:center; font-size:30px; margin-bottom:30px; color:#FF8C55;">{select_language_text}</h2>',
        unsafe_allow_html=True
    )

    # Language selection
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Wixárika", key="wixarika_btn", use_container_width=True):
            set_language('Wixárika')

    with col2:
        if st.button("Rarámuri", key="raramuri_btn", use_container_width=True):
            set_language('Rarámuri')

    with col3:
        if st.button("Otomí", key="otomi_btn", use_container_width=True):
            set_language('Otomí')

    # About section
    about_TAI_text = get_ui_text("about_TAI")
    TAI_description = get_ui_text("TAI_description")

    st.markdown(
        f'<h3 style="text-align:center; font-size:26px; margin-top:60px; color:#FF8C55;">{about_TAI_text}</h3>',
        unsafe_allow_html=True
    )

    st.markdown(f'''
    <p style="text-align:center; font-size:18px; margin:20px 40px;">
    {TAI_description}
    </p>
    ''', unsafe_allow_html=True)

    # Footer
    footer_text = cached_translate(
        st.session_state.selected_language,
        "© 2025 TAI - Inclusive Education"
    )
    st.markdown(f'<div class="footer">{footer_text}</div>', unsafe_allow_html=True)


def subjects_page():
    # Back button
    back_text = get_ui_text("back")
    if st.button(back_text, key="back_to_home", use_container_width=False):
        set_tab('home')

    # Header showing selected language
    language_text = get_ui_text("language")
    if st.session_state.selected_language:
        st.markdown(
            f'<h2 style="text-align:center; font-size:28px; margin-bottom:20px;">{language_text}: {st.session_state.selected_language}</h2>',
            unsafe_allow_html=True
        )

    # Study Topics header
    study_topics_text = get_ui_text("study_topics")
    st.markdown(f'<h1 class="subject-header">{study_topics_text}</h1>', unsafe_allow_html=True)

    # Subject selection with icons and descriptions
    col1, col2 = st.columns(2)

    # Translate subject names
    biology_text = cached_translate(st.session_state.selected_language, "Biology")
    mathematics_text = cached_translate(st.session_state.selected_language, "Mathematics")
    geography_text = cached_translate(st.session_state.selected_language, "Geography")
    history_text = cached_translate(st.session_state.selected_language, "History")

    # Get subject descriptions
    biology_desc = get_ui_text("biology_desc")
    mathematics_desc = get_ui_text("mathematics_desc")
    geography_desc = get_ui_text("geography_desc")
    history_desc = get_ui_text("history_desc")

    with col1:
        # Biology button with icon
        if st.button(f"{SUBJECT_ICONS['biology']} {biology_text}", key="biology_btn", use_container_width=True):
            set_subject('biology')

        st.markdown(f'<p style="text-align:center; margin-bottom:30px;">{biology_desc}</p>',
                    unsafe_allow_html=True)

        # Math button with icon
        if st.button(f"{SUBJECT_ICONS['mathematics']} {mathematics_text}", key="math_btn", use_container_width=True):
            set_subject('mathematics')

        st.markdown(
            f'<p style="text-align:center; margin-bottom:30px;">{mathematics_desc}</p>',
            unsafe_allow_html=True)

    with col2:
        # Geography button with icon
        if st.button(f"{SUBJECT_ICONS['geography']} {geography_text}", key="geography_btn", use_container_width=True):
            set_subject('geography')

        st.markdown(
            f'<p style="text-align:center; margin-bottom:30px;">{geography_desc}</p>',
            unsafe_allow_html=True)

        # History button with icon
        if st.button(f"{SUBJECT_ICONS['history']} {history_text}", key="history_btn", use_container_width=True):
            set_subject('history')

        st.markdown(
            f'<p style="text-align:center; margin-bottom:30px;">{history_desc}</p>',
            unsafe_allow_html=True)

    # Footer
    footer_text = cached_translate(
        st.session_state.selected_language,
        "© 2025 rAlces - Inclusive Education"
    )
    st.markdown(f'<div class="footer">{footer_text}</div>', unsafe_allow_html=True)


def subject_detail_page():
    # Back button
    back_to_topics_text = get_ui_text("back_to_topics")
    if st.button(back_to_topics_text, key="back_to_subjects", use_container_width=False):
        set_tab('subjects')

    # Get subject name and translate it
    subject_name = st.session_state.selected_subject.capitalize()
    translated_subject = cached_translate(st.session_state.selected_language, subject_name)

    # Header with subject icon
    icon = SUBJECT_ICONS.get(st.session_state.selected_subject.lower(), '📚')
    st.markdown(f'<h1 class="subject-header">{icon} {translated_subject}</h1>', unsafe_allow_html=True)

    # Tab navigation for subject content
    lessons_text = get_ui_text("lessons")
    exercises_text = get_ui_text("exercises")
    multimedia_text = get_ui_text("multimedia")

    tabs = [lessons_text, exercises_text, multimedia_text]
    tab_keys = ["Lessons", "Exercises", "Multimedia"]  # internal keys that don't change

    cols = st.columns(len(tabs))
    selected_tab = "Lessons"  # Default tab

    for i, tab in enumerate(tabs):
        with cols[i]:
            if st.button(tab, key=f"tab_{tab_keys[i]}", use_container_width=True):
                selected_tab = tab_keys[i]

    # Display the selected tab name
    selected_tab_translated = tabs[tab_keys.index(selected_tab)]
    st.markdown(f'<h2 class="secondary-header">{selected_tab_translated}</h2>', unsafe_allow_html=True)

    # Content based on subject and tab
    if selected_tab == "Lessons":
        if st.session_state.selected_subject == 'biology':
            if st.session_state.selected_language == "Wixárika":
                st.write(markdown_text)
            # Get translated content for biology
            title1 = get_ui_text("title1", "biology_content")
            content1 = get_ui_text("content1", "biology_content")
            title2 = get_ui_text("title2", "biology_content")
            list2 = [get_ui_text("list2", "biology_content", i) for i in range(5)]
            title3 = get_ui_text("title3", "biology_content")
            content3 = get_ui_text("content3", "biology_content")

            st.markdown(f'''
            <div class="subject-text">
                <b>{title1}</b><br>
                {content1}
            </div>

            <div class="subject-text">
                <b>{title2}</b>
                <ul>
                    <li>{list2[0]}</li>
                    <li>{list2[1]}</li>
                    <li>{list2[2]}</li>
                    <li>{list2[3]}</li>
                    <li>{list2[4]}</li>
                </ul>
            </div>

            <div class="subject-text">
                <b>{title3}</b><br>
                {content3}
            </div>
            ''', unsafe_allow_html=True)

        elif st.session_state.selected_subject == 'mathematics':
            # Get translated content for mathematics
            title1 = get_ui_text("title1", "mathematics_content")
            content1 = get_ui_text("content1", "mathematics_content")
            title2 = get_ui_text("title2", "mathematics_content")
            list2 = [get_ui_text("list2", "mathematics_content", i) for i in range(4)]
            title3 = get_ui_text("title3", "mathematics_content")
            content3 = get_ui_text("content3", "mathematics_content")

            st.markdown(f'''
            <div class="subject-text">
                <b>{title1}</b><br>
                {content1}
            </div>

            <div class="subject-text">
                <b>{title2}</b>
                <ul>
                    <li>{list2[0]}</li>
                    <li>{list2[1]}</li>
                    <li>{list2[2]}</li>
                    <li>{list2[3]}</li>
                </ul>
            </div>

            <div class="subject-text">
                <b>{title3}</b><br>
                {content3}
            </div>
            ''', unsafe_allow_html=True)
        else:
            default_content = get_ui_text("default_content")
            st.markdown(f'''
            <div class="subject-text">
                {default_content}
            </div>
            ''', unsafe_allow_html=True)

    elif selected_tab == "Exercises":
        exercises_intro = get_ui_text("exercises_intro")
        practice_exercise = get_ui_text("practice_exercise")
        complete_activity = get_ui_text("complete_activity")
        question = get_ui_text("question")
        living_beings_question = get_ui_text("living_beings_question")

        st.markdown(f'''
        <div class="subject-text">
            {exercises_intro}
        </div>
        ''', unsafe_allow_html=True)

        # Sample exercise
        st.markdown(f'''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;">
            <h3 style="color: #FF8C55;">{practice_exercise}</h3>
            <p>{complete_activity}</p>
            <div style="margin-top: 15px;">
                <p><b>{question}</b> {living_beings_question}</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    elif selected_tab == "Multimedia":
        multimedia_intro = get_ui_text("multimedia_intro")
        multimedia_material = get_ui_text("multimedia_material")
        multimedia_coming_soon = get_ui_text("multimedia_coming_soon")
        space_for_multimedia = get_ui_text("space_for_multimedia")

        st.markdown(f'''
        <div class="subject-text">
            {multimedia_intro}
        </div>
        ''', unsafe_allow_html=True)

        # Placeholder for multimedia content
        st.markdown(f'''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: center;">
            <h3 style="color: #FF8C55;">{multimedia_material}</h3>
            <p>{multimedia_coming_soon}</p>
            <div style="background-color: #e9ecef; height: 200px; border-radius: 5px; display: flex; align-items: center; justify-content: center; margin-top: 15px;">
                <p>{space_for_multimedia}</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # Footer
    footer_text = cached_translate(
        st.session_state.selected_language,
        "© 2025 TAI - Inclusive Education"
    )
    st.markdown(f'<div class="footer">{footer_text}</div>', unsafe_allow_html=True)

    # Move columns to the bottom
    col1, col2 = st.columns(2)
    with col1:
        take_etext = get_ui_text("take_exam")
        if st.button(take_etext, key="quiz_btn", use_container_width=True):
            exam_response = take_exam_text()
            if exam_response:
                response_label = translate(st.session_state.selected_language, exam_response)
                st.write(response_label)

    with col2:
        request_help_text = get_ui_text("request_help")
        if st.button(request_help_text, key="help_btn", use_container_width=True):
            question_label = translate(st.session_state.selected_language, "What is your question?")
            question = st.text_input(question_label, key="question_input")
            if question:
                ask_question(question=question)

# Display the appropriate page based on session state
if st.session_state.tab == 'home':
    home_page()
elif st.session_state.tab == 'subjects':
    subjects_page()
elif st.session_state.tab == 'subject_detail':
    subject_detail_page()
