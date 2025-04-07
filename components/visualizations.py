import streamlit as st
import pandas as pd
import plotly.express as px

def render_visualizations():
    """Render the visualizations tab content"""
    st.markdown("<h2 class='section-header'>Data Visualizations</h2>", unsafe_allow_html=True)
    
    # Choose between original and processed data
    if st.session_state.processed_data is not None:
            data_option = st.radio(
                "Select data to visualize:",
                ["Original Data", "Processed Data"],
                horizontal=True,
                key="viz_data_option"
            )
            df_to_visualize = st.session_state.data if data_option == "Original Data" else st.session_state.processed_data
    else:
        df_to_visualize = st.session_state.data
    
    # Numerical Visualizations
    if st.session_state.numerical_features:
        st.markdown("<h3 class='subsection-header'>Numerical Features</h3>", unsafe_allow_html=True)
        
        viz_num_options = ["Distribution Plots", "Box Plots", "Scatter Plots"]
        viz_num_selection = st.selectbox("Select visualization type:", viz_num_options, key="num_viz_type")
        
        if viz_num_selection == "Distribution Plots":
            cols = st.columns(2)
            for i, col_name in enumerate(st.session_state.numerical_features):
                with cols[i % 2]:
                    fig = px.histogram(df_to_visualize, x=col_name, marginal="box", 
                                        title=f"Distribution of {col_name}",
                                        template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
        
        elif viz_num_selection == "Box Plots":
            cols = st.columns(2)
            for i, col_name in enumerate(st.session_state.numerical_features):
                with cols[i % 2]:
                    fig = px.box(df_to_visualize, y=col_name, 
                                title=f"Box Plot of {col_name}",
                                template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
        
        elif viz_num_selection == "Scatter Plots":
            if len(st.session_state.numerical_features) >= 2:
                x_feature = st.selectbox("Select X-axis feature:", st.session_state.numerical_features, key="scatter_x")
                y_feature = st.selectbox("Select Y-axis feature:", 
                                        [f for f in st.session_state.numerical_features if f != x_feature], 
                                        key="scatter_y")
                
                # Optional color by categorical
                color_by = None
                if st.session_state.categorical_features:
                    color_options = ["None"] + st.session_state.categorical_features
                    color_selection = st.selectbox("Color by (optional):", color_options, key="scatter_color")
                    if color_selection != "None":
                        color_by = color_selection
                
                fig = px.scatter(df_to_visualize, x=x_feature, y=y_feature, color=color_by,
                                title=f"Scatter Plot: {x_feature} vs {y_feature}",
                                template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 numerical features for scatter plots")
    else:
        st.info("No numerical features available for visualization")
    
    # Categorical Visualizations
    if st.session_state.categorical_features:
        st.markdown("<h3 class='subsection-header'>Categorical Features</h3>", unsafe_allow_html=True)
        
        viz_cat_options = ["Bar Charts", "Pie Charts", "Count Plots by Category"]
        viz_cat_selection = st.selectbox("Select visualization type:", viz_cat_options, key="cat_viz_type")
        
        if viz_cat_selection == "Bar Charts":
            cols = st.columns(2)
            for i, col_name in enumerate(st.session_state.categorical_features):
                with cols[i % 2]:
                    value_counts = df_to_visualize[col_name].value_counts().head(10)
                    fig = px.bar(x=value_counts.index, y=value_counts.values, 
                                labels={'x': col_name, 'y': 'Count'},
                                title=f"Top 10 values for {col_name}",
                                template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
        
        elif viz_cat_selection == "Pie Charts":
            cols = st.columns(2)
            for i, col_name in enumerate(st.session_state.categorical_features):
                with cols[i % 2]:
                    value_counts = df_to_visualize[col_name].value_counts().head(8)
                    
                    # If we have too many categories, show top 7 and group the rest
                    if df_to_visualize[col_name].nunique() > 8:
                        others_count = df_to_visualize[col_name].value_counts().iloc[8:].sum()
                        value_counts = pd.concat([value_counts, pd.Series([others_count], index=["Others"])])
                    
                    fig = px.pie(values=value_counts.values, names=value_counts.index,
                                title=f"Distribution of {col_name}",
                                template="plotly_white")
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
        
        elif viz_cat_selection == "Count Plots by Category":
            if len(st.session_state.categorical_features) >= 2:
                x_feature = st.selectbox("Select primary category:", st.session_state.categorical_features, key="count_x")
                color_feature = st.selectbox("Select secondary category:", 
                                            [f for f in st.session_state.categorical_features if f != x_feature], 
                                            key="count_color")
                
                # Limit to top categories for readability
                top_x_cats = df_to_visualize[x_feature].value_counts().head(8).index
                filtered_df = df_to_visualize[df_to_visualize[x_feature].isin(top_x_cats)]
                
                fig = px.histogram(filtered_df, x=x_feature, color=color_feature,
                                    title=f"Count Plot: {x_feature} by {color_feature}",
                                    template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 categorical features for this visualization")
    else:
        st.info("No categorical features available for visualization")
    
    # Relationships Between Numerical and Categorical
    if st.session_state.numerical_features and st.session_state.categorical_features:
        st.markdown("<h3 class='subsection-header'>Relationships Between Numerical and Categorical</h3>", unsafe_allow_html=True)
        
        num_feature = st.selectbox("Select numerical feature:", st.session_state.numerical_features, key="relation_num")
        cat_feature = st.selectbox("Select categorical feature:", st.session_state.categorical_features, key="relation_cat")
        
        # Limit to top categories for readability
        top_cats = df_to_visualize[cat_feature].value_counts().head(10).index
        filtered_df = df_to_visualize[df_to_visualize[cat_feature].isin(top_cats)]
        
        viz_relation_options = ["Box Plot", "Violin Plot", "Bar Plot (Mean)"]
        viz_relation_selection = st.selectbox("Select visualization type:", viz_relation_options, key="relation_viz_type")
        
        if viz_relation_selection == "Box Plot":
            fig = px.box(filtered_df, x=cat_feature, y=num_feature, 
                        title=f"{num_feature} by {cat_feature}",
                        template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_relation_selection == "Violin Plot":
            fig = px.violin(filtered_df, x=cat_feature, y=num_feature, 
                            box=True, points="all",
                            title=f"{num_feature} by {cat_feature}",
                            template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_relation_selection == "Bar Plot (Mean)":
            mean_by_cat = filtered_df.groupby(cat_feature)[num_feature].mean().sort_values(ascending=False)
            fig = px.bar(x=mean_by_cat.index, y=mean_by_cat.values,
                        labels={'x': cat_feature, 'y': f'Mean {num_feature}'},
                        title=f"Mean {num_feature} by {cat_feature}",
                        template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)