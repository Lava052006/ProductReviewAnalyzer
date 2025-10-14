from transformers import pipeline
import pandas as pd

# Load your scraped data
df = pd.read_csv("reviews.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()
print("Columns found:", df.columns)

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Apply it to the correct column (review_text)
df["sentiment"] = df["review_text"].apply(lambda x: sentiment_analyzer(str(x))[0]['label'])

# Save results
df.to_csv("reviews_with_sentiment.csv", index=False)

print("✅ Sentiment analysis completed! Results saved to reviews_with_sentiment.csv")

