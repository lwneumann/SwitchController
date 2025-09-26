import requests
import time


BASE_URL = "http://localhost:5000"


# -----------------------------
# One-way update
# -----------------------------
def send_update(message: str):
    try:
        resp = requests.post(f"{BASE_URL}/update", json={"message": message})
        data = resp.json()
        print(f"One-way update response: {data}")
    except Exception as e:
        print(f"Error sending update: {e}")

# -----------------------------
# Ask for user input
# -----------------------------
def request_input(prompt: str):
    try:
        # Send input request
        resp = requests.post(f"{BASE_URL}/update", json={"id": "ask", "prompt": prompt})
        data = resp.json()
        if data.get("status") != "ok":
            print(f"Error from bot: {data}")
            return None

        # Poll until reply is ready (no request ID needed)
        reply = None
        while True:
            r = requests.get(f"{BASE_URL}/result")
            result = r.json()
            if result["status"] == "ok":
                reply = result["reply"]
                break
            elif result["status"] == "pending":
                time.sleep(1)
            else:
                print(f"Error from bot: {result.get('message')}")
                break
        return reply
    except Exception as e:
        print(f"Error requesting input: {e}")
        return None

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # One-way update
    send_update("Update Message 1")

    # Ask for user input
    reply = request_input("What should the system do next?")
    print(f"Received input from Discord: {reply}")
