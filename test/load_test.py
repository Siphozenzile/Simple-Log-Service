import requests
import json
import datetime
import time

# Replace with your actual API Gateway URL
API_URL = "https://ktu6kd7bml.execute-api.us-east-1.amazonaws.com/Prod/log"

def send_logs():
    for i in range(1, 101):
        payload = {
            "ID": str(i),
            "DateTime": datetime.datetime.utcnow().isoformat() + "Z",
            "Severity": "info",  # can be "warning" or "error" too
            "Message": f"Test log entry number {i}"
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

        print(f"[{i}] Status: {response.status_code} - {response.text}")

        # Optional: Delay to avoid spamming API Gateway too quickly
        time.sleep(0.1)  # 100 ms pause

if __name__ == "__main__":
    send_logs()
