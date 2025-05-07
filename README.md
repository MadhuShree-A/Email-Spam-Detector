#  Email Spam Detector using IMAP and Trie

This Python project connects to a Gmail account using IMAP, retrieves all emails from the inbox, and classifies each email as **spam** or **ham** based on keyword detection and presence of links. It uses a Trie data structure for efficient spam keyword lookup.


##  Features

-  Secure login with Gmail via IMAP
-  Automatically retrieves all inbox emails
-  Classifies emails using:
  - Trie-based keyword matching
  - Regex link detection
-  Displays sender, subject, and spam/ham classification


## Technologies Used

- `imaplib` and `email` (Python standard library) — for connecting to and parsing emails
- `re` — for detecting links via regular expressions
- Trie data structure — for efficient keyword matching


##  How It Works

1. Connects securely to Gmail via `imap.gmail.com`.
2. Fetches all emails from the inbox.
3. Extracts subject, sender, and body of each email.
4. Converts the body to lowercase and checks for:
   - Spam keywords stored in a **Trie**
   - Presence of **links**
5. Classifies the email as **Spam** or **Ham**.


##  Prerequisites

- **Enable IMAP** in your Gmail settings.
- **Generate an App Password**:
  - Go to [Google Account > Security > App Passwords](https://myaccount.google.com/apppasswords)
  - Generate an app password for "Mail" and "Windows Computer" (or other).
  - Use this password in place of your Gmail password in the script.



