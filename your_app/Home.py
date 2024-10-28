import streamlit as st

# Set the page title and layout
st.set_page_config(page_title="Home Page", layout="wide", initial_sidebar_state="collapsed")

# Hide the sidebar completely
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
        #MainMenu {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Add styling to make content flush and professional
st.markdown("""
    <style>
    /* Add spacing and styling for content */
    .section-heading {
        color: #1f1f1f;
        font-size: 24px;
        margin-bottom: 15px;
        font-weight: 500;
    }
    .section-content {
        color: #444;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 25px;
    }
    /* Remove default streamlit padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 20rem;
        padding-right: 20rem;
    }
            /* Hide image expand button */
    button[title="View fullscreen"] {
        display: none;
    }
    /* Ensure columns are equal height */
    [data-testid="column"] {
        height: fit-content;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: start;
    }
    /* Container for text content */
    .text-content {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: start;
        padding: 20px 0;
    }
    /* Navigation styling */
    .nav-links {
        display: flex;
        justify-content: center;
        padding: 20px;
        background-color: #f8f9fa;
        margin-bottom: 30px;
    }
    .nav-links a {
        margin: 0 20px;
        padding: 8px 16px;
        text-decoration: none;
        color: #1f1f1f;
        font-size: 18px;
        border-radius: 4px;
        transition: background-color 0.3s;
    }
    .nav-links a:hover {
        background-color: #e9ecef;
    }
    /* Image container styling */
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    </style>

    <div class="nav-links">
        <a href="Finance">Finance</a>
        <a href="Football">Football</a>
    </div>
""", unsafe_allow_html=True)

# Create two equal columns with custom padding
col1, col2 = st.columns([1, 1], gap="small")

# Column 1: Image on the left
with col1:
    st.markdown(
        '<div style="display: flex; justify-content: center; align-items: center; padding-top: 20px;">',
        unsafe_allow_html=True
    )
    #st.image("image.png", width=500)  # Set explicit width to 200 pixels
    st.markdown('</div>', unsafe_allow_html=True)

# Column 2: Text content on the right
with col2:
    st.markdown('<div class="text-content">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-heading">Professional Background</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-content">
        Master's candidate in Quantitative and Computational Finance at Georgia Tech with a strong background in 
        Industrial Engineering. Former United States Coast Guard servicemember with experience in intelligence 
        operations and leadership roles.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-heading">Technical Expertise</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-content">
        Proficient in Python, Excel, R, SAS, SQL, and various other programming languages. Experienced in 
        developing quantitative trading strategies, option pricing models, and portfolio optimization techniques. 
        Series 65 certified with hands-on experience in automated trading systems and risk management.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-heading">Project Experience</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-content">
        Led multiple successful projects including development of automated trading systems, option pricing 
        simulations using Heston Model and Jump Diffusion volatility estimates, and stochastic optimization 
        programs for options portfolio management. Experienced in utilizing NLP for market sentiment analysis 
        and volatility prediction.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)