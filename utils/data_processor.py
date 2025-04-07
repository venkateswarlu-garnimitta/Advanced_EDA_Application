import streamlit as st


def preprocess_data(data, num_strategy, cat_strategy, duplicate_strategy):
    """Preprocess data based on selected strategies"""
    try:
        # Create a copy of the original data
        processed_data = data.copy()
        
        # Handle duplicates
        if duplicate_strategy == "Remove duplicates":
            initial_rows = processed_data.shape[0]
            processed_data = processed_data.drop_duplicates()
            
        
        # Handle missing values in numerical features
        for col in st.session_state.numerical_features:
            if processed_data[col].isnull().sum() > 0:
                if num_strategy == "Mean":
                    processed_data[col] = processed_data[col].fillna(processed_data[col].mean())
                elif num_strategy == "Median":
                    processed_data[col] = processed_data[col].fillna(processed_data[col].median())
                elif num_strategy == "Zero":
                    processed_data[col] = processed_data[col].fillna(0)
        
        # Handle missing values in categorical features
        for col in st.session_state.categorical_features:
            if processed_data[col].isnull().sum() > 0:
                if cat_strategy == "Mode":
                    processed_data[col] = processed_data[col].fillna(processed_data[col].mode()[0])
                elif cat_strategy == "Missing":
                    processed_data[col] = processed_data[col].fillna("Missing")
        
        return processed_data
        
    except Exception as e:
        st.error(f"Error during preprocessing: {e}")
        return None