import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        footer {
                visibility: hidden;
                }
        header {
                visibility: hidden;
                }
        .stAppToolbar.st-emotion-cache-15ecox0.e4hpqof2 {
        DISPLAY: NONE;
                }
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: red;
            text-align: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #3B82F6;
           
        }
        .stMainBlockContainer{
                margin-top: -5rem;}
        .stElementContainer{
                margin-top:1rem;
                }
        .section-header {
            font-size: 1.8rem;
            font-weight: 600;
            color: #1E40AF;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #93C5FD;
        }
        .subsection-header {
            font-size: 1.4rem;
            font-weight: 600;
            color: #2563EB;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        .metric-container {
            background-color: #EFF6FF;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #3B82F6;
        }
        .stPlotlyChart {
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 1rem;
        }
        .stDataFrame {
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 1rem;
        }
        .text-analysis-container {
            background-color: #F0F9FF;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #0EA5E9;
        }
        
    </style>
    """, unsafe_allow_html=True)