# Penguin Server Watcher 🐧

A Python-based multi-server health monitoring tool that checks website availability and sends real-time notifications through Telegram when a server goes down or recovers.

Developed for **Penguin Entertainment Limit**.

---

## Features

- Monitor multiple websites and server endpoints.
- Automatically check server availability at regular intervals.
- Send Telegram notifications when a server goes down.
- Send recovery notifications when a server becomes available again.
- Prevent repeated alerts while a server remains in the same state.
- Check server status directly through Telegram commands.
- Display monitoring activity in the terminal.

## Requirements

- Windows 10 or Windows 11
- Python 3.9 or newer recommended
- An internet connection
- A Telegram account
- A Telegram bot created through [@BotFather](https://t.me/BotFather)

## Project Structure

```text
Server_Health_Checking/
├── shc.py
├── README.md
└── requirements.txt
```

The `requirements.txt` file should contain:

```text
requests
```

## 1. Install Dependencies

Open PowerShell in the project directory.

Install the required Python library:

```powershell
py -m pip install -r requirements.txt
```

Alternatively, install it directly:

```powershell
py -m pip install requests
```

## 2. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot`.
3. Enter a display name for your bot.
4. Choose a unique username ending in `bot`.
5. Copy the API token provided by BotFather.

**Security warning:** Your bot token is a secret credential. Never publish it in source code, screenshots, Git repositories, or public messages.

If your token is exposed, revoke it through BotFather and generate a replacement.

## 3. Configure the Environment Variables

The application uses environment variables to store its Telegram credentials instead of hardcoding them into the source code.

Open PowerShell and set your bot token:

```powershell
$env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
```

Replace `YOUR_BOT_TOKEN` with your actual token.

Keep this PowerShell window open. Environment variables set this way are available to programs launched from that window and its child processes, but do not persist after the window closes.

## 4. Get Your Telegram Chat ID

The bot needs your chat ID to know where to send monitoring alerts.

### Step 1: Start the bot

1. Open your bot's Telegram link.
2. Press **Start**.
3. Send a message such as `hello`.

### Step 2: Retrieve your chat ID

Run this command in PowerShell:

```powershell
py -c "import os,requests; t=os.getenv('TELEGRAM_BOT_TOKEN'); r=requests.get(f'https://api.telegram.org/bot{t}/getUpdates',timeout=10); print(r.json())"
```

Find the following structure in the output:

```json
{
  "chat": {
    "id": 123456789,
    "type": "private"
  }
}
```

The number under `chat.id` is your Telegram chat ID.

Do not confuse it with `update_id` or `message_id`.

### Step 3: Set the chat ID

In PowerShell, run:

```powershell
$env:TELEGRAM_CHAT_ID="YOUR_CHAT_ID"
```

Replace `YOUR_CHAT_ID` with the number you retrieved.

**Important:** If `getUpdates` returns an empty result, open the bot in Telegram and send another message. Also make sure another running instance of the bot is not consuming the updates.

## 5. Configure the Servers

Open `shc.py` and locate the `SERVERS` dictionary.

Example:

```python
SERVERS = {
    "Main Website": "https://example.com",
    "Python Website": "https://www.python.org",
    "Company API": "https://api.example.com/health",
}
```

Replace these example URLs with the actual websites or health-check endpoints you want to monitor.

Each entry contains:

- **Key:** A friendly name displayed in Telegram notifications.
- **Value:** The URL that the monitoring system checks.

The current implementation considers an HTTP response with a status code below `400` to be online. A successful HTTP response does not necessarily mean every application function is healthy.

## 6. Start the Monitoring Program

Navigate to the project directory:

```powershell
cd "C:\Users\User\Documents\Working\Server_Health_Checking"
```

Set your credentials if they are not already set in this PowerShell session:

```powershell
$env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
$env:TELEGRAM_CHAT_ID="YOUR_CHAT_ID"
```

Start the program:

```powershell
py -u shc.py
```

When the program starts successfully, it sends a startup message to Telegram and begins checking the configured servers.

The terminal displays monitoring activity and server states.

**Keep the terminal open while monitoring.** Closing it or stopping the Python process stops the monitoring loop.

## 7. Use the Bot in Telegram

Open your bot's chat and use these commands:

| Command | Description |
|---|---|
| `/start` | Receive a startup message and command information. |
| `/status` | View the latest recorded status of monitored servers. |
| `/help` | Display available bot commands. |

### Example Notifications

Server down:

```text
🔴 SERVER DOWN
Main Website
https://example.com
```

Server recovered:

```text
🟢 SERVER RECOVERED
Main Website
https://example.com
```

The bot tracks state changes to avoid repeatedly sending the same alert on every monitoring cycle.

## 8. Stop the Monitoring Program

To stop monitoring:

1. Return to the PowerShell window running `shc.py`.
2. Press **Ctrl + C**.
3. Wait for Python to terminate and the PowerShell prompt to return.

The monitoring process has now stopped. No further checks or notifications will be generated by that process.

To start monitoring again, run:

```powershell
py -u shc.py
```

If you open a new PowerShell window, configure the environment variables again before starting the program.

### Stop or Mute the Telegram Bot

Muting or archiving the Telegram conversation only changes how you receive or view messages. It does not stop the monitoring program.

To stop server monitoring, terminate the Python process.

## 9. Troubleshooting

### `401 Unauthorized`

The bot token is invalid, revoked, or incorrectly configured.

- Check the token in BotFather.
- Set the correct `TELEGRAM_BOT_TOKEN`.
- Restart the program.

### `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` Missing

Set both environment variables in the same PowerShell window before running the program.

### No Telegram Notifications

- Confirm that you pressed Start and opened a conversation with the bot.
- Verify the chat ID.
- Ensure the bot token is valid.
- Check that the Python program is still running.
- Review any errors displayed in PowerShell.

### A Website Is Reported as Down

- Check the URL manually in a browser.
- Confirm that the endpoint is accessible from your network.
- Check for DNS, TLS, firewall, or proxy problems.
- Consider whether the endpoint requires authentication or returns an HTTP error during normal operation.

A failed HTTP request may indicate a network problem rather than an actual server outage.

### The Program Appears to Be Doing Nothing

The monitoring loop may be waiting for Telegram updates or the next scheduled server check. This is normal for a background monitoring program.

Use the terminal output to confirm activity. Press Ctrl + C to stop it.

## 10. Operational Notes

- The monitoring program must remain running to perform checks.
- The configured check interval determines how frequently the servers are checked.
- The current implementation stores server states in memory. Restarting the program resets its state history.
- Use a computer or server that remains online for continuous monitoring.
- For production deployments, consider persistent logs, repeated-failure confirmation, secure credential management, and automatic process restarts.

## License and Ownership

Copyright © Penguin Entertainment Limit. All rights reserved.

This project is intended for authorized server and website monitoring. Ensure that you have permission to monitor all configured endpoints.

