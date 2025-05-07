import imaplib
import email
from email.header import decode_header
import re

class TrieNode:
    """A node in the trie."""
    def __init__(self):
        self.children = {}
        self.is_end_of_keyword = False

class Trie:
    """A trie for storing keywords."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_keyword = True

    def search(self, word):
        """Search for a word in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_keyword

def connect_to_email(username, app_password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        result, response = mail.login(username, app_password)
        print(f"Login result: {result}")
        return mail
    except imaplib.IMAP4.error as e:
        print(f"Login failed: {str(e)}")
        raise




def classify_email(email_body, spam_trie):
    """Classify an email as spam or ham based on keywords."""
    email_body = email_body.lower()
    
    # Regex for detecting links
    links = re.findall(r'http[s]?://\S+', email_body)

    # Check for spam keywords in the email body
    for word in email_body.split():
        if spam_trie.search(word):
            return True  # Classified as spam

    # Check for links in the email body
    if links:
        return True  # If there are links, classify as spam

    return False  # Classified as ham

def retrieve_and_classify_emails(mail_connection):
    """Retrieve emails from the inbox and classify them."""
    mail_connection.select("inbox")
    status, messages = mail_connection.search(None, "ALL")
    email_ids = messages[0].split()
    print(f"Total emails: {len(email_ids)}")

    # Create a Trie for spam keywords
    spam_trie = Trie()
    spam_keywords = [
        "free", "win", "winner", "prize", "click", "here", 
        "subscribe", "act", "now", "limited", "time", 
        "offer", "buy", "discount", "urgent", "call",
        "money", "cash", "save big", "risk free", "100% free"
    ]

    for keyword in spam_keywords:
        spam_trie.insert(keyword)

    # Process all emails
    for email_id in email_ids:  # Process all emails without limit
        res, msg = mail_connection.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')

        sender = msg.get("From")
        email_body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            email_body += payload.decode('utf-8')
                        except UnicodeDecodeError:
                            email_body += payload.decode('ISO-8859-1', errors='ignore')

        else:
            payload = msg.get_payload(decode=True)
            if payload:
                try:
                    email_body = payload.decode('utf-8')
                except UnicodeDecodeError:
                    email_body = payload.decode('ISO-8859-1', errors='ignore')

        is_spam = classify_email(email_body, spam_trie)

        print(f"Email from: {sender} - Subject: {subject} - Classified as: {'Spam' if is_spam else 'Ham'}")

def main():
    username = "adspackage24@gmail.com"  # Your Gmail address
    app_password = "gryt yfkq znnx eayw"  # Your app-specific password for Gmail

    mail_connection = connect_to_email(username, app_password)
    retrieve_and_classify_emails(mail_connection)

    mail_connection.logout()

if __name__ == "__main__":
    main()
