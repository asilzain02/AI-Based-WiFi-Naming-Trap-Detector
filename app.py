from flask import Flask, render_template, jsonify
import pandas as pd
import joblib
from train_model import bssid_to_last_byte  # your custom helper
import pywifi
from pywifi import const
import time

app = Flask(__name__)

# Load trained model
pipeline = joblib.load(r"E:\Zain collage file\SEM VII\ISAA\wifi_scanner\wifi_pipeline.pkl")

# Scan Wi-Fi networks
def scan_wifi_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(5)  # wait for results
    scan_results = iface.scan_results()

    networks = []
    for net in scan_results:
        if net.akm:
            auth = "WPA2" if const.AKM_TYPE_WPA2PSK in net.akm else "WPA3" if const.AKM_TYPE_WPA3 in net.akm else "Open"
        else:
            auth = "Open"
        networks.append({
            "SSID": net.ssid,
            "BSSID": net.bssid,
            "RSSI": net.signal,
            "Auth": auth,
            "Channel": net.freq // 5
        })
    return networks

# Predict real/fake networks
def predict_networks(networks):
    if not networks:
        return []
    df = pd.DataFrame(networks, columns=["SSID", "BSSID", "RSSI", "Auth", "Channel"])
    preds = pipeline.predict(df)
    results = []
    for net, pred in zip(networks, preds):
        net['prediction'] = pred.capitalize()
        net['prediction_class'] = 'real' if pred == 'real' else 'fake'
        results.append(net)
    return results

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/scan")
def api_scan():
    networks = scan_wifi_networks()
    results = predict_networks(networks)
    # Summary metrics
    total = len(results)
    real_count = len([n for n in results if n['prediction_class'] == 'real'])
    fake_count = total - real_count
    strongest = max(results, key=lambda x: x['RSSI']) if results else {}
    return jsonify({"networks": results, "summary": {"total": total, "real": real_count, "fake": fake_count, "strongest": strongest}})

if __name__ == "__main__":
    app.run(debug=True)
