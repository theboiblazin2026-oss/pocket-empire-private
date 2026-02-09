import os
import pandas as pd
import time
import shutil
from datetime import datetime
try:
    from .lead_manager import score_by_identifier
except ImportError:
    try:
        from lead_manager import score_by_identifier
    except ImportError:
        # Fallback for manual run
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from lead_manager import score_by_identifier

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Where scrapers dump files
INCOMING_DIR = os.path.join(BASE_DIR, "incoming_feeds")
# Where processed files go
ARCHIVE_DIR = os.path.join(BASE_DIR, "processed_feeds")
# Where high-quality leads are saved (or we just use the main db)
RESULTS_DIR = os.path.join(BASE_DIR, "pipeline_results")

def ensure_dirs():
    for d in [INCOMING_DIR, ARCHIVE_DIR, RESULTS_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)

def process_feed_file(filepath):
    """Process a single CSV file of leads"""
    print(f"Processing {os.path.basename(filepath)}...")
    try:
        df = pd.read_csv(filepath)
        
        # Find ID column
        id_col = None
        for col in df.columns:
            if col.upper() in ["MC", "MC_NUMBER", "DOT", "DOT_NUMBER", "USDOT"]:
                id_col = col
                break
        
        if not id_col:
            print("❌ No ID column found (MC/DOT)")
            return False

        results = []
        for index, row in df.iterrows():
            identifier = str(row[id_col])
            print(f"  Scoring {identifier}...")
            res = score_by_identifier(identifier)
            
            # Auto-Filter: Only keep if not error
            if "error" not in res:
                flat = {
                    "input_id": identifier,
                    "score": res.get("score"),
                    "risk": res.get("risk_level"),
                    "company": res.get("carrier_data", {}).get("legal_name"),
                    "processed_at": datetime.now().isoformat()
                }
                results.append(flat)
                
        # Save Results
        if results:
            out_df = pd.DataFrame(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_name = f"scored_{timestamp}_{os.path.basename(filepath)}"
            out_path = os.path.join(RESULTS_DIR, out_name)
            out_df.to_csv(out_path, index=False)
            print(f"✅ Saved results to {out_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def run_pipeline_once():
    """Check for files and process them"""
    ensure_dirs()
    
    files = [f for f in os.listdir(INCOMING_DIR) if f.endswith(".csv")]
    
    if not files:
        print("📭 No new feeds found.")
        return
        
    print(f"🚀 Found {len(files)} new feed files.")
    
    for f in files:
        path = os.path.join(INCOMING_DIR, f)
        success = process_feed_file(path)
        
        # Move to archive
        if success:
            shutil.move(path, os.path.join(ARCHIVE_DIR, f))
            print(f"📦 Archived {f}")
        else:
            print(f"⚠️ Skipped {f}")

if __name__ == "__main__":
    run_pipeline_once()
