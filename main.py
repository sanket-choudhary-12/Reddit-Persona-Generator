import streamlit as st
import praw
import prawcore
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()

def initialize_apis():
    """Initializes and returns configured API clients for Reddit and Gemini."""
    try:
        # Configure the Gemini API key from environment variables
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        llm = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize the Reddit instance with credentials from environment variables
        reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_USER_AGENT"],
        )
        return reddit, llm
    except (AttributeError, KeyError) as e:
        st.error(f"FATAL: API key or Reddit credential environment variable is not set. Please check your .env file. Error: {e}", icon="🚨")
        st.stop()

# --- 2. DATA FETCHING ---

def fetch_reddit_data(reddit_client, username: str):
    """
    Fetches the Reddit user object and their recent activity with full URLs for citation.
    """
    try:
        redditor = reddit_client.redditor(username)
        # A lightweight check to see if the user exists and is accessible
        _ = redditor.id  
        
        user_activity = ""
        base_url = "https://www.reddit.com"
        
        # Fetch recent submissions (posts)
        for submission in redditor.submissions.new(limit=15):
            full_url = base_url + submission.permalink
            user_activity += f"Post Title: {submission.title}\nContent: {submission.selftext}\nURL: {full_url}\n\n"

        # Fetch recent comments
        for comment in redditor.comments.new(limit=25):
            full_url = base_url + comment.permalink
            user_activity += f"Comment: {comment.body}\nURL: {full_url}\n\n"

        return redditor, user_activity
    except prawcore.exceptions.NotFound:
        st.error(f"Reddit user '{username}' could not be found. Please check the username and URL.", icon="🧐")
        return None, None
    except Exception as e:
        st.error(f"An error occurred while fetching data from Reddit: {e}", icon="🔥")
        return None, None

# --- 3. AI PERSONA GENERATION ---

def generate_user_persona(llm_client, user_activity: str, username: str) -> str:
    """
    Generates a detailed user persona using an LLM, with instructions for Markdown hyperlinks.
    """
    if not user_activity.strip():
        return "Not enough public activity found to generate a persona for this user."

    # The prompt is highly structured to guide the LLM's output for easy parsing.
    prompt = f"""
    Analyze the following Reddit activity from the user '{username}' to create a user persona.
    Your output MUST be in valid Markdown. For EACH characteristic, you MUST cite the source as a clickable Markdown hyperlink.
    Format citations like this: `[source](Full_URL_Here)`. Do NOT use plain text URLs.

    Structure the output EXACTLY as follows, using '###' for main headings:

    ### Bio/Quote
    A short, representative quote that summarizes the user's core attitude based on their comments.

    ### Demographics
    - **Age:** Infer an age range, followed by a brief justification. (e.g., 25-30. This is inferred from...) [source](URL)
    - **Occupation:** Infer occupation or student status, followed by a brief justification. [source](URL)
    - **Location:** Infer a location, followed by a brief justification. [source](URL)

    ### Behavior & Habits
    - *Detail online and offline behaviors in bullet points.* [source](URL)

    ### Motivations
    - *Identify key drivers for their actions in bullet points.* [source](URL)

    ### Frustrations
    - *Pinpoint their main challenges and annoyances in bullet points.* [source](URL)

    ### Goals & Needs
    - *Outline what they seem to aim for in bullet points.* [source](URL)

    ### Personality
    - *Characterize them with descriptive traits in bullet points.* [source](URL)

    ---
    **Reddit Activity Data:**
    {user_activity}
    """
    try:
        response = llm_client.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the AI model: {e}"

# --- 4. UI RENDERING ---

def parse_and_display_persona(persona_text: str):
    """
    Parses the Markdown persona string and displays it in a polished Streamlit UI
    with metric cards and collapsible expanders.
    """
    sections = re.split(r'###\s+', persona_text)
    
    # Process Bio/Quote first
    for section in sections:
        if section.startswith("Bio/Quote"):
            content = section.replace("Bio/Quote\n", "").strip()
            st.markdown(f"> {content}", unsafe_allow_html=True) # Render as a blockquote

    st.subheader("Key Details")
    
    # Isolate and display demographics in metric cards
    demographics_text = ""
    for section in sections:
        if section.startswith("Demographics"):
            demographics_text = section.replace("Demographics\n", "")
            break
            
    # Use non-greedy regex to capture just the core data point for the metric card
    age = re.search(r'\*\*Age:\*\* (.*?)\.', demographics_text)
    occupation = re.search(r'\*\*Occupation:\*\* (.*?)\.', demographics_text)
    location = re.search(r'\*\*Location:\*\* (.*?)\.', demographics_text)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Age", age.group(1).strip() if age else "N/A")
    with col2:
        st.metric("Occupation", occupation.group(1).strip() if occupation else "N/A")
    with col3:
        st.metric("Location", location.group(1).strip() if location else "N/A")

    st.markdown("---")

    # Display all sections (including full demographics) in expanders for a clean look
    for section in sections:
        if not section.strip(): continue
        
        parts = section.split('\n', 1)
        title = parts[0].strip()
        content = parts[1].strip() if len(parts) > 1 else ""
        
        if title not in ["Bio/Quote"]:
            with st.expander(f"**{title}**", expanded=True):
                st.markdown(content, unsafe_allow_html=True)


# --- 5. MAIN APPLICATION ---

def main():
    """The main function to run the Streamlit application."""
    st.set_page_config(page_title="Reddit Persona Generator", page_icon="🤖", layout="wide")
    
    st.title("🤖 AI-Powered Reddit Persona Generator")
    st.write("This tool creates a detailed user persona from a Reddit profile URL, complete with AI-driven insights and cited sources.")

    # Initialize APIs
    reddit_client, llm_client = initialize_apis()

    profile_url = st.text_input("Enter a Reddit User Profile URL", placeholder="e.g., https://www.reddit.com/user/kojied/")

    if st.button("✨ Generate Persona"):
        if profile_url and "reddit.com/user/" in profile_url:
            try:
                username = profile_url.split("/user/")[1].rstrip("/")
                
                with st.spinner(f"🕵️‍♂️ Analyzing '{username}'... Fetching recent activity..."):
                    redditor, reddit_activity = fetch_reddit_data(reddit_client, username)

                if redditor and reddit_activity:
                    st.success(f"Activity retrieved. Now asking the AI to build the persona...")
                    
                    with st.spinner("🧠 Crafting persona... This may take a moment..."):
                        persona_result = generate_user_persona(llm_client, reddit_activity, username)

                    st.markdown("---")
                    
                    col1, col2 = st.columns([1, 4]) # Profile pic column is smaller

                    with col1:
                        if hasattr(redditor, 'icon_img') and redditor.icon_img:
                            # FIX: Use use_container_width instead of deprecated use_column_width
                            st.image(redditor.icon_img, caption=f"{username}", use_column_width='auto')
                        else:
                            st.info("No profile picture available.")
                    
                    with col2:
                        st.header(f"User Persona: {username}")
                        parse_and_display_persona(persona_result)

                    # Save the generated persona to a text file
                    file_path = f"{username}_persona.txt"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"Persona for user: {username}\n\n{persona_result}")
                    st.success(f"Full persona report saved to `{file_path}`", icon="✅")

            except IndexError:
                st.error("Invalid URL format. Please ensure it is a full Reddit user profile URL.", icon="🚨")
            except Exception as e:
                st.error(f"A critical, unexpected error occurred: {e}", icon="🚨")
        else:
            st.warning("Please provide a valid Reddit user profile URL to proceed.", icon="⚠️")

if __name__ == "__main__":
    main()