
import os
import time
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise SystemExit("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID first.")

API = f"https://api.telegram.org/bot{TOKEN}"

SERVERS = {
    "Example Website": "https://example.com",
    "Python Website": "https://www.python.org",
}

CHECK_INTERVAL = 30
REQUEST_TIMEOUT = 8

session = requests.Session()
server_states = {}
offset = None
last_check = 0


def send_message(text):
    response = session.post(
        f"{API}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=10
    )
    response.raise_for_status()

    if not response.json().get("ok"):
        raise RuntimeError("Telegram failed to send the message")


def check_server(name, url):
    try:
        response = session.get(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )
        return response.status_code < 400
    except requests.RequestException:
        return False


def check_all_servers():
    global server_states

    print("\nChecking servers...", flush=True)

    for name, url in SERVERS.items():
        online = check_server(name, url)
        previous = server_states.get(name)

        if previous is None:
            state = "ONLINE" if online else "DOWN"
            print(f"{name}: {state}", flush=True)

            if not online:
                send_message(f"🔴 SERVER DOWN\n{name}\n{url}")
        elif previous != online:
            if online:
                message = f"🟢 SERVER RECOVERED\n{name}\n{url}"
                print(f"{name}: RECOVERED", flush=True)
            else:
                message = f"🔴 SERVER DOWN\n{name}\n{url}"
                print(f"{name}: DOWN", flush=True)

            send_message(message)

        else:
            state = "ONLINE" if online else "DOWN"
            print(f"{name}: {state}", flush=True)

        server_states[name] = online


def get_status():
    lines = ["SERVER STATUS"]

    for name, online in server_states.items():
        icon = "Good!" if online else "Oops.."
        state = "UP" if online else "DOWN"
        lines.append(f"{icon} {name}: {state}")

    if not server_states:
        lines.append("No checks completed yet.")

    return "\n".join(lines)


def handle_updates():
    global offset

    response = session.get(
        f"{API}/getUpdates",
        params={"offset": offset, "timeout": 5},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    if not data.get("ok"):
        raise RuntimeError("Telegram could not retrieve updates")

    for update in data["result"]:
        offset = update["update_id"] + 1

        message = update.get("message", {})
        chat = message.get("chat", {})
        text = message.get("text", "")

        if str(chat.get("id")) != CHAT_ID:
            continue

        if text == "/start":
            send_message(
                "Server Watcher is online\n"
                "Commands: /status, /help"
            )
        elif text == "/status":
            send_message(get_status())
        elif text == "/help":
            send_message(
                "/status - Check the latest server statuses\n"
                "/help - Show available commands"
            )


def main():
    global last_check

    print("Penguin Server Watcher started.", flush=True)
    send_message("Server Watcher started!")

    while True:
        try:
            now = time.monotonic()

            if now - last_check >= CHECK_INTERVAL:
                check_all_servers()
                last_check = time.monotonic()

            handle_updates()

        except (requests.RequestException, RuntimeError) as error:
            print(f"Connection error: {error}", flush=True)
            time.sleep(3)


if __name__ == "__main__":
    main()

