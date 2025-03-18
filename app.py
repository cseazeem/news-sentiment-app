import streamlit as st
from utils import get_news, comparative_sentiment_analysis, generate_hindi_audio

# Streamlit App Title
st.title("📰 Company News Sentiment Analysis")

# User Input for Company Name
company_name = st.text_input("Enter Company Name", "Tesla")

if st.button("Analyze News"):
    with st.spinner("Fetching news and analyzing sentiment..."):
        news = get_news(company_name)

        if not news:
            st.error("No news articles found! Try another company.")
        else:
            # Display News Articles with Sentiment
            st.subheader(f"🔍 Top 10 News Articles for {company_name}")
            for n in news:
                st.markdown(f"**📰 {n['title']}**")
                st.markdown(f"📊 Sentiment: `{n['sentiment']}`")
                st.markdown(f"[🔗 Read More]({n['link']})")
                st.write("---")

            # Perform Comparative Sentiment Analysis
            sentiment_report = comparative_sentiment_analysis(news)

            # Display Sentiment Summary
            st.subheader("📊 Sentiment Analysis Report")
            st.json(sentiment_report)

            # Generate Hindi Speech Report
            hindi_text = f"Company {company_name} ke total {sentiment_report['Total Articles']} news articles analyze kiye gaye hain. " \
                         f"Jisme {sentiment_report['Sentiment Distribution']['Positive']} positive, " \
                         f"{sentiment_report['Sentiment Distribution']['Negative']} negative, aur " \
                         f"{sentiment_report['Sentiment Distribution']['Neutral']} neutral articles mile hain. " \
                         f"Final sentiment analysis ke anusar, yeh coverage {sentiment_report['Final Sentiment Analysis']} hai."

            st.subheader("🔊 Hindi Audio Summary")
            generate_hindi_audio(hindi_text, "sentiment_report.mp3")
            audio_file = open("sentiment_report.mp3", "rb")
            st.audio(audio_file, format="audio/mp3")
