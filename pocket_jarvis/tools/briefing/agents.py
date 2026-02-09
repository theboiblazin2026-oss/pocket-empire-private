import os
import re
from datetime import datetime, timedelta

def get_agent_stats():
    """
    Scrapes logs from the SSD to get yesterday's/today's stats.
    """
    stats = {
        "enricher_emails": 0,
        "enricher_status": "Unknown",
        "lead_puller_leads": 0,
        "lead_puller_status": "Unknown"
    }

    # Paths (Hardcoded to SSD as discovered)
    enricher_log = "/Volumes/CeeJay SSD/Truck Scraper Master File/scraper.log"
    puller_log = "/Volumes/CeeJay SSD/Projects/lead puller/automation.log"

    # --- 1. Lead Enricher Stats ---
    if os.path.exists(enricher_log):
        try:
            # We want to find "Sent X emails" lines from TODAY
            # Log format usually has timestamps or we just grep the file end
            # Simplification: Read last 200 lines and look for "Sent X emails" or "Campaign Complete"
            with open(enricher_log, 'r') as f:
                lines = f.readlines()[-300:]
            
            content = "".join(lines)
            if "Execution Successful" in content or "Enrichment Complete" in content:
                stats['enricher_status'] = "🟢 Active"
            elif "Execution Failed" in content:
                stats['enricher_status'] = "🔴 Failed"
            
            # Regex for "Sent X emails" or similar. 
            # From log check: "Sent 49 emails."
            sent_matches = re.findall(r"Sent (\d+) emails", content)
            if sent_matches:
                # Summing might be risky if duplicated, but usually it prints total at end.
                # Let's take the last match which is usually the summary.
                stats['enricher_emails'] = int(sent_matches[-1])
        except Exception as e:
            stats['enricher_status'] = f"❌ Error: {e}"
    else:
        stats['enricher_status'] = "❌ Log Not Found"

    # --- 2. Lead Puller Stats ---
    if os.path.exists(puller_log):
        try:
            with open(puller_log, 'r') as f:
                lines = f.readlines()[-300:]
            
            content = "".join(lines)
            if "Job Wrapper Finished with code 0" in content:
                stats['lead_puller_status'] = "🟢 Active"
            
            # Regex for "Found X records" or "Extracted Total X"
            # From log check: "Found 2121 records"
            # We want the 'Fresh' count usually.
            found_matches = re.findall(r"Found (\d+) records", content)
            if found_matches:
                 # Be careful, could be total. Let's grab the max or last.
                 stats['lead_puller_leads'] = found_matches[-1]
                 
        except Exception as e:
            stats['lead_puller_status'] = f"❌ Error: {e}"
    else:
        stats['lead_puller_status'] = "❌ Log Not Found"

    return stats

if __name__ == "__main__":
    print(get_agent_stats())
