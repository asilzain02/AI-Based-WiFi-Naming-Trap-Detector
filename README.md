📡 AI-Based-WiFi-Naming-Trap-Detector

📌 Overview

This project implements a Wi-Fi SSID classification system using a pre-trained Machine Learning model and Flask web interface.
It scans available Wi-Fi networks (or allows manual SSID entry), runs them through a trained classifier, and predicts whether each SSID is Fake or Legit.

📂 Project Structure
<img width="824" height="297" alt="image" src="https://github.com/user-attachments/assets/f2f2d29b-0e70-493c-b25b-9e0c0fb0e84b" />


⚙️ Installation

Clone the repository or download the project.

git clone https://github.com/your-username/wifi-fake-ssid-detector.git
cd wifi-fake-ssid-detector


Create and activate a virtual environment (recommended).

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies.

pip install -r requirements.txt

📦 Requirements

Add this to requirements.txt:

flask
joblib
pandas
scikit-learn


For Wi-Fi scanning support:

Windows → netsh (pre-installed)

Linux → nmcli or iwlist required

MacOS → airport binary available

🚀 Usage

Ensure you have the trained model (wifi_model.pkl) and vectorizer (wifi_vectorizer.pkl) in the project directory.

Run the Flask app:

python app.py


Open browser → http://127.0.0.1:5000

Options available:

Manual SSID Entry → Enter a Wi-Fi name (SSID) to check if it’s Fake or Legit.

Scan Wi-Fi Networks → Auto-scan nearby SSIDs (platform-dependent) and classify them.

🖼 Example Output

Manual Input:

SSID: Free_Public_WiFi_123 → Prediction: Fake
SSID: HomeNetwork → Prediction: Legit


Wi-Fi Scan Output:

SSID: Airport_WiFi → Fake
SSID: TP-Link_76AB → Legit
SSID: Free_Coffee_Shop_WiFi → Fake

🔮 Future Enhancements

✅ Add support for real-time background scanning.

✅ Store scan history in a database (SQLite/Postgres).

✅ Build an Android app (via Flask API + React Native/Flutter).

✅ Improve classification accuracy with deep learning models (LSTM/BERT).

👨‍💻 Author

Developed by Zain ✨
