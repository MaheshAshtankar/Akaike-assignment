# api.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils import scrape_news, perform_sentiment_analysis, comparative_analysis, generate_tts

app = FastAPI()

# Allow all origins (for development purposes).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "News Summarization API is running"}


@app.get("/get_news")
def get_news(company: str):
    try:
        articles = scrape_news(company)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not articles:
        raise HTTPException(status_code=404, detail="No news articles found")
    return {"company": company, "articles": articles}


@app.post("/analyze")
def analyze_news(data: dict):
    """
    Expects JSON payload with key 'company'
    Processes scraping, sentiment analysis, comparative analysis, and TTS.
    """
    company = data.get("company")
    if not company:
        raise HTTPException(status_code=400, detail="Company name is required")

    try:
        articles = scrape_news(company)
        articles = perform_sentiment_analysis(articles)
        comp_analysis = comparative_analysis(articles)
        audio_file = generate_tts(articles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "company": company,
        "articles": articles,
        "comparative_analysis": comp_analysis,
        "audio": audio_file
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
