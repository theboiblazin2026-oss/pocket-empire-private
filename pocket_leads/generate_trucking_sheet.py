import json
import os

LEADS_FILE = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_leads/data/new_authorities.json"
OUTPUT_FILE = "/Users/newguy/.gemini/antigravity/brain/9f9ec288-5a66-4f35-85b5-ad773cec8808/trucking_call_hit_list.md"

def main():
    if not os.path.exists(LEADS_FILE):
        print(f"[-] Error: {LEADS_FILE} not found.")
        return

    with open(LEADS_FILE, "r") as f:
        prospects = json.load(f)

    # We specifically want the newest 27 leads (or the ones added today)
    # The JSON is ordered, usually newest at the top or bottom depending on how it was appended.
    # Looking at the scraper logic, it appended newest leads. Let's filter for just the ones scraped today.
    import datetime
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    new_leads = [p for p in prospects if today_str in p.get("found_at", "")]
    
    with open(OUTPUT_FILE, "w") as f:
        f.write("# 🚚 B2B Trucking Call Sheet: New MC Authorities\n\n")
        f.write("*These companies just registered their MC Number with the FMCSA today. They are highly motivated but overwhelmed. Pitch the $1,497 Road Ready Package, down-sell to $1,000 Authority Starter.*\n\n")
        
        valid_count = 0
        for lead in new_leads:
            name = lead.get("legal_name", "Unknown")
            phone = lead.get("phone", "No Phone Available")
            mc = lead.get("mc_number", "Unknown")
            
            if name != "Unknown" and phone:
                valid_count += 1
                f.write(f"### {valid_count}. {name} (MC: {mc})\n")
                f.write(f"- **Phone:** {phone}\n")
                f.write(f"- **Notes:** Newly registered authority.\n\n")

    print(f"[+] Call List Generated: {OUTPUT_FILE} with {valid_count} valid numbers.")

if __name__ == "__main__":
    main()
