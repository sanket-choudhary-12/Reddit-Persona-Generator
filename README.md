Reddit Persona Generator
Ever wondered what kind of person is behind a Reddit username?
This tool uses the power of AI to create a detailed personality profile from a user's public posts and comments. It's a fascinating way to understand online behavior, built as a submission for the BeyondChats AI/LLM Engineer Intern assignment.

🚀 What Makes This Tool Special?
This isn't just a data scraper. It's an intelligent analysis tool that provides deep insights in a clean, professional format.

🎯 Intelligent Persona Building
Goes beyond word clouds by using a Large Language Model (Google's Gemini Pro) to infer personality traits, motivations, frustrations, and even demographics.

🔗 Evidence-Based Analysis
Every insight is backed up by a clickable citation, linking directly to the post or comment that informed the AI's conclusion. This was a core requirement and ensures transparency.

🖥️ Polished & Interactive UI
Built with Streamlit, the interface is clean, modern, and easy to use. Key details are highlighted in metric cards, and deeper insights are organized into collapsible sections.

📄 One-Click Export
Instantly save any generated persona as a neatly formatted .txt report for your records.

⚙️ Technology at a Glance
This project leverages a modern stack to get the job done efficiently:

Backend: Python

Web Framework: Streamlit

Reddit API Wrapper: PRAW (The Python Reddit API Wrapper)

AI/LLM: Google Gemini Pro

Secrets Management: python-dotenv

🛠️ Getting Started on Your Machine
Want to run this yourself? It’s easy. Just follow these three steps.

1️⃣ Step 1: Get the Code
bash
Copy
Edit
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
2️⃣ Step 2: Install the Dependencies
This project uses a few Python libraries, which are listed in the requirements.txt file. Install them all with:

bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Step 3: Set Up Your API Keys
The magic of this app comes from the Reddit and Google APIs. To keep your secret keys safe, we use a .env file.

Create a new file in the project directory named .env

Copy the block below into that file.

Replace the placeholder text with your actual API keys.

dotenv
Copy
Edit
# .env file

# Get this from the Google AI Studio
GEMINI_API_KEY="Your_Google_AI_API_Key"

# Get these by creating a 'script' app on Reddit's developer page
REDDIT_CLIENT_ID="Your_Reddit_Client_ID"
REDDIT_CLIENT_SECRET="Your_Reddit_Client_Secret"
REDDIT_USER_AGENT="Desktop:PersonaGenerator:v1.0 (by /u/YourRedditUsername)"
Why the .env file?
This file is listed in .gitignore, so you'll never accidentally commit your secret keys to a public repository. It's a crucial security practice!

🧠 How It Works
Once everything is set up, running the app is simple.

▶️ Launch the App
bash
Copy
Edit
streamlit run app.py
🌐 Paste a URL
Your browser will open with the app running. Just paste a full Reddit user profile URL into the input box.

🔍 Generate!
Click the "Generate Persona" button and watch as the AI analyzes the user and builds the report right before your eyes.

The final report will also be saved as a .txt file in your project folder.
