# AI-Powered Reddit Persona Generator

This project is an AI-driven tool, developed as part of an assignment, that generates a detailed user persona from a public Reddit user profile. It uses a Streamlit web interface to accept a URL, scrapes user data with PRAW, and leverages Google's Gemini Pro LLM to analyze the data and construct a comprehensive, cited persona.

## Features

-   **Simple Web Interface:** A clean and interactive UI built with Streamlit.
-   **Reddit Data Scraping:** Fetches a user's most recent posts and comments using the PRAW library.
-   **AI Persona Generation:** Utilizes the Google Gemini Pro Large Language Model to create in-depth user personas based on the scraped text.
-   **Cited Analysis:** Every inferred characteristic in the persona includes a clickable hyperlink to the specific comment or post that informed the analysis, fulfilling a key assignment requirement.
-   **Polished UI:** Presents the persona in a structured layout with metric cards for key details and collapsible sections for a clean user experience.
-   **File Export:** Automatically saves the complete, Markdown-formatted persona to a local text file.

## Setup and Execution

Follow these steps to set up and run the project locally.

### 1. Prerequisites

-   Python 3.8 or higher
-   Pip (Python package installer)

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
Use code with caution.
Markdown

3. Install Dependencies
Install all the necessary Python packages from the requirements.txt file.
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash

4. Set Up Environment Variables
For the script to access the necessary APIs, you must provide your own credentials. Create a file named .env in the root directory of the project.

Copy the following into your .env file and replace the placeholder text with your actual keys:
# Google Gemini API Key
GEMINI_API_KEY="Your_Google_AI_API_Key"

# Reddit API Credentials
REDDIT_CLIENT_ID="Your_Reddit_Client_ID"
REDDIT_CLIENT_SECRET="Your_Reddit_Client_Secret"
REDDIT_USER_AGENT="Python:PersonaGenerator:v1.0 (by /u/YourRedditUsername)"
Use code with caution.
See the guides for generating Google AI keys and Reddit API credentials.

5. Run the Application
Execute the following command in your terminal from the project's root directory:
Generated bash
streamlit run app.py
Use code with caution.
Bash
Your default web browser will automatically open a new tab with the running application.
How to Use
Enter URL: Paste the full URL of a public Reddit user's profile into the input field (e.g., https://www.reddit.com/user/kojied/).
Generate: Click the "Generate Persona" button.
View and Save: The application will display the persona on the screen. A text file named [username]_persona.txt will also be saved in the project folder.
Sample Output Files
This repository includes pre-generated persona files for the sample users provided in the assignment for reference:
kojied_persona.txt
Hungry-Move-6603_persona.txt


### **Final `requirements.txt`**

Ensure this file is in your repository.
