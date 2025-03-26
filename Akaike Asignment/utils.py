# utils.py
# utils.py

import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS

# Initialize the summarization and sentiment pipelines.
# Note: The first time you run these, the models will download.
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis")

def scrape_news(company: str, num_articles: int = 10):
    """
    Scrapes news articles for the given company using Bing News RSS feed.
    Only non-JS pages are considered.
    """
    url = f"https://www.bing.com/news/search?q={company}&format=rss"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch news from Bing")
    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")
    articles = []
    for item in items[:num_articles]:
        title = item.title.text if item.title else "No Title"
        description = item.description.text if item.description else "No Summary"
        # Summarize the description
        summary_text = summarizer(description, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
        articles.append({
            "title": title,
            "summary": summary_text
        })
    return articles

def perform_sentiment_analysis(articles: list):
    """
    Uses a transformer-based sentiment analyzer on the summary of each article.
    """
    for article in articles:
        result = sentiment_analyzer(article["summary"])
        # The sentiment label is typically "POSITIVE" or "NEGATIVE"
        article["sentiment"] = result[0]['label']
    return articles

def comparative_analysis(articles: list):
    """
    Creates a basic comparative analysis by computing sentiment distribution.
    Returns a string summarizing the distribution.
    """
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        label = article.get("sentiment", "Neutral").capitalize()
        if label in sentiment_counts:
            sentiment_counts[label] += 1
        else:
            sentiment_counts["Neutral"] += 1
    analysis_message = f"Sentiment Distribution: {sentiment_counts}"
    return analysis_message

def generate_tts(articles: list, lang: str = "hi", filename: str = "news_summary.mp3"):
    """
    Combines the article titles and their sentiment results into a summary text,
    then generates a Hindi TTS audio file.
    """
    # Create a summary text from all articles.
    text = " ".join([f"{article['title']} is {article['sentiment']}." for article in articles])
    # Generate audio from the text using gTTS.
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename

# Test functions (optional)
if __name__ == "__main__":
    company = "Tesla"
    print("Scraping news articles...")
    articles = scrape_news(company)
    print("Performing sentiment analysis...")
    articles = perform_sentiment_analysis(articles)
    comp_analysis = comparative_analysis(articles)
    print(comp_analysis)
    audio_file = generate_tts(articles)
    print(f"Generated TTS audio file: {audio_file}")

