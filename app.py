from flask import Flask, render_template, jsonify, request
import pandas as pd
import joblib
import platform, subprocess, re, os, shlex, time
import pywifi
from pywifi import const

# Initialize Flask app
app = Flask(__name__)

# === Load Models ===
PIPELINE_FILE = r"E:\Zain collage file\SEM VII\ISAA\wifi_scanner\wifi_pipeline.pkl"
MODEL_FILE = r"E:\Zain collage file\SEM VII\ISAA\web_app\wifi_model.pkl"
VECTORIZER_FILE = r"E:\Zain collage file\SEM VII\ISAA\web_app\wifi_vectorizer.pkl"

# Load trained pipeline
try:
    pipeline = joblib.load(PIPELINE_FILE)
except:
    pipeline = None

try:
    clf = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)
except:
    clf = None
    vectorizer = None


# === Wi-Fi Scanner for pywifi (Windows only) ===
def scan_wifi_networks():
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.scan()
        time.sleep(5)
        scan_results = iface.scan_results()
    except Exception as e:
        print("Wi-Fi scan unavailable:", e)
        scan_results = []
    return scan_results



# === Predict Real/Fake Networks ===
def predict_networks(networks):
    if not networks or not pipeline:
        return []
    df = pd.DataFrame(networks, columns=["SSID", "BSSID", "RSSI", "Auth", "Channel"])
    preds = pipeline.predict(df)
    results = []
    for net, pred in zip(networks, preds):
        net['prediction'] = pred.capitalize()
        net['prediction_class'] = 'real' if pred == 'real' else 'fake'
        results.append(net)
    return results


# === Alternate OS Scan (netsh/nmcli) ===
def scan_wifi_cross_platform():
    """Cross-platform Wi-Fi SSID scan."""
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
            out = subprocess.check_output(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], text=True)
            ssids = [s for s in out.splitlines() if s.strip()]
    except Exception as e:
        print("Error scanning Wi-Fi:", e)
    return list(dict.fromkeys(ssids))


# === Predict SSIDs ===
def predict_ssids(ssids):
    if not clf or not vectorizer:
        return []
    X = vectorizer.transform(ssids)
    preds = clf.predict(X)
    return list(zip(ssids, preds))


# === ROUTES ===

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_results = []
    if request.method == "POST":
        if request.form.get("manual_ssid"):
            ssid = request.form["manual_ssid"]
            pred = predict_ssids([ssid])[0][1]
            prediction_results.append((ssid, pred))
        elif request.form.get("scan_wifi"):
            ssids = scan_wifi_cross_platform()
            prediction_results = predict_ssids(ssids)
    return render_template("index.html", predictions=prediction_results)


@app.route("/api/scan")
def api_scan():
    networks = scan_wifi_networks()
    results = predict_networks(networks)
    total = len(results)
    real_count = len([n for n in results if n['prediction_class'] == 'real'])
    fake_count = total - real_count
    strongest = max(results, key=lambda x: x['RSSI']) if results else {}
    return jsonify({
        "networks": results,
        "summary": {
            "total": total,
            "real": real_count,
            "fake": fake_count,
            "strongest": strongest
        }
    })


# === RUN ===
if __name__ == "__main__":
    app.run(debug=True)
