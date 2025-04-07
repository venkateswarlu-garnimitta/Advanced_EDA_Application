import streamlit as st
import pandas as pd
import nltk
from config import REQUIRED_NLTK_RESOURCES

def initialize_session_state():
    """Initialize session state variables if not already defined"""
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'numerical_features' not in st.session_state:
        st.session_state.numerical_features = []
    if 'categorical_features' not in st.session_state:
        st.session_state.categorical_features = []
    if 'text_features' not in st.session_state:
        st.session_state.text_features = []
    if 'metadata' not in st.session_state:
        st.session_state.metadata = {}
    if 'descriptive_stats' not in st.session_state:
        st.session_state.descriptive_stats = {}

def download_dependencies():
    """Download required NLTK and spaCy resources"""
    # Download NLTK resources
    for resource in REQUIRED_NLTK_RESOURCES:
        try:
            nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)

   

def load_data(uploaded_file):
    """Load data from uploaded file and initialize features"""
    try:
        
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        
        st.session_state.data = data.copy()
        
        # Segregate features
        numerical_features = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = data.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        
        # Identify text features
        text_features = []
        for col in categorical_features[:]:  # Use a copy for iteration
            if data[col].nunique() > data.shape[0] * 0.3:  # More than 30% unique values
                text_features.append(col)
                categorical_features.remove(col)
            elif data[col].astype(str).str.len().mean() > 30:  # Average length > 30 chars
                text_features.append(col)
                categorical_features.remove(col)
        
        st.session_state.numerical_features = numerical_features
        st.session_state.categorical_features = categorical_features
        st.session_state.text_features = text_features
        
        # Calculate metadata
        st.session_state.metadata = {
            'rows': data.shape[0],
            'columns': data.shape[1],
            'duplicates': data.duplicated().sum(),
            'missing_values': data.isnull().sum().sum(),
            'memory_usage': data.memory_usage(deep=True).sum() / (1024 * 1024),  # MB
            'numerical_cols': len(numerical_features),
            'categorical_cols': len(categorical_features),
            'text_cols': len(text_features)
        }
        
        # Calculate descriptive stats
        st.session_state.descriptive_stats = data.describe(include='all')
        
        return True
        
    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.data = None
        return False