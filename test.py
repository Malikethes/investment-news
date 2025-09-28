import os
import requests
import trafilatura
from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.environ.get("HF_TOKEN")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

QUERY = "investment"
NEWS_API_URL = f"https://newsapi.org/v2/everything?q={QUERY}&language=en&pageSize=5&apiKey={NEWS_API_KEY}"
SUMMARY_API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
SENTIMENT_API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"

HEADERS_HF = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_text(url):
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        print(f"Failed to download: {url}")
        return None
    content = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
    return content if content else None

def summarize(text):
    if not text:
        return None
    payload = {
        "inputs": text[:1024],
        "parameters": {"max_length": 300, "min_length": 30, "do_sample": False}
    }
    response = requests.post(SUMMARY_API_URL, headers=HEADERS_HF, json=payload, timeout=60).json()
    if isinstance(response, list) and "summary_text" in response[0]:
        return response[0]["summary_text"]
    return None

def sentiment_analysis(text):
    if not text:
        return "UNKNOWN"
    payload = {"inputs": text[:512]}
    response = requests.post(
        "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json=payload,
        timeout=60
    ).json()

    print("DEBUG SENTIMENT RESPONSE:", response)

    if isinstance(response, list) and len(response) > 0 and isinstance(response[0], list):
        labels_map = {"LABEL_0": "NEGATIVE", "LABEL_1": "NEUTRAL", "LABEL_2": "POSITIVE"}
        top_label = response[0][0]["label"]  
        return labels_map.get(top_label, "UNKNOWN")
    
    if isinstance(response, dict) and "error" in response:
        print("API Error:", response["error"])
    
    return "UNKNOWN"

if __name__ == "__main__":
    print(sentiment_analysis("I like investing. Stock market is going up!"))

    print("="*80)
    print("MAIN INVESTMENT NEWS SUMMARY".center(80))
    print("="*80)

    news_data = requests.get(NEWS_API_URL).json()
    articles = news_data.get("articles", [])

    for i, article in enumerate(articles, start=1):
        title = article.get("title")
        url = article.get("url")
        description = article.get("description", "")

        text = get_text(url)
        summary = summarize(text) if text else description
        sentiment = sentiment_analysis(summary)

        print(f"\n{'-'*80}")
        print(f"NEWS ITEM {i}".center(80))
        print(f"{'-'*80}\n")

        print(f"Title: {title}\n")
        print(f"Summary:\n{summary}\n")
        print(f"Sentiment / Market Impact: {sentiment}")
        print(f"{'-'*80}\n")
