from flask import Flask, render_template, request
import joblib
import platform, subprocess, re, os, shlex
import pandas as pd

MODEL_FILE = r"E:\Zain collage file\SEM VII\ISAA\web_app\wifi_model.pkl"
VECTORIZER_FILE = r"E:\Zain collage file\SEM VII\ISAA\web_app\wifi_vectorizer.pkl"

app = Flask(__name__)

# Load ML model + vectorizer
clf = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)

def scan_wifi():
    """Cross-platform Wi-Fi scan."""
    system = platform.system().lower()
    ssids = []
    try:
        if "windows" in system:
            out = subprocess.check_output(["netsh", "wlan", "show", "networks"], text=True)
            for line in out.splitlines():
                m = re.match(r"\s*SSID\s+\d+\s*:\s*(.+)$", line)
                if m:
                    ssid = m.group(1).strip()
                    if ssid:
                        ssids.append(ssid)
        elif "darwin" in system:
            airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
            out = subprocess.check_output([airport, "-s"], text=True)
            for line in out.splitlines()[1:]:
                if line.strip():
                    parts = re.split(r"\s{2,}", line.strip())
                    if parts:
                        ssid = parts[0].strip()
                        if ssid:
                            ssids.append(ssid)
        elif "linux" in system:
            try:
                out = subprocess.check_output(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], text=True)
                ssids = [s for s in out.splitlines() if s.strip()]
            except:
                out = subprocess.check_output(shlex.split("iwlist scan"), text=True)
                ssids = re.findall(r'ESSID:"([^"]+)"', out)
    except Exception as e:
        print("Error scanning Wi-Fi:", e)
    return list(dict.fromkeys(ssids))

def predict_ssids(ssids):
    X = vectorizer.transform(ssids)
    preds = clf.predict(X)
    return list(zip(ssids, preds))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_results = []
    if request.method == "POST":
        if request.form.get("manual_ssid"):
            ssid = request.form["manual_ssid"]
            pred = predict_ssids([ssid])[0][1]
            prediction_results.append((ssid, pred))
        elif request.form.get("scan_wifi"):
            ssids = scan_wifi()
            prediction_results = predict_ssids(ssids)
    return render_template("index.html", predictions=prediction_results)

if __name__ == "__main__":
    app.run(debug=True)
