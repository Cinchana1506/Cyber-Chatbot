import spacy
import gradio as gr
import requests
from bs4 import BeautifulSoup
import random

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Function to scrape live headlines from Cybersecurity Insiders
def get_live_cases():
    try:
        url = "https://www.cybersecurity-insiders.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)  # Increased timeout
        response.raise_for_status()  # Raises an error for bad status codes (e.g., 404)
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Updated: Try multiple selectors (fallback if one fails)
        articles = soup.find_all("h3", class_="jeg_post_title") or \
                  soup.find_all("h2", class_="post-title")  # Alternative class
        
        headlines = [a.text.strip() for a in articles[:5]]
        
        if not headlines:
            return " No recent headlines found. Check back later."
            
        return " Top Cybersecurity News:\n\n" + "\n".join(f"• {h}" for h in headlines)
        
    except Exception as e:
        print(f"[DEBUG] Scraping error: {e}")  # Log the error for debugging
        return "⚠️ Unable to fetch live cases right now. Try again later."

# Get response based on intent
def get_response(user_input):
    user_input = user_input.lower()
    if "live" in user_input or "case" in user_input or "news" in user_input:
        return get_live_cases()
    elif "scam" in user_input:
        return " Scams often trick users into giving up sensitive info. Be cautious!"
    elif "phishing" in user_input:
        return " Phishing tricks people into revealing data by impersonating trusted sources."
    elif "password" in user_input:
        return " Use strong passwords and enable 2FA for better protection."
    elif "privacy" in user_input:
        return "Don't overshare on social media. Review app permissions regularly."
    else:
        return "I can help with phishing, scams, passwords, or privacy. Try asking again, or ask for a live cyber case!"

# Gradio callback for chat interface
def chatbot(message, history):
    response = get_response(message)
    return response

# Chat Interface with custom CSS
with gr.Blocks(css="""
#chatbox {background-color: #f0f4f8; font-family: 'Segoe UI', sans-serif;}
.gr-chat-message.user {background-color: #e1f5fe; color: #000;}
.gr-chat-message.bot {background-color: #e8f5e9; color: #000;}
""") as demo:
    gr.Markdown("## 🛡️ CyberGuard — Your Cyber Safety Companion\nAsk me about **scams, phishing, passwords, privacy**, or type **'live cases'** to get current cybercrime news!")
    chat = gr.ChatInterface(
        fn=chatbot,
        chatbot=gr.Chatbot(elem_id="chatbox", label="CyberGuard Chat", height=400),
        examples=[
            "What is phishing?",
            "How do scams work?",
            "Tell me about password safety",
            "Show me live cases",
            "Any recent cyber attack?"
        ],
        cache_examples=False
    )

demo.launch()
