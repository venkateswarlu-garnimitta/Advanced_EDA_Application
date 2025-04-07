import time
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import streamlit as st
import tempfile
import os

def generate_pdf_report(data, metadata, numerical_features, categorical_features, text_features):
    """
    Generate a comprehensive PDF report with statistics and visualizations.
    Pre-generates the report and stores it in session state for quick download.
    """
    # Create PDF object with smaller margins to use more of the page
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    
    # Set up PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Dataset Analysis Report", ln=True, align="C")
    
    # Add timestamp in smaller font
    pdf.set_font("Arial", "", 8)
    pdf.cell(190, 5, f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    
    # Dataset information - compact format
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Dataset Overview", ln=True)
    
    # Dataset metadata in a compact table
    pdf.set_font("Arial", "", 10)
    pdf.cell(45, 6, f"Rows: {metadata['rows']}", border=1)
    pdf.cell(45, 6, f"Columns: {metadata['columns']}", border=1)
    pdf.cell(50, 6, f"Missing: {metadata['missing_values']}", border=1)
    pdf.cell(50, 6, f"Duplicates: {metadata['duplicates']}", border=1, ln=True)
    
    # Feature type counts in a compact row
    pdf.cell(63, 6, f"Numerical: {len(numerical_features)}", border=1)
    pdf.cell(63, 6, f"Categorical: {len(categorical_features)}", border=1)
    pdf.cell(64, 6, f"Text: {len(text_features)}", border=1, ln=True)
    pdf.ln(5)
    
    # Feature lists - more compact presentation
    if numerical_features:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(190, 6, "Numerical Features:", ln=True)
        pdf.set_font("Arial", "", 8)
        features_text = ", ".join(numerical_features)
        pdf.multi_cell(190, 4, features_text)
    
    if categorical_features:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(190, 6, "Categorical Features:", ln=True)
        pdf.set_font("Arial", "", 8)
        features_text = ", ".join(categorical_features)
        pdf.multi_cell(190, 4, features_text)
    
    if text_features:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(190, 6, "Text Features:", ln=True)
        pdf.set_font("Arial", "", 8)
        features_text = ", ".join(text_features)
        pdf.multi_cell(190, 4, features_text)
    
    pdf.ln(5)
    
    # Data Preview section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 8, "Data Preview", 0, 1, 'L')
    
    # Create data preview table
    df_preview = data.head(5)
    
    # Table header
    pdf.set_font("Arial", "B", 7)
    col_width = 190 / min(len(df_preview.columns), 8)  # Limit columns if too many
    
    # Show only up to 8 columns to prevent overflow
    display_cols = list(df_preview.columns)[:8]
    
    for col in display_cols:
        col_name = str(col)[:10] + "..." if len(str(col)) > 10 else str(col)
        pdf.cell(col_width, 6, col_name, border=1)
    pdf.ln()
    
    # Table rows
    pdf.set_font("Arial", "", 7)
    for i, row in df_preview.iterrows():
        for col in display_cols:
            val = row[col]
            if isinstance(val, (int, float)):
                val_str = f"{val:.2f}" if isinstance(val, float) else str(val)
            else:
                val_str = str(val)
                
            # Truncate if too long
            if len(val_str) > 10:
                val_str = val_str[:10] + "..."
                
            pdf.cell(col_width, 6, val_str, border=1)
        pdf.ln()
    
    # Add note if there are more columns
    if len(df_preview.columns) > 8:
        pdf.set_font("Arial", "I", 7)
        pdf.cell(190, 4, f"Note: Only showing 8 of {len(df_preview.columns)} columns", ln=True)
    
    pdf.ln(5)
    
    # Numerical Statistics
    if numerical_features:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 8, "Numerical Statistics", ln=True)
        
        # Get statistics
        num_stats = data[numerical_features].describe().round(2).T
        # Select only key statistics to save space
        stats_to_show = ['count', 'mean', 'std', 'min', 'max']
        num_stats = num_stats[stats_to_show]
        
        # Create a more compact table
        pdf.set_font("Arial", "B", 7)
        
        # Calculate column widths
        feat_width = 40
        stat_width = 30
        
        # Header row
        pdf.cell(feat_width, 6, "Feature", border=1)
        for stat in stats_to_show:
            pdf.cell(stat_width, 6, stat, border=1)
        pdf.ln()
        
        # Data rows
        pdf.set_font("Arial", "", 7)
        for feature in num_stats.index:
            # Feature name (possibly truncated)
            feat_name = str(feature)[:15] + "..." if len(str(feature)) > 15 else str(feature)
            pdf.cell(feat_width, 6, feat_name, border=1)
            
            # Stats
            for stat in stats_to_show:
                val = num_stats.loc[feature, stat]
                val_str = f"{val:.2f}" if isinstance(val, float) else str(val)
                pdf.cell(stat_width, 6, val_str, border=1)
            pdf.ln()
        
        pdf.ln(5)
        
        # Generate histograms for numerical features (up to 6)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 8, "Numerical Distributions", ln=True)
        
        # Create a temporary directory for the images
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create histograms (up to 6 for space considerations)
            for i, feature in enumerate(numerical_features[:6]):
                # Create histogram using seaborn
                plt.figure(figsize=(5, 3))
                sns.histplot(data[feature].dropna(), kde=True)
                plt.title(f"Distribution of {feature}")
                plt.tight_layout()
                
                # Save to temporary file
                temp_img_path = os.path.join(tmpdirname, f"hist_{i}.png")
                plt.savefig(temp_img_path, format='png', dpi=100)
                plt.close()
                
                # Calculate position for 2 columns of plots
                if i % 2 == 0:
                    pdf.cell(95, 5, f"{feature}", ln=False)
                    x = pdf.get_x()
                    y = pdf.get_y()
                    pdf.cell(95, 5, "", ln=True)
                    pdf.image(temp_img_path, x=10, y=y+5, w=90)
                else:
                    pdf.cell(95, 5, f"{feature}", ln=True)
                    pdf.image(temp_img_path, x=110, y=y+5, w=90)
                    pdf.ln(50)  # Space for the plots
            
            # Add a page break only if there's an odd number of plots
            if len(numerical_features[:6]) % 2 != 0:
                pdf.ln(50)
    
    # Categorical Statistics
    if categorical_features:
        # Check if we need a new page based on content so far
        if pdf.get_y() > 200:
            pdf.add_page()
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 8, "Categorical Statistics", ln=True)
        
        # For each categorical feature, show frequency table (up to 5 features)
        for i, feature in enumerate(categorical_features[:5]):
            pdf.set_font("Arial", "B", 10)
            pdf.cell(190, 6, f"{feature} Value Counts:", ln=True)
            
            # Get value counts
            value_counts = data[feature].value_counts().head(8)  # Show top 8 values
            
            # Create a table
            pdf.set_font("Arial", "", 8)
            
            # Header
            pdf.cell(95, 6, "Value", border=1)
            pdf.cell(95, 6, "Count", border=1, ln=True)
            
            # Rows
            for val, count in value_counts.items():
                val_str = str(val)
                if len(val_str) > 25:
                    val_str = val_str[:22] + "..."
                
                pdf.cell(95, 6, val_str, border=1)
                pdf.cell(95, 6, str(count), border=1, ln=True)
            
            # Add note if there are more values
            if len(data[feature].unique()) > 8:
                pdf.set_font("Arial", "I", 7)
                pdf.cell(190, 4, f"Note: Only showing top 8 of {len(data[feature].unique())} unique values", ln=True)
            
            pdf.ln(5)
        
        # Generate bar charts for categorical features (up to 4)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 8, "Categorical Distributions", ln=True)
        
        # Create a temporary directory for the images
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create bar charts (up to 4 for space considerations)
            for i, feature in enumerate(categorical_features[:4]):
                # Get top 8 categories for readability
                top_cats = data[feature].value_counts().head(8)
                
                # Create bar chart using seaborn
                plt.figure(figsize=(5, 3))
                sns.barplot(x=top_cats.index, y=top_cats.values)
                plt.title(f"Top values: {feature}")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                # Save to temporary file
                temp_img_path = os.path.join(tmpdirname, f"bar_{i}.png")
                plt.savefig(temp_img_path, format='png', dpi=100)
                plt.close()
                
                # Position plots
                if i % 2 == 0:
                    pdf.cell(95, 5, f"{feature}", ln=False)
                    x = pdf.get_x()
                    y = pdf.get_y()
                    pdf.cell(95, 5, "", ln=True)
                    pdf.image(temp_img_path, x=10, y=y+5, w=90)
                else:
                    pdf.cell(95, 5, f"{feature}", ln=True)
                    pdf.image(temp_img_path, x=110, y=y+5, w=90)
                    pdf.ln(50)  # Space for the plots
    
    # Footer
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Page {pdf.page_no()}", 0, 0, "C")
    
    # Return the PDF bytes
    return pdf.output(dest='S').encode('latin1')

# The function to be called from your Streamlit app
def setup_pdf_download_button():
    """Set up a simple one-click PDF download button using Streamlit's download_button"""
    if 'data' in st.session_state and st.session_state.data is not None:
        # Check if PDF is already generated
        if 'pdf_data' not in st.session_state:
           
            try:
                # Generate the PDF and store in session state
                pdf_data = generate_pdf_report(
                    st.session_state.data,
                    st.session_state.metadata,
                    st.session_state.numerical_features,
                    st.session_state.categorical_features,
                    st.session_state.text_features
                )
                
                # Store raw bytes in session state
                st.session_state.pdf_data = pdf_data
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
                return
        
        # Display simple download button
        st.download_button(
            label="Download PDF Report",
            data=st.session_state.pdf_data,
            file_name="data_analysis_report.pdf",
            mime="application/pdf",
            key="download_pdf_button"
        )