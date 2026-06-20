import streamlit as st
import os 
from dotenv import load_dotenv
from google.genai import Client
import imaplib
import email
from email.header import decode_header
import pywhatkit as kit
import time

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
phone_number = os.getenv("PHONE_NUMBER")

# Initialize Gemini client 
client = Client(api_key=api_key)

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="JARVIS Email Console", page_icon="🤖", layout="wide")

# --- CYBERPUNK GLASSMORPHISM INJECTION MATRIX ---
glassmorphism_css = """
<style>
/* Frosted Side Navigation Core */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.45) !important;
    backdrop-filter: blur(16px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
    border-right: 1px solid rgba(0, 255, 255, 0.1) !important;
}

/* Frosted Main Display Content Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(30, 41, 59, 0.35) !important;
    backdrop-filter: blur(10px) saturate(140%) !important;
    border: 1px solid rgba(0, 255, 255, 0.15) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
    margin-bottom: 15px !important;
}

/* Custom Alert Message Radii Override */
.stAlert {
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}
</style>
"""
st.markdown(glassmorphism_css, unsafe_allow_html=True)


# Sidebar for Controls
with st.sidebar:
    st.markdown("### 🖥️ System Core")
    st.info(f"**User:** {email_user.split('@')[0] if email_user else 'Unknown User'}")
    st.markdown("---")
    st.markdown("#### ⚙️ Operations")
    sync_button = st.button("🔄 Initialize Inbox Scan", use_container_width=True)

# Main Dashboard Title
st.title("🤖 JARVIS // Personal Email Console")
st.markdown("---")


# Function to safely connect to Gmail & fetch emails
def fetch_unread_emails():
    emails_list = []
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select("inbox")
        
        # Bypassing strict filters using the baseline "ALL" command
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            return []

        mail_ids = messages[0].split()
        latest_ids = mail_ids[-3:]  # Grab the latest 3 emails
        
        for mail_i in reversed(latest_ids):
            status, msg_data = mail.fetch(mail_i, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode Subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                    
                    # Decode Sender
                    from_sender, encoding = decode_header(msg["From"])[0]
                    if isinstance(from_sender, bytes):
                        from_sender = from_sender.decode(encoding if encoding else "utf-8", errors="ignore")
                    
                    # Extract Body
                    body = "" 
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                                except:
                                    pass
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")
                    
                    body = body[:500].strip()

                    emails_list.append({
                        "sender": from_sender,
                        "subject": subject,
                        "body": body if body else "No text payload detected."
                    })
                    
        mail.logout()
        return emails_list
        
    except Exception as e:
        st.sidebar.error(f"System Link Failed: {e}")
        return []


# --- MAIN LOGIC EXECUTION ---
if sync_button:
    with st.spinner("Establishing secure handshake with mail servers..."):
        unread_messages = fetch_unread_emails()

        if not unread_messages:
            st.info("Console Report: Main inbox is completely clear, Sir. No immediate data found.")
        else:
            st.success(f"Handshake complete. Retrieved {len(unread_messages)} data packets. Processing pipeline active.")

            # Loop through fetched emails
            for idx, msg in enumerate(unread_messages):
                with st.container(border=True):
                    col1, col2 = st.columns([1, 4])
                    
                    with col1:
                        st.markdown(f"### `PACKET #{idx+1}`")
                        st.caption("Incoming Data Stream")
                    
                    with col2:
                        st.markdown(f"**📧 From:** `{msg['sender']}`")
                        st.markdown(f"**📌 Subject:** {msg['subject']}")
                    
                    full_email_text = f"Subject: {msg['subject']}\nBody: {msg['body']}"

                    with st.spinner(f"JARVIS is decrypting packet #{idx+1}..."):
                        # --- RETRY MATRIX PROTOCOL (Bypassing Free Tier 503 Capacity Fluctuations) ---
                        ai_response = None
                        max_retries = 3
                        
                        for attempt in range(max_retries):
                            try:
                                ai_response = client.models.generate_content(
                                    model='gemini-3.5-flash',
                                    contents=(
                                        "You are JARVIS, the highly sophisticated AI assistant built by Tony Stark. "
                                        "Analyze the following email packet. "
                                        "On the VERY FIRST line of your response, you must output exactly either 'STATUS: CRITICAL' or 'STATUS: NORMAL'. "
                                        "Mark it as CRITICAL only if it concerns an exam schedule, hall ticket, lab test, official university notice, "
                                        "technical account lockout, or urgent action item. Otherwise, mark it as NORMAL.\n\n"
                                        "After the first line, address the user directly as 'Sir' and provide your briefing like this:\n"
                                        "**Intelligence Briefing:** (A sharp analytical summary)\n"
                                        "**Action Assessment:** (What to do, or a witty dismissal if it's junk spam)\n"
                                        "**Draft Protocol:** (Short response template if needed, else 'No draft required, Sir.')"
                                        f"\n\nHere is the data packet:\n{full_email_text}"
                                    ),
                                )
                                break  # Handshake secured. Terminating retry evaluations.
                            except Exception as e:
                                if ("503" in str(e) or "UNAVAILABLE" in str(e)) and attempt < max_retries - 1:
                                    time.sleep(2)  # Delay 2 seconds to absorb computing spike
                                    continue
                                else:
                                    st.error(f"AI Matrix Analysis Failure on Packet #{idx+1}: {e}")
                                    break
                        
                        # Process response if available
                        if ai_response:
                            try:
                                response_text = ai_response.text
                                
                                # Parse out the hidden status line for our Python loop logic
                                lines = response_text.split('\n')
                                status_line = lines[0] if lines else ""
                                
                                # Clean up the display text so the user doesn't see the ugly raw status line on the UI dashboard
                                display_text = response_text.replace("STATUS: CRITICAL", "").replace("STATUS: NORMAL", "").strip()
                                
                                st.markdown("#### 🦾 JARVIS Intelligence Report:")
                                st.info(display_text)
                                
                                # WHATSAPP TRIGGER PROTOCOL
                                if "STATUS: CRITICAL" in status_line:
                                    st.warning("🚨 Critical data packet detected! Initiating WhatsApp notification dispatch...")
                                    
                                    # Extract just the summary sentences for a quick phone alert text
                                    summary_line = "Urgent notice received, Sir."
                                    for line in lines:
                                        if "Intelligence Briefing:" in line:
                                            summary_line = line.replace("**Intelligence Briefing:**", "").strip()
                                    
                                    whatsapp_message = f"Sir, an urgent intelligence packet regarding '{msg['subject']}' has breached the terminal. Briefing: {summary_line}"
                                    
                                    # Send the WhatsApp message instantly via open browser tab
                                    kit.sendwhatmsg_instantly(phone_no=phone_number, message=whatsapp_message, wait_time=15, tab_close=True)
                                    st.success("📬 Alert package pushed to your mobile device successfully, Sir.")
                                    
                            except Exception as ai_err:
                                st.error(f"AI Matrix Analysis Failure: {ai_err}")