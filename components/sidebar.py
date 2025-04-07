import streamlit as st
from utils.data_loader import load_data, download_dependencies
from utils.data_processor import preprocess_data

def render_sidebar():
    """Render the sidebar with data loading and preprocessing options"""
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #1E40AF;margin-top:-3rem;'>Controls</h2>", unsafe_allow_html=True)
        download_dependencies()
        # File uploader
        uploaded_file = st.file_uploader("Upload your dataset (CSV, Excel)", type=['csv', 'xlsx'])
        
        if uploaded_file is not None:
            # Load data
            load_data(uploaded_file)
        
        if st.session_state.data is not None:
            st.markdown("### Preprocessing Options")
            
            # Handle missing values
            st.subheader("Handle Missing Values")
            numerical_strategy = st.selectbox(
                "Fill missing values in numerical features:",
                ["Mean", "Median", "Zero", "None"],
                key="num_strategy"
            )
            
            categorical_strategy = st.selectbox(
                "Fill missing values in categorical features:",
                ["Mode", "Missing", "None"],
                key="cat_strategy"
            )
            
            # Handle duplicates
            st.subheader("Handle Duplicates")
            duplicate_strategy = st.selectbox(
                "Handle duplicate rows:",
                ["Remove duplicates", "Keep duplicates"],
                key="dup_strategy"
            )
            
            # Preprocessing button
            if st.button("Preprocess Data"):
                with st.spinner("Preprocessing data..."):
                    processed_data = preprocess_data(
                        st.session_state.data,
                        numerical_strategy,
                        categorical_strategy,
                        duplicate_strategy
                    )
                    
                    if processed_data is not None:
                        st.session_state.processed_data = processed_data
                        st.success("Preprocessing completed!")
                        
        # Download preprocessed Data
        if st.session_state.processed_data is not None:
            processed_data = st.session_state.processed_data
            if st.download_button("Download Preprocessed Data",
                                    data=processed_data.to_csv(index=False), 
                                    file_name="preprocessed_data.csv"):
                st.success("Download started!")
                
            
       