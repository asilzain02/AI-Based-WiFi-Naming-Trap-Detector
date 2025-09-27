import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer   # ✅ Correct import
from sklearn.linear_model import LogisticRegression

# ---------- Custom BSSID transformer ----------
def bssid_to_last_byte(bssid_series):
    results = []
    for bssid in bssid_series:
        try:
            results.append(int(bssid.split(":")[-1], 16))
        except:
            results.append(-1)
    return np.array(results).reshape(-1, 1)   # always 2D

# ---------- Load dataset ----------
df = pd.read_csv(r"E:\Zain collage file\SEM VII\ISAA\wifi_scanner\Dataset\wifi_dataset_clean.csv")

X = df[["SSID", "BSSID", "RSSI", "Auth", "Channel"]]
y = df["Label"]

# ---------- Preprocessing ----------
preprocessor = ColumnTransformer(
    transformers=[
        ("ssid", TfidfVectorizer(analyzer="char", ngram_range=(2, 4)), "SSID"),
        ("bssid", FunctionTransformer(bssid_to_last_byte, validate=False), "BSSID"),
        ("rssi", StandardScaler(), ["RSSI"]),
        ("auth", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["Auth"]),
        ("channel", StandardScaler(), ["Channel"]),
    ]
)

# ---------- Pipeline ----------
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

# ---------- Train/test split ----------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)

print("Training accuracy:", pipeline.score(X_train, y_train))
print("Testing accuracy:", pipeline.score(X_test, y_test))

# ---------- Save pipeline ----------
joblib.dump(pipeline, r"E:\Zain collage file\SEM VII\ISAA\wifi_scanner\wifi_pipeline.pkl")
print("✅ Model saved as wifi_pipeline.pkl")
