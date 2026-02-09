import os
import shutil
import json
from datetime import datetime, timedelta

# Define Vault Directory
VAULT_DIR = os.path.join(os.path.dirname(__file__), "vault_data")

def ensure_vault():
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)

def get_carrier_folder(identifier):
    """Get or create folder for a specific carrier ID"""
    clean_id = identifier.replace(":", "_").replace(" ", "_")
    folder = os.path.join(VAULT_DIR, clean_id)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def get_metadata_file(identifier):
    folder = get_carrier_folder(identifier)
    return os.path.join(folder, "metadata.json")

def load_metadata(identifier):
    path = get_metadata_file(identifier)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(identifier, data):
    path = get_metadata_file(identifier)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def save_document(identifier, file_obj, doc_type="General", expiry_date=None):
    """Save an uploaded file to the carrier's vault with optional expiry"""
    ensure_vault()
    folder = get_carrier_folder(identifier)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_name = file_obj.name.replace(" ", "_")
    filename = f"{doc_type}_{timestamp}_{sanitized_name}"
    path = os.path.join(folder, filename)
    
    with open(path, "wb") as f:
        f.write(file_obj.getbuffer())
        
    # Update Metadata
    meta = load_metadata(identifier)
    meta[filename] = {
        "original_name": file_obj.name,
        "type": doc_type,
        "uploaded_at": datetime.now().isoformat(),
        "expiry_date": expiry_date.isoformat() if expiry_date else None
    }
    save_metadata(identifier, meta)
        
    return path

def list_documents(identifier):
    """List all documents for a carrier with metadata"""
    ensure_vault()
    folder = get_carrier_folder(identifier)
    meta = load_metadata(identifier)
    
    files = []
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if f.startswith(".") or f == "metadata.json": continue
            
            path = os.path.join(folder, f)
            try:
                stat = os.stat(path)
            except:
                continue
                
            # Get metadata if exists, else parse filename
            file_meta = meta.get(f, {})
            
            doc_type = file_meta.get("type", "Unknown")
            orig_name = file_meta.get("original_name", f)
            expiry = file_meta.get("expiry_date")
            
            # Legacy fallback if not in metadata
            if doc_type == "Unknown":
                parts = f.split("_", 2)
                if len(parts) >= 3:
                    doc_type = parts[0]
            
            # Layout for UI
            files.append({
                "filename": f,
                "path": path,
                "type": doc_type,
                "name": orig_name,
                "size_kb": round(stat.st_size / 1024, 2),
                "uploaded_at": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "expiry_date": expiry
            })
            
    return files

def get_document_path(identifier, filename):
    folder = get_carrier_folder(identifier)
    return os.path.join(folder, filename)

def check_expiring_docs(days_threshold=30):
    """Check ALL vaults for expiring documents"""
    ensure_vault()
    alerts = []
    
    if not os.path.exists(VAULT_DIR):
        return []
        
    for carrier_id in os.listdir(VAULT_DIR):
        if carrier_id.startswith("."): continue
        
        meta = load_metadata(carrier_id)
        for filename, info in meta.items():
            expiry_str = info.get("expiry_date")
            if expiry_str:
                expiry = datetime.fromisoformat(expiry_str) # Expects YYYY-MM-DD format generally
                # If timestamp format, we might need verify. 
                # Startswith check handles ISO format typically.
                
                days_left = (expiry - datetime.now()).days
                
                if days_left < 0:
                    alerts.append(f"🔴 **EXPIRED**: {carrier_id} - {info['type']} (Expired {abs(days_left)} days ago)")
                elif days_left <= days_threshold:
                    alerts.append(f"⚠️ **EXPIRING SOON**: {carrier_id} - {info['type']} (Expires in {days_left} days)")
                    
    return alerts
