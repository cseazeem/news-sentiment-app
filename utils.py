import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from gtts import gTTS  # Import Google Text-to-Speech
import os  # To play the audio file

def get_news(company_name):
    """Fetch latest news articles from Bing related to a given company and analyze sentiment."""
    search_url = f"https://www.bing.com/news/search?q={company_name}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    print("Response Status Code:", response.status_code)  # Debugging

    if response.status_code != 200:
        print(f"Error fetching news! Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    news_list = []

    for item in soup.find_all("a", {"class": "title"}):
        title = item.get_text()
        link = item["href"]

        # Fix URLs
        if not link.startswith("http"):
            link = "https://www.bing.com" + link  

        # Sentiment Analysis
        sentiment = analyze_sentiment(title)

        news_list.append({"title": title, "link": link, "sentiment": sentiment})

        if len(news_list) >= 10:
            break  

    return news_list

def analyze_sentiment(text):
    """Analyze sentiment of a given text using TextBlob."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity  # -1 (negative) to +1 (positive)

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def comparative_sentiment_analysis(news_list):
    """Compare sentiment of 10 articles and generate a final report."""
    sentiment_count = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for news in news_list:
        sentiment_count[news["sentiment"]] += 1

    total_articles = len(news_list)
    positive = sentiment_count["Positive"]
    negative = sentiment_count["Negative"]
    neutral = sentiment_count["Neutral"]

    # Generate final sentiment summary
    if positive > negative:
        final_sentiment = "Mostly Positive"
    elif negative > positive:
        final_sentiment = "Mostly Negative"
    else:
        final_sentiment = "Neutral"

    return {
        "Total Articles": total_articles,
        "Sentiment Distribution": sentiment_count,
        "Final Sentiment Analysis": final_sentiment
    }

def generate_hindi_audio(text, filename="sentiment_report.mp3"):
    """Convert text to Hindi speech and save as an MP3 file."""
    tts = gTTS(text=text, lang="hi")  # Convert text to Hindi speech
    tts.save(filename)  # Save as MP3 file
    print(f"🔊 Audio saved as {filename}")
    
    # Play the audio file
    os.system(f"start {filename}")  # Windows
    # os.system(f"mpg321 {filename}")  # Linux/Mac (If mpg321 is installed)

if __name__ == "__main__":
    company = input("Enter company name: ")
    print(f"Fetching news for: {company}")

    news = get_news(company)
    
    if not news:
        print("No news articles found.")
    else:
        print("\n--- News Articles with Sentiment ---")
        for n in news:
            print(f"📰 {n['title']}")
            print(f"🔗 {n['link']}")
            print(f"📊 Sentiment: {n['sentiment']}\n")

        # Perform Comparative Sentiment Analysis
        print("\n--- Comparative Sentiment Analysis ---")
        sentiment_report = comparative_sentiment_analysis(news)
        print(sentiment_report)

        # Generate Hindi Speech from Sentiment Report
        hindi_text = f"Company {company} ke total {sentiment_report['Total Articles']} news articles analyze kiye gaye hain. " \
                     f"Jisme {sentiment_report['Sentiment Distribution']['Positive']} positive, " \
                     f"{sentiment_report['Sentiment Distribution']['Negative']} negative, aur " \
                     f"{sentiment_report['Sentiment Distribution']['Neutral']} neutral articles mile hain. " \
                     f"Final sentiment analysis ke anusar, yeh coverage {sentiment_report['Final Sentiment Analysis']} hai."

        print("\n🔊 Generating Hindi Speech...")
        generate_hindi_audio(hindi_text)
