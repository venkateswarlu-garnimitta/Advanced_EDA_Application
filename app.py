import streamlit as st
from streamlit_option_menu import option_menu   # type: ignore
import warnings
from config import setup_page_config
from styles.custom_styles import apply_custom_styles
from utils.data_loader import initialize_session_state
from components.sidebar import render_sidebar
from components.overview import render_overview
from components.data_analysis import render_data_analysis
from components.visualizations import render_visualizations
from components.text_analysis import render_text_analysis
from utils.get_pdf_report import setup_pdf_download_button
warnings.filterwarnings('ignore')

def main():
    # Setup page configuration
    setup_page_config()
    
    # Apply custom CSS styles
    apply_custom_styles()
    
    # Initialize session state variables
    initialize_session_state()
    
    # Main title
    st.markdown("<h1 class='main-header'>Advanced EDA & Preprocessing Tool</h1>", unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    if st.session_state.data is not None:
        # Create tabs for organization
        tabs = option_menu(
            menu_title=None,
            options=["Overview", "Data Analysis", "Visualizations", "Text Analysis"],
            icons=["clipboard-data", "table", "bar-chart-line", "chat-square-text"],
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "margin": "0!important"},
                "icon": {"font-size": "14px"},
                "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#eee","padding-top":"7px","padding-bottom":"7px"},
                "nav-link-selected": {"background-color": "#1E40AF"},
            }
        )
        
        
        # Render appropriate tab content
        if tabs == "Overview":
            render_overview()
        elif tabs == "Data Analysis":
            render_data_analysis()
        elif tabs == "Visualizations":
            render_visualizations()
        elif tabs == "Text Analysis":
            render_text_analysis()
        setup_pdf_download_button()
    else:
        # Welcome screen
        st.markdown("""
        <div style="text-align: center; margin-top:30px;">
            <h1 style="color: #1E40AF;">Welcome to Advanced EDA & Preprocessing Tool!</h1>
            <p style="font-size: 1.2rem; margin-top:10px;">Upload your dataset using the sidebar to get started.</p>
            <div style="margin-top: 50px;">
                <ul style="list-style-type: none; padding: 0;">
                    <li style="margin: 10px 0;"><span style="background-color: #E0F2FE; padding: 5px 10px; border-radius: 5px; font-weight:bold;">📊 Visualization</span> Generate insightful visualizations automatically</li>
                    <li style="margin: 10px 0;"><span style="background-color: #E0F2FE; padding: 5px 10px; border-radius: 5px; font-weight:bold;">🔍 Analysis</span> Get detailed statistics about your data</li>
                    <li style="margin: 10px 0;"><span style="background-color: #E0F2FE; padding: 5px 10px; border-radius: 5px;font-weight:bold;">🧹 Preprocessing</span> Clean and prepare your data for modeling</li>
                    <li style="margin: 10px 0;"><span style="background-color: #E0F2FE; padding: 5px 10px; border-radius: 5px; font-weight:bold;">📝 Report</span> Generate PDF reports of your findings</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    

if __name__ == "__main__":
    main()