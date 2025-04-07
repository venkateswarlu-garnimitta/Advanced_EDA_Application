import streamlit as st
import re
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from textblob import TextBlob
from nltk.util import ngrams
from collections import Counter

def render_text_analysis():
    st.markdown("<h2 class='section-header'>Text Data Analysis</h2>", unsafe_allow_html=True)
    
    if st.session_state.text_features:
        # Choose between original and processed data
        if st.session_state.processed_data is not None:
            data_option = st.radio(
                "Select data to analyze:",
                ["Original Data", "Processed Data"],
                horizontal=True,
                key="text_data_option"
            )
            df_for_text = st.session_state.data if data_option == "Original Data" else st.session_state.processed_data
        else:
            df_for_text = st.session_state.data
        
        # Text column selection
        text_col_options = ["None"] + st.session_state.text_features
        selected_text_col = st.selectbox("Select text column for analysis:", text_col_options, key="text_col_select")
        
        if selected_text_col != "None":
            # Only run text analysis on selected column
            text_data = df_for_text[selected_text_col].dropna().astype(str)
            
            st.markdown("<div class='text-analysis-container'>", unsafe_allow_html=True)
            
            # Create tabs for different text analyses
            text_tabs = st.tabs(["Basic Stats", "Word Cloud", "N-grams", "Sentiment"])
            
            with text_tabs[0]:  # Basic Stats
                st.markdown("<h3 class='subsection-header'>Basic Text Statistics</h3>", unsafe_allow_html=True)
                
                # Calculate text statistics
                text_length = text_data.str.len()
                word_count = text_data.str.split().str.len()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Entries", f"{len(text_data):,}")
                with col2:
                    st.metric("Avg. Characters", f"{text_length.mean():.1f}")
                with col3:
                    st.metric("Avg. Words", f"{word_count.mean():.1f}")
                
                # Text length distribution
                fig = px.histogram(
                    x=text_length, 
                    labels={'x': 'Text Length (characters)', 'y': 'Count'},
                    title="Distribution of Text Length",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Word count distribution
                fig = px.histogram(
                    x=word_count, 
                    labels={'x': 'Word Count', 'y': 'Count'},
                    title="Distribution of Word Count",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with text_tabs[1]:  # Word Cloud
                st.markdown("<h3 class='subsection-header'>Word Cloud</h3>", unsafe_allow_html=True)
                
                # Progress indicator for word cloud generation
                with st.spinner("Generating word cloud..."):
                    # Combine all text
                    all_text = ' '.join(text_data)
                    
                    # Get stop words
                    from nltk.corpus import stopwords
                    stop_words = set(stopwords.words('english'))
                    
                    # Word cloud customization
                    max_words = st.slider("Maximum number of words:", 50, 300, 100)
                    
                    # Generate word cloud
                    wc = WordCloud(
                        width=800, 
                        height=400, 
                        background_color='white',
                        max_words=max_words,
                        stopwords=stop_words
                    ).generate(all_text)
                    
                    # Display word cloud
                    plt.figure(figsize=(10, 5))
                    plt.imshow(wc, interpolation='bilinear')
                    plt.axis("off")
                    plt.tight_layout(pad=0)
                    st.pyplot(plt)
                    
                    # Top words table
                    words = re.findall(r'\b[a-zA-Z]{3,15}\b', all_text.lower())
                    word_freq = Counter(word for word in words if word not in stop_words)
                    top_words = pd.DataFrame(word_freq.most_common(20), columns=['Word', 'Frequency'])
                    
                    st.markdown("<h4>Top 20 Words</h4>", unsafe_allow_html=True)
                    st.dataframe(top_words, use_container_width=True)
            
            with text_tabs[2]:  # N-grams
                st.markdown("<h3 class='subsection-header'>N-grams Analysis</h3>", unsafe_allow_html=True)
                
                # N-gram selection
                n_value = st.radio("Select N-gram size:", [2, 3], horizontal=True)
                
                with st.spinner(f"Generating {n_value}-grams..."):
                    # Combine all text and tokenize
                    all_text = ' '.join(text_data)
                    tokens = nltk.word_tokenize(all_text.lower())
                    
                    # Remove stop words and punctuation
                    from nltk.corpus import stopwords
                    stop_words = set(stopwords.words('english'))
                    filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
                    
                    # Generate n-grams
                    n_grams = list(ngrams(filtered_tokens, n_value))
                    n_gram_freq = Counter(n_grams)
                    
                    # Convert to DataFrame
                    top_n_grams = pd.DataFrame(n_gram_freq.most_common(20), 
                                                columns=['N-gram', 'Frequency'])
                    top_n_grams['N-gram'] = top_n_grams['N-gram'].apply(lambda x: ' '.join(x))
                    
                    # Display bar chart
                    fig = px.bar(
                        top_n_grams, 
                        x='Frequency', 
                        y='N-gram',
                        orientation='h',
                        title=f"Top {n_value}-grams",
                        template="plotly_white"
                    )
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display data table
                    st.dataframe(top_n_grams, use_container_width=True)
            
            with text_tabs[3]:  # Sentiment
                st.markdown("<h3 class='subsection-header'>Sentiment Analysis</h3>", unsafe_allow_html=True)
                
                with st.spinner("Analyzing sentiment..."):
                    # Process all rows instead of sampling
                    sentiments = []
                    for text in text_data:
                        analysis = TextBlob(text)
                        sentiments.append({
                            'text': text[:100] + '...' if len(text) > 100 else text,
                            'polarity': analysis.sentiment.polarity,
                            'subjectivity': analysis.sentiment.subjectivity
                        })
                    
                    sentiment_df = pd.DataFrame(sentiments)
                    
                    # Add sentiment categories
                    def categorize_sentiment(polarity):
                        if polarity > 0.3:
                            return "Positive"
                        elif polarity < -0.3:
                            return "Negative"
                        else:
                            return "Neutral"
                    
                    sentiment_df['sentiment'] = sentiment_df['polarity'].apply(categorize_sentiment)
                    
                    # Display table with sentiment scores for each record
                    st.markdown("<h4>Sentiment Analysis Results (All Records)</h4>", unsafe_allow_html=True)
                    
                    # Format the table for better readability
                    display_df = sentiment_df.copy()
                    display_df['polarity'] = display_df['polarity'].round(2)
                    display_df['subjectivity'] = display_df['subjectivity'].round(2)
                    display_df = display_df[['text', 'polarity', 'subjectivity', 'sentiment']]
                    display_df.columns = ['Text', 'Polarity', 'Subjectivity', 'Sentiment']
                    
                    # Apply styling to the table based on sentiment
                    def highlight_sentiment(val):
                        if val == 'Positive':
                            return 'background-color: rgba(0, 128, 0, 0.2)'
                        elif val == 'Negative':
                            return 'background-color: rgba(255, 0, 0, 0.2)'
                        else:
                            return 'background-color: rgba(128, 128, 128, 0.2)'
                    
                    # Display the styled table with pagination
                    styled_df = display_df.style.applymap(highlight_sentiment, subset=['Sentiment'])
                    st.dataframe(styled_df, use_container_width=True, height=400)
                    
                    # Add download button for the full results
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Full Results as CSV",
                        data=csv,
                        file_name="sentiment_analysis_results.csv",
                        mime="text/csv",
                    )
                    
                    # Display bar chart of sentiment counts
                    st.markdown("<h4>Sentiment Distribution</h4>", unsafe_allow_html=True)
                    
                    sentiment_counts = sentiment_df['sentiment'].value_counts().reset_index()
                    sentiment_counts.columns = ['Sentiment', 'Count']
                    
                    # Create a bar chart using plotly
                    fig = px.bar(
                        sentiment_counts,
                        x='Sentiment',
                        y='Count',
                        color='Sentiment',
                        color_discrete_map={'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'},
                        title="Sentiment Distribution",
                        template="plotly_white"
                    )
                    
                    # Customize the layout
                    fig.update_layout(
                        xaxis_title="Sentiment Category",
                        yaxis_title="Number of Records",
                        legend_title="Sentiment"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display summary statistics
                    st.markdown("<h4>Summary Statistics</h4>", unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        positive_count = (sentiment_df['sentiment'] == 'Positive').sum()
                        positive_percent = (positive_count / len(sentiment_df) * 100).round(1)
                        st.metric("Positive", f"{positive_count} ({positive_percent}%)")
                    
                    with col2:
                        neutral_count = (sentiment_df['sentiment'] == 'Neutral').sum()
                        neutral_percent = (neutral_count / len(sentiment_df) * 100).round(1)
                        st.metric("Neutral", f"{neutral_count} ({neutral_percent}%)")
                    
                    with col3:
                        negative_count = (sentiment_df['sentiment'] == 'Negative').sum()
                        negative_percent = (negative_count / len(sentiment_df) * 100).round(1)
                        st.metric("Negative", f"{negative_count} ({negative_percent}%)")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Please select a text column to analyze")
    else:
        st.info("No text features detected in the dataset")
