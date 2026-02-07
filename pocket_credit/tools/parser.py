import pdfplumber
import re
import os

# Try to import optional libraries for other formats
try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


def parse_credit_report(file_path):
    """
    Extracts derogatory accounts from a Credit Report.
    Supports: PDF, DOCX, TXT
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    print(f"🔍 Scanning: {os.path.basename(file_path)} ({file_ext})...")
    
    if file_ext == '.pdf':
        text = extract_from_pdf(file_path)
    elif file_ext in ['.docx', '.doc']:
        text = extract_from_docx(file_path)
    elif file_ext == '.txt':
        text = extract_from_txt(file_path)
    elif file_ext == '.pages':
        print("⚠️ Pages files use Apple's binary format. Please export as PDF.")
        return []
    else:
        print(f"❌ Unsupported file type: {file_ext}")
        return []
    
    if not text:
        print("⚠️ No text could be extracted from the file.")
        return []
    
    return find_negative_items_transunion(text)


def extract_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
            return full_text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""


def extract_from_docx(docx_path):
    if not HAS_DOCX:
        return ""
    try:
        doc = DocxDocument(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"❌ Error reading DOCX: {e}")
        return ""


def extract_from_txt(txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading TXT: {e}")
        return ""


def find_negative_items_transunion(text):
    """
    Parse TransUnion credit report format.
    Looks for the 'Accounts with Adverse Information' section.
    
    TransUnion format example:
        Account Name Account Balance Monthly
        Number Payment
        ATLANTIC CAP CRD000000009 - - -
        $105
        BKSELFLENDER 8161**** No Data
    """
    negative_items = []
    lines = text.split('\n')
    
    # Find the "Accounts with Adverse Information" section
    in_adverse_section = False
    skip_until_account = False
    
    # Known creditor name patterns (all caps, may contain spaces)
    CREDITOR_PATTERN = re.compile(r'^([A-Z][A-Z\s\-\.&]+)(?:\s+\d|\s+[A-Z0-9\*]+|\s*$)')
    
    # Patterns that indicate end of adverse section
    END_PATTERNS = ["Satisfactory Accounts", "Regular Inquiries", "Promotional Inquiries"]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for start of adverse section
        if "Accounts with Adverse" in line or "Adverse Information" in line:
            in_adverse_section = True
            print("  📍 Found Adverse Accounts section...")
            i += 1
            continue
        
        # Check for end of adverse section
        for end_pat in END_PATTERNS:
            if end_pat in line:
                in_adverse_section = False
                break
        
        if not in_adverse_section:
            i += 1
            continue
        
        # Skip header lines
        if "Account Name" in line or "Number" in line and "Payment" in line:
            i += 1
            continue
        
        # Skip empty lines and misc text
        if len(line) < 3 or line.startswith("opens in") or "FAQs" in line:
            i += 1
            continue
        
        # Try to identify account entries
        # Format: "CREDITOR NAME ACCOUNT#" followed by balance info
        
        # Check if this line starts with a creditor name (ALL CAPS word)
        first_word = line.split()[0] if line.split() else ""
        
        # Creditor names are all caps, not "No Data", not numbers
        if (first_word.isupper() and 
            len(first_word) > 1 and 
            first_word not in ["NO", "ACCOUNT", "CREDIT", "DATE", "THE", "FOR", "BALANCE", "MONTHLY"] and
            not first_word.startswith("$") and
            not first_word.isdigit()):
            
            # This looks like a creditor line
            creditor_name = ""
            account_num = ""
            balance = "0"
            
            # Extract creditor name (all caps portion)
            parts = line.split()
            name_parts = []
            for j, part in enumerate(parts):
                # Stop when we hit the account number (contains * or is mostly digits)
                if '*' in part or (len(part) > 6 and sum(c.isdigit() for c in part) > 3):
                    account_num = part
                    break
                # Stop at balance
                if part.startswith('$'):
                    balance = part.replace('$', '').replace(',', '')
                    break
                if part.upper() == part and len(part) > 1:
                    name_parts.append(part)
            
            creditor_name = ' '.join(name_parts).strip()
            
            # If no account num in this line, check next line
            if not account_num and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Account numbers have * or lots of digits
                if re.match(r'^[\dA-Z\*]+$', next_line) and ('*' in next_line or len(next_line) > 4):
                    account_num = next_line
                    i += 1
            
            # Look for balance in current line or next few lines
            if balance == "0":
                # Check current line for $ amount
                balance_match = re.search(r'\$[\d,]+\.?\d*', line)
                if balance_match:
                    balance = balance_match.group().replace('$', '').replace(',', '')
                else:
                    # Check next 2 lines
                    for look_ahead in range(1, 3):
                        if i + look_ahead < len(lines):
                            next_l = lines[i + look_ahead].strip()
                            if next_l.startswith('$'):
                                balance = next_l.replace('$', '').replace(',', '')
                                break
            
            # Only add if we got a creditor name
            if creditor_name and len(creditor_name) > 2:
                # Skip if it's actually a header or description
                skip_names = ["ACCOUNT NAME", "CREDIT REPORT", "TRANSUNION", "FILE NUMBER", 
                              "DATE CREATED", "PERSONAL INFORMATION", "ADVERSE INFORMATION"]
                if creditor_name not in skip_names:
                    item = {
                        "creditor": creditor_name,
                        "status": "Adverse/Derogatory",
                        "account_num": account_num or "See Report",
                        "balance": balance,
                        "original_text": line[:100]
                    }
                    
                    # Avoid duplicates
                    is_dupe = any(n['creditor'] == item['creditor'] for n in negative_items)
                    if not is_dupe:
                        negative_items.append(item)
                        print(f"  ⚠️ Found: {creditor_name} | Acct: {account_num or 'N/A'} | ${balance}")
        
        i += 1
    
    # If we didn't find the adverse section, fall back to keyword search
    if not negative_items:
        print("  ⚠️ No adverse section found, using keyword search...")
        negative_items = find_by_keywords(text)
    
    print(f"📊 Total negative items found: {len(negative_items)}")
    return negative_items


def find_by_keywords(text):
    """Fallback: search for keywords if section-based parsing fails"""
    negative_items = []
    
    KEYWORDS = ["COLLECTION", "CHARGE OFF", "CHARGED OFF", "LATE", "DELINQUENT", 
                "PAST DUE", "REPOSSESSION", "FORECLOSURE"]
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        upper = line.upper()
        for kw in KEYWORDS:
            if kw in upper and len(line) > 20:
                # Try to extract info
                balance_match = re.search(r'\$[\d,]+\.?\d*', line)
                balance = balance_match.group().replace('$', '').replace(',', '') if balance_match else "0"
                
                item = {
                    "creditor": lines[i-1].strip()[:50] if i > 0 else "Unknown",
                    "status": kw,
                    "account_num": "See Report",
                    "balance": balance,
                    "original_text": line[:100]
                }
                
                if item not in negative_items:
                    negative_items.append(item)
                break
    
    return negative_items


if __name__ == "__main__":
    print("Parser Module Ready.")
