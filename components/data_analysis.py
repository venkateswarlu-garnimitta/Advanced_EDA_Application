import streamlit as st
import pandas as pd
import plotly.express as px

def render_data_analysis():
    """Render the data analysis tab content"""
    st.markdown("<h2 class='section-header'>Detailed Data Analysis</h2>", unsafe_allow_html=True)
    
    # Choose between original and processed data
    if st.session_state.processed_data is not None:
        data_option = st.radio(
            "Select data to analyze:",
            ["Original Data", "Processed Data"],
            horizontal=True
        )
        df_to_analyze = st.session_state.data if data_option == "Original Data" else st.session_state.processed_data
    else:
        df_to_analyze = st.session_state.data
        
    # Descriptive Statistics
    st.markdown("<h3 class='subsection-header'>Descriptive Statistics</h3>", unsafe_allow_html=True)
    
    # Create tabs for numerical and categorical stats
    stats_tab1, stats_tab2 = st.tabs(["Numerical Statistics", "Categorical Statistics"])
    
    with stats_tab1:
        if st.session_state.numerical_features:
            num_stats = df_to_analyze[st.session_state.numerical_features].describe().T
            num_stats['range'] = num_stats['max'] - num_stats['min']
            num_stats['missing'] = df_to_analyze[st.session_state.numerical_features].isnull().sum().values
            num_stats['missing_pct'] = (df_to_analyze[st.session_state.numerical_features].isnull().sum() / len(df_to_analyze) * 100).values
            num_stats = num_stats.round(2)
            
            st.dataframe(num_stats, use_container_width=True)
        else:
            st.info("No numerical features available for statistics")
    
    with stats_tab2:
        if st.session_state.categorical_features:
            cat_stats = pd.DataFrame(index=st.session_state.categorical_features)
            cat_stats['unique_values'] = [df_to_analyze[col].nunique() for col in st.session_state.categorical_features]
            cat_stats['missing'] = df_to_analyze[st.session_state.categorical_features].isnull().sum().values
            cat_stats['missing_pct'] = (df_to_analyze[st.session_state.categorical_features].isnull().sum() / len(df_to_analyze) * 100).values.round(2)
            cat_stats['most_common'] = [df_to_analyze[col].value_counts().index[0] if not df_to_analyze[col].value_counts().empty else None for col in st.session_state.categorical_features]
            cat_stats['most_common_count'] = [df_to_analyze[col].value_counts().values[0] if not df_to_analyze[col].value_counts().empty else None for col in st.session_state.categorical_features]
            cat_stats['most_common_pct'] = [(df_to_analyze[col].value_counts().values[0] / df_to_analyze[col].count() * 100).round(2) if not df_to_analyze[col].value_counts().empty else None for col in st.session_state.categorical_features]
            
            st.dataframe(cat_stats, use_container_width=True)
        else:
            st.info("No categorical features available for statistics")
    
    # Feature Details
    st.markdown("<h3 class='subsection-header'>Feature Details</h3>", unsafe_allow_html=True)
    
    # Create feature selection
    all_features = st.session_state.numerical_features + st.session_state.categorical_features
    if all_features:
        selected_feature = st.selectbox("Select feature for detailed analysis:", all_features)
        
        # Get feature information
        feature_data = df_to_analyze[selected_feature]
        feature_type = "Numerical" if selected_feature in st.session_state.numerical_features else "Categorical"
        
        # Feature metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.metric("Type", feature_type)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.metric("Unique Values", feature_data.nunique())
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            missing_count = feature_data.isnull().sum()
            missing_pct = (missing_count / len(feature_data) * 100).round(2)
            st.metric("Missing Values", f"{missing_count} ({missing_pct}%)")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col4:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            if feature_type == "Numerical":
                st.metric("Range", f"{feature_data.min()} to {feature_data.max()}")
            else:
                top_value = feature_data.value_counts().index[0] if not feature_data.value_counts().empty else "N/A"
                st.metric("Most Common", top_value)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Feature visualization
        if feature_type == "Numerical":
            fig = px.histogram(df_to_analyze, x=selected_feature, marginal="box", 
                              title=f"Distribution of {selected_feature}",
                              template="plotly_white")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Categorical
            value_counts = feature_data.value_counts().sort_values(ascending=False).head(10)
            fig = px.bar(x=value_counts.index, y=value_counts.values, 
                       labels={'x': selected_feature, 'y': 'Count'},
                       title=f"Top 10 values for {selected_feature}",
                       template="plotly_white")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No features available for detailed analysis")
    
    # Correlation Analysis
    if len(st.session_state.numerical_features) > 1:
        st.markdown("<h3 class='subsection-header'>Correlation Analysis</h3>", unsafe_allow_html=True)
        
        corr = df_to_analyze[st.session_state.numerical_features].corr()
        
        fig = px.imshow(corr, 
                      labels=dict(color="Correlation"),
                      x=corr.columns, 
                      y=corr.columns,
                      color_continuous_scale="RdBu_r",
                      title="Correlation Matrix",
                      template="plotly_white")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top correlations
        corr_pairs = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                corr_pairs.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))
        corr_pairs = sorted(corr_pairs, key=lambda x: abs(x[2]), reverse=True)
        
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("**Top 5 Feature Correlations:**")
        
        for i, (feat1, feat2, corr_val) in enumerate(corr_pairs[:5]):
            sign = "positive" if corr_val > 0 else "negative"
            st.write(f"{i+1}. **{feat1}** and **{feat2}**: {corr_val:.3f} ({sign})")
        
        st.markdown("</div>", unsafe_allow_html=True)