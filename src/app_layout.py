import streamlit as st
import base64
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="rAlces Educational App",
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

# Function to create navigation buttons with conditional star
def nav_button(label, key, selected=False):
    button_html = f"""
    <div class="nav-button nav-button-selected" style="position: relative;">
        {label}
        {"<span class='blue-star'>★</span>" if selected else ""}
    </div>
    """
    return st.markdown(button_html, unsafe_allow_html=True)

# Function to encode image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

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
    st.markdown('<div class="tabs-container">', unsafe_allow_html=True)
    
    # Create a placeholder for the logo and header
    col1, col2 = st.columns([1, 2])
    
    with col1:
        pass   # TO FIX!
        
    with col2:
        st.markdown('<h1 class="main-header">rAlces</h1>', unsafe_allow_html=True)
    
    # Navigation buttons with clickable functionality
    if st.button("WIXARIKA", key="wixarika_btn", use_container_width=True):
        st.session_state.biology_selected = True
        set_tab('subjects')
    
    if st.button("RARAMURI", key="raramuri_btn", use_container_width=True):
        set_tab('subjects')
    
    if st.button("OTOMI", key="otomi_btn", use_container_width=True):
        set_tab('subjects')
        
    st.markdown('</div>', unsafe_allow_html=True)

def subjects_page():
    st.markdown('<div class="tabs-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">Subjects</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        biology_btn = st.button(
            "BIOLOGY", 
            key="biology_btn", 
            use_container_width=True,
            help="Click to view Biology content"
        )
        if biology_btn:
            set_subject('BIOLOGY')
            
        math1_btn = st.button(
            "MATH", 
            key="math1_btn", 
            use_container_width=True,
            help="Click to view Math content"
        )
        if math1_btn:
            set_subject('MATH')
            
    with col2:
        math2_btn = st.button(
            "MATH", 
            key="math2_btn", 
            use_container_width=True,
            help="Click to view Math content"
        )
        if math2_btn:
            set_subject('MATH')
            
        math3_btn = st.button(
            "MATH", 
            key="math3_btn", 
            use_container_width=True,
            help="Click to view Math content"
        )
        if math3_btn:
            set_subject('MATH')
            
    st.markdown('</div>', unsafe_allow_html=True)

def subject_detail_page():
    st.markdown('<div class="tabs-container">', unsafe_allow_html=True)
    
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
        if st.button("Quiz!", key="quiz_btn", use_container_width=True):
            st.write("Quiz functionality will be implemented here.")
            
    with col2:
        if st.button("Help me Tutor!", key="help_btn", use_container_width=True):
            st.write("Tutoring assistance will be provided here.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### Navigation")
    
    if st.button("Home", key="nav_home"):
        set_tab('home')
        
    if st.button("Subjects", key="nav_subjects"):
        set_tab('subjects')
        
    if st.session_state.selected_subject:
        if st.button(f"{st.session_state.selected_subject} Detail", key="nav_detail"):
            set_tab('subject_detail')

# Display the appropriate page based on session state
if st.session_state.tab == 'home':
    home_page()
elif st.session_state.tab == 'subjects':
    subjects_page()
elif st.session_state.tab == 'subject_detail':
    subject_detail_page()