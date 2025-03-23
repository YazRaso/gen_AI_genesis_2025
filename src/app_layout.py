import streamlit as st
import base64
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="rAlces",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
def apply_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Arial Black', sans-serif;
    }
    
    .nav-button {
        background-color: #FF8C55;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px 20px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        margin-bottom: 15px;
        cursor: pointer;
        transition: background-color 0.3s;
        text-align: center;
    }
    
    .nav-button:hover {
        background-color: #FF7033;
    }
    
    .nav-button-selected {
        background-color: #FF8C55;
        position: relative;
    }
    
    .blue-star {
        color: #4287f5;
        font-size: 24px;
        position: absolute;
        top: -5px;
        right: -5px;
    }
    
    .subject-button {
        background-color: #FF8C55;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 25px;
        font-size: 22px;
        font-weight: bold;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    
    .quiz-button {
        background-color: #7DCE82;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        margin-bottom: 15px;
        cursor: pointer;
    }
    
    .help-button {
        background-color: #FFD54F;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
    }
    
    .content-box {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 20px;
        margin-top: 20px;
        min-height: 500px;
    }
    
    .subject-header {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Arial Black', sans-serif;
    }
    
    .subject-text {
        font-size: 18px;
        line-height: 1.6;
        margin-bottom: 20px;
        text-align: justify;
    }
    
    .tabs-container {
        padding: 20px;
        border: 2px solid #ddd;
        border-radius: 10px;
        min-height: 600px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to create navigation buttons without star
def nav_button(label, key):
    button_html = f"""
    <div class="nav-button" style="position: relative;">
        {label}
    </div>
    """
    return st.markdown(button_html, unsafe_allow_html=True)


# Initialize session state
if 'tab' not in st.session_state:
    st.session_state.tab = 'home'
if 'selected_subject' not in st.session_state:
    st.session_state.selected_subject = None
if 'biology_selected' not in st.session_state:
    st.session_state.biology_selected = False

# Function to set tab
def set_tab(tab_name):
    st.session_state.tab = tab_name
    
# Function to set selected subject
def set_subject(subject_name):
    st.session_state.selected_subject = subject_name
    if subject_name == 'BIOLOGY':
        st.session_state.biology_selected = True
    st.session_state.tab = 'subject_detail'

# Apply custom CSS
apply_custom_css()

def home_page():
    #st.markdown('<div class="tabs-container">', unsafe_allow_html=True)
    
    # Create a placeholder for the logo and header
    col1, col2 = st.columns([1, 2])
    
    # Create a placeholder for the logo and header
    st.markdown('<h1 class="main-header">rAlces</h1>', unsafe_allow_html=True)
    
    # Navigation buttons with clickable functionality
    if st.button("wixárika", key="wixarika_btn", use_container_width=True):
        st.session_state.biology_selected = True
        set_tab('subjects')
    
    if st.button("rarámuri", key="raramuri_btn", use_container_width=True):
        set_tab('subjects')
    
    if st.button("otomí", key="otomi_btn", use_container_width=True):
        set_tab('subjects')
        
    #st.markdown('</div>', unsafe_allow_html=True)

def subjects_page():
    #st.markdown('<div class="tabs-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">temas</h1>', unsafe_allow_html=True) # subjects
    
    col1, col2 = st.columns(2)
    
    with col1:
        biology_btn = st.button(
            "biologia", # biology
            key="biology_btn", 
            use_container_width=True,
            help="Click to view Biology content"
        )
        if biology_btn:
            set_subject('biologia')
            
        math_btn = st.button(
            "matematicas", # math
            key="math_btn", 
            use_container_width=True,
            help="Click to view Math content"
        )
        if math_btn:
            set_subject('matematicas')
            
    with col2:
        geography_btn = st.button(
            "geografia", # geography
            key="geography_btn", 
            use_container_width=True,
            help="Click to view Math content"
        )
        if geography_btn:
            set_subject('geografia')
            
        history_btn = st.button(
            "historia", # history
            key="history_btn", 
            use_container_width=True,
            help="Click to view Math content"
        )
        if history_btn:
            set_subject('historia')
            
    st.markdown('</div>', unsafe_allow_html=True)

def subject_detail_page():
    #st.markdown('<div class="tabs-container">', unsafe_allow_html=True)
    
    st.markdown(f'<h1 class="subject-header">{st.session_state.selected_subject}</h1>', unsafe_allow_html=True)
    
    # Sample content
    st.markdown("""
    <div class="subject-text">
        Here is where the textual content for this subject will be displayed. 
        This can include introductory information, lessons, examples, and other educational material.
    </div>
    
    <div class="subject-text">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris. 
        Vivamus hendrerit arcu sed erat molestie vehicula. Sed auctor neque eu tellus rhoncus ut eleifend nibh porttitor.
    </div>
    
    <div class="subject-text">
        The content can be customized based on the specific subject and learning objectives.
        Images, charts, and other visual aids can also be incorporated to enhance the learning experience.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("examen", key="quiz_btn", use_container_width=True): # exam
            st.write("Quiz functionality will be implemented here.")
            
    with col2:
        if st.button("ayuda tutor", key="help_btn", use_container_width=True): # help tutor
            st.write("Tutoring assistance will be provided here.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### Navigation")
    
    if st.button("inicio", key="nav_home"): # home
        set_tab('home')
        
    if st.button("tema", key="nav_subjects"): # tema
        set_tab('subjects')
        
    if st.session_state.selected_subject:
        if st.button(f"{st.session_state.selected_subject} detalle", key="nav_detail"): # detail
            set_tab('subject_detail')

# Display the appropriate page based on session state
if st.session_state.tab == 'home':
    home_page()
elif st.session_state.tab == 'subjects':
    subjects_page()
elif st.session_state.tab == 'subject_detail':
    subject_detail_page()