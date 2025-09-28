# Investment News Summarizer

This project collects news articles related to the keyword `investment`, summarizes them, and performs sentiment analysis (positive, neutral, negative) using Hugging Face models.

---

## Installation

git clone https://github.com/Malikethes/investment-news.git
cd investment-news

python -m venv venv
# Windows
venv\Scripts\activate

pip install -r requirements.txt
Create a .env file in the root folder with the following variables:
HF_TOKEN=your_HuggingFace_API_Token
NEWS_API_KEY=your_NewsAPI_Key