import streamlit as st

def render_overview():
    """Render the overview tab content"""
    st.markdown("<h2 class='section-header'>Dataset Overview</h2>", unsafe_allow_html=True)
    
    # Dataset preview
    st.markdown("<h3 class='subsection-header'>Data Preview</h3>", unsafe_allow_html=True)
    df_to_display = st.session_state.processed_data if st.session_state.processed_data is not None else st.session_state.data
    st.dataframe(df_to_display.head(10), use_container_width=True)
    
    # Metadata
    st.markdown("<h3 class='subsection-header'>Dataset Metadata</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Rows", value=f"{st.session_state.metadata['rows']:,}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Numerical Columns", value=st.session_state.metadata['numerical_cols'])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Columns", value=st.session_state.metadata['columns'])
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Categorical Columns", value=st.session_state.metadata['categorical_cols'])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Memory Usage", value=f"{st.session_state.metadata['memory_usage']:.2f} MB")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Text Columns", value=st.session_state.metadata['text_cols'])
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Missing values and duplicates
    st.markdown("<h3 class='subsection-header'>Data Quality</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Missing Values", value=f"{st.session_state.metadata['missing_values']:,}")
        missing_percentage = (st.session_state.metadata['missing_values'] / (st.session_state.metadata['rows'] * st.session_state.metadata['columns'])) * 100
        st.progress(min(missing_percentage / 100, 1.0))
        st.caption(f"{missing_percentage:.2f}% of total cells")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(label="Duplicate Rows", value=f"{st.session_state.metadata['duplicates']:,}")
        duplicate_percentage = (st.session_state.metadata['duplicates'] / st.session_state.metadata['rows']) * 100
        st.progress(min(duplicate_percentage / 100, 1.0))
        st.caption(f"{duplicate_percentage:.2f}% of total rows")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Feature lists
    st.markdown("<h3 class='subsection-header'>Feature Categories</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("**Numerical Features:**")
        if st.session_state.numerical_features:
            for feat in st.session_state.numerical_features:
                st.write(f"• {feat}")
        else:
            st.write("No numerical features detected")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("**Categorical Features:**")
        if st.session_state.categorical_features:
            for feat in st.session_state.categorical_features:
                st.write(f"• {feat}")
        else:
            st.write("No categorical features detected")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("**Text Features:**")
        if st.session_state.text_features:
            for feat in st.session_state.text_features:
                st.write(f"• {feat}")
        else:
            st.write("No text features detected")
        st.markdown("</div>", unsafe_allow_html=True)