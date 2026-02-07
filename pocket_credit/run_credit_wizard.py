import os
import glob
from tools.parser import parse_credit_report
from tools.writer import DisputeWriter
from dotenv import load_dotenv

load_dotenv()

# We need user info to fill the letters. 
# For now, we simulate asking, or read from .env if available.
USER_DATA = {
    "name": os.getenv("CREDIT_NAME", "YOUR NAME HERE"),
    "address": os.getenv("CREDIT_ADDRESS", "YOUR ADDRESS HERE"),
    "ssn": os.getenv("CREDIT_SSN", "XXX-XX-XXXX"),
    "dob": os.getenv("CREDIT_DOB", "MM/DD/YYYY")
}

INPUT_DIR = "pocket_credit/input_reports"
ARCHIVE_DIR = "pocket_credit/archive"

def main():
    print("🧙‍♂️ Credit Repair Wizard Started...")
    
    # 1. Find PDFs
    pdfs = glob.glob(os.path.join(INPUT_DIR, "*.pdf"))
    
    if not pdfs:
        print(f"❌ No PDF reports found in {INPUT_DIR}. Please drop your Experian/TransUnion/Equifax PDF there.")
        return

    writer = DisputeWriter()
    
    for pdf in pdfs:
        print(f"\n📄 Processing: {os.path.basename(pdf)}")
        
        # 2. Parse (AI/OCR)
        items = parse_credit_report(pdf)
        
        if not items:
            print("   ⚠️ No negative items found (or parsing failed).")
            continue
            
        print(f"   found {len(items)} negative items:")
        for i in items:
            print(f"    - {i['creditor']} ({i['status']})")
            
        # 3. Generate Letter
        output_path = writer.generate_round1(USER_DATA, items)
        print(f"   ✅ Generated Dispute Letter: {output_path}")
        
    print("\n🎉 All Done! Check output_letters folder.")

if __name__ == "__main__":
    main()
