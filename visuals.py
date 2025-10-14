import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("reviews_with_sentiment.csv")

# Count how many reviews per sentiment
counts = df["sentiment"].value_counts()
print("📊 Sentiment Counts:")
print(counts)

# Percentage breakdown
print("\n📈 Percentage Distribution:")
print((counts / counts.sum() * 100).round(2))

counts.plot(kind='bar', color=['green', 'red', 'gray'])
plt.title("Customer Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.show()
