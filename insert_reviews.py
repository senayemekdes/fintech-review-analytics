import pandas as pd
import psycopg2

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("notebooks/dataprocessed/all_reviews3.csv")

# =========================
# THEME ANALYSIS
# =========================

THEME_MAP = {
    "Stability": ["crash", "freeze", "bug", "slow", "error", "stuck"],
    "Authentication": ["otp", "login", "password", "verify", "sign in"],
    "Transactions": ["transfer", "payment", "transaction", "send", "receive"],
    "User Experience": ["easy", "smooth", "simple", "friendly", "interface"],
    "Performance": ["fast", "quick", "responsive"],
    "Account Issues": ["account", "blocked", "locked"],
    "Customer Support": ["support", "service", "help", "response"]
}

# Function to identify theme
def identify_theme(review):

    review = str(review).lower()

    for theme, keywords in THEME_MAP.items():

        for keyword in keywords:

            if keyword in review:
                return theme

    return "Other"

# Apply theme analysis
df["identified_theme"] = df["content"].apply(identify_theme)

# =========================
# SAVE UPDATED CSV
# =========================

df.to_csv("notebooks/dataprocessed/all_reviews3.csv", index=False)

print("Theme analysis completed and CSV updated!")

# =========================
# POSTGRESQL CONNECTION
# =========================

conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",
    password="123456",
    port="5432"
)

cur = conn.cursor()

# =========================
# BANK MAPPING
# =========================

bank_map = {
    "CBE Bank": 3,
    "BOA Bank": 1,
    "Dashen Bank": 2
}

# =========================
# INSERT DATA
# =========================

for _, row in df.iterrows():

    bank_id = bank_map[row["bank"]]

    cur.execute(
        """
        INSERT INTO reviews (
            bank_id,
            review_text,
            rating,
            review_date,
            transformer_sentiment_label,
            transformer_sentiment_score,
            identified_theme,
            source
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            bank_id,
            row["content"],
            row["score"],
            row["at"],
            row["transformer_sentiment_label"],
            row["transformer_sentiment_score"],
            row["identified_theme"],
            "Google Play Store"
        )
    )

# =========================
# SAVE TO DATABASE
# =========================

conn.commit()

print("Reviews inserted successfully!")

cur.close()
conn.close()