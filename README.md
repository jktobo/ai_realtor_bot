# AI Telegram Bot for Apartment Rentals in Kyrgyzstan 🇰🇬🏠

## Description

This project is an AI-powered Telegram bot designed to simplify the process of finding rental apartments in Kyrgyzstan. Instead of manually browsing websites like Lalafo.kg, users can send requests in natural language (e.g., "find a 1-bedroom apartment," "show me 2-bedroom flats") directly to the bot. The bot utilizes AI to understand the request, scrapes relevant listings in real-time, and sends the top results back to the user in the Telegram chat.

## Features ✨

* **Natural Language Processing (NLP):** Understands user requests written in plain language using the OpenAI API (GPT-3.5).
* **Real-time Web Scraping:** Fetches the latest apartment listings directly from lalafo.kg using `httpx` and `BeautifulSoup`.
* **Telegram Integration:** Provides a user-friendly interface through a Telegram bot.
* **Asynchronous Backend:** Built with FastAPI for high performance and responsiveness.
* **Containerized:** Fully containerized using Docker for easy deployment and environment consistency.
* **Cloud-Ready:** Designed for deployment on cloud platforms like AWS App Runner.

## Tech Stack 🛠️

* **Language:** Python 3.11+
* **Backend Framework:** FastAPI
* **AI:** OpenAI API
* **HTTP Client:** httpx (for asynchronous requests)
* **HTML Parsing:** BeautifulSoup4
* **Telegram Bot Library:** python-telegram-bot
* **Environment Variables:** python-dotenv
* **Containerization:** Docker
* **Deployment Platform:** AWS App Runner (via Amazon ECR)

---

## Detailed Local Setup & Installation Guide ⚙️

This guide will walk you through setting up and running the bot on your local computer step-by-step.

### Step 1: Prerequisites (Install Required Software) 💻

Before you start, make sure you have the following installed on your computer:

1.  **Python:** Version 3.9 or higher. You can download it from [python.org](https://www.python.org/). Verify your installation by opening a terminal and typing `python --version` or `python3 --version`.
2.  **Git:** A version control system needed to download the project code. Download from [git-scm.com](https://git-scm.com/). Verify by typing `git --version` in your terminal.
3.  **(Optional but Recommended) Docker Desktop:** For building and running the container locally. Download from [docker.com](https://www.docker.com/).
4.  **ngrok:** A tool to create a secure tunnel to your local machine, allowing Telegram to send messages to your bot. Sign up and download from [ngrok.com](https://ngrok.com/).

### Step 2: Get Secret API Keys 🔑

This bot needs two secret keys to function:

1.  **Telegram Bot Token:**
    * Open Telegram and search for the bot named `@BotFather`.
    * Send the command `/newbot` to BotFather.
    * Follow the instructions to choose a name (e.g., "My Apartment Finder") and a unique username (e.g., "MyAptFinderBot") for your bot.
    * BotFather will provide you with a **token**. It looks like `71234XXXXX:AAFabcdefghijklmnopqrstuvwxyzXXXXX`. **Copy this token and save it securely.** 
2.  **OpenAI API Key:**
    * Go to [platform.openai.com](https://platform.openai.com/) and sign up or log in.
    * Navigate to the **"API keys"** section in your account settings (usually under your profile icon). 
    * Click **"+ Create new secret key"**.
    * Give the key a name (optional, e.g., `TelegramBotKey`) and click "Create secret key".
    * OpenAI will display your **API key** (starting with `sk-...`). **Copy this key immediately and save it securely.** You won't be able to see it again.

### Step 3: Download the Project Code 📥

1.  Open your **Terminal** (or Command Prompt/PowerShell on Windows).
2.  Navigate to the directory where you want to store the project using the `cd` command (e.g., `cd Documents/Projects`).
3.  Clone the repository from GitHub using its URL:
    ```bash
    git clone <URL_OF_YOUR_GITHUB_REPOSITORY>
    ```
4.  Enter the newly created project directory:
    ```bash
    cd ai_realtor_bot # Or your project's folder name
    ```

### Step 4: Set Up the Python Environment 🛠️

1.  **Create a virtual environment:** This keeps the project's dependencies separate.
    ```bash
    python -m venv venv
    ```
2.  **Activate the virtual environment:**
    * **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    Your terminal prompt should now start with `(venv)`.
3.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

### Step 5: Configure Secret Keys 🤫

1.  In the main project folder (where `requirements.txt` is), create a new file named exactly **`.env`**.
2.  Open `.env` with a text editor and add your saved keys, replacing the placeholders:
    ```env
    TELEGRAM_BOT_TOKEN="<PASTE_YOUR_TELEGRAM_TOKEN_HERE>"
    OPENAI_API_KEY="<PASTE_YOUR_OPENAI_API_KEY_HERE>"
    ```
    * **Important:** Ensure there are no extra spaces before or after the quotes. The OpenAI key must start with `sk-`.
3.  **Save** the `.env` file.

### Step 6: Run the Bot! 🚀

You'll need **two Terminal windows** open for this.

1.  **Terminal Window 1 (Run the Server):**
    * Make sure you are in the project directory (`ai_realtor_bot`) and the virtual environment `(venv)` is active.
    * Start the FastAPI web server:
        ```bash
        uvicorn app.main:app --reload --port 8000
        ```
    * Keep this terminal open. You'll see server logs here.
2.  **Terminal Window 2 (Run ngrok):**
    * Start ngrok to expose port 8000:
        ```bash
        ngrok http 8000
        ```
    * Look for the `Forwarding` line in the ngrok output. Copy the **HTTPS** URL (it looks like `https://random-words.ngrok-free.app`). 
    * Keep this terminal open.
3.  **Tell Telegram Where to Send Messages (Set Webhook):**
    * Open your **web browser**.
    * Construct the following URL, replacing `<YOUR_TELEGRAM_BOT_TOKEN>` and `<YOUR_NGROK_HTTPS_URL>` with your actual token and the ngrok URL you just copied:
        ```text
        [https://api.telegram.org/bot](https://api.telegram.org/bot)<YOUR_TELEGRAM_BOT_TOKEN>/setWebhook?url=<YOUR_NGROK_HTTPS_URL>/webhook
        ```
    * Paste this complete URL into your browser's address bar and press Enter.
    * You should see a confirmation message like `{"ok":true,"result":true,"description":"Webhook was set"}`.

### Step 7: Test Your Bot ✅

Go to Telegram, find the bot you created, and send it a message like `/start` or "1 комнатная квартира". It should respond! Check Terminal Window 1 for logs of its activity.

Congratulations! Your AI bot is running locally. 🎉

---

## Running with Docker 🐳

(Instructions for running with Docker remain the same as before)

1.  **Build the Docker image:**
    ```bash
    docker build -t ai-realtor-bot .
    ```
2.  **Run the Docker container:**
    * **Using `.env` file:**
        ```bash
        docker run --rm -p 8000:80 --env-file .env ai-realtor-bot
        ```
    * **Or passing variables directly:**
        ```bash
        docker run --rm -p 8000:80 \
        -e TELEGRAM_BOT_TOKEN="YOUR_NEW_TELEGRAM_BOT_TOKEN" \
        -e OPENAI_API_KEY="sk-YOUR_NEW_OPENAI_API_KEY" \
        ai-realtor-bot
        ```
3.  Use `ngrok http 8000` and set the webhook as described in Step 6.3 above.

---

## Deployment on AWS ☁️

(Instructions for AWS deployment remain the same as before)

This application is ready for deployment on AWS App Runner:

1.  Push the built Docker image to Amazon ECR (Elastic Container Registry).
2.  Create an AWS App Runner service, configuring it to use the image from ECR.
3.  Set the `TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY` as environment variables in the App Runner service configuration.
4.  Configure the service port to `80`.
5.  Once deployed, use the permanent App Runner domain URL to set the Telegram webhook.

---

## Usage 💬

Simply open a chat with your bot in Telegram and send it a message describing the apartment you are looking for, e.g.:

* `1 комнатная квартира`
* `find 2 bedroom flat`
* `двушка`

The bot will analyze your request and reply with the search results.
