
# 👑 Pocket Empire (2026 Edition)
**The Ultimate Solopreneur Operating System**

Pocket Empire is a modular, AI-powered command center designed to run a trucking and logistics business from a single dashboard. It integrates lead generation, CRM, invoicing, legal assistance, and credit repair into a unified Streamlit application.

## 🚀 Key Features

*   **⛏️ Prospector**: Automated Lead Generation.
    *   **Web Hunter**: Scrapes Google Maps for local business leads.
    *   **Fleet Manager**: Pulls new carrier authority data from the FMCSA daily.
    *   **Email Studio**: Built-in HTML email editor with "Tech Trap Solutions" branding.
    *   **Auto-Blaster**: One-click email campaigns with persistent status tracking.
*   **📋 Lead Pipeline**: Kanban-style CRM.
    *   **AI Analyst**: Analyzes email replies using Google Gemini to detect sentiment (Interested/Not Interested).
    *   **Smart Sync**: Two-way sync with Google Sheets.
    *   **Convert to Client**: Instantly turn a "Won" lead into a billable client.
*   **💳 Invoices**: Professional PDF invoice generation and client management.
*   **⚖️ Pocket Lawyer**: AI-powered legal assistant for FMCSA/DOT compliance and contract review.
*   **🔨 Credit Repair**: DIY credit dispute generation and tracking module.

## 🛠️ Installation & Setup

### 1. Prerequisites
*   Python 3.10+
*   Google Cloud Platform Account (for Sheets/Gmail APIs)
*   Gemini API Key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration (`.streamlit/secrets.toml`)
Create a `.streamlit/secrets.toml` file in the root directory with the following structure:

```toml
# Security
app_password = "YOUR_APP_PASSWORD"

# Google Sheets & Drive (Service Account)
[connections.gspread]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----..."
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"

# Gmail Configuration (SMTP)
[fleet_manager]
email_address = "your-email@gmail.com"
app_password = "your-gmail-app-password"
smtp_server = "smtp.gmail.com"
smtp_port = 587
your_name = "Your Name"

# Gemini AI
[gemini]
api_key = "YOUR_GEMINI_API_KEY"
```

### 4. Running the App
The central hub links all modules together. Run from the project root:

```bash
streamlit run pocket_hub/Home.py
```

## 📂 Project Structure
*   `pocket_hub/`: Main application navigation and "Home" dashboard.
    *   `pages/`: Individual modules (Prospector, Pipeline, Lawyer, etc.).
*   `pocket_leads/`: Core logic for scraping and email automation.
*   `pocket_invoices/`: Invoice generation logic.
*   `pocket_lawyer/`: RAG (Retrieval-Augmented Generation) logic for legal AI.
*   `scripts/`: Automation scripts (Daily Backup, Lead Pruning).

## 🛡️ Safety Features
*   **Daily Backups**: All data (Leads, Invoices, Credit) is zipped and saved to `backups/` daily.
*   **Kill Switch**: Stop all automation instantly from the Settings menu.
*   **Secure Storage**: No hardcoded keys; all credentials use `secrets.toml`.

---
*Powered by Tech Trap Solutions*
