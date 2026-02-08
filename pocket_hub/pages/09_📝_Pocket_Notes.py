import streamlit as st
import os
import json
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
import base64

st.set_page_config(page_title="Pocket Notes", page_icon="📝", layout="wide")

st.title("📝 Pocket Notes")
st.caption("Jot down ideas, sketch diagrams, or handwrite notes.")

# --- Storage ---
# --- Storage ---
# Local Fallback
NOTES_DIR = os.path.join(os.path.dirname(__file__), "../pocket_notes_data")
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# Import DB functions
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from pocket_core.db import fetch_notes, save_note_db

def save_note(title, content, drawing_data=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Try DB first
    note_data = {
        "title": title,
        "content": content,
        "drawing_data": drawing_data, # DB handles JSON
        "created_at": datetime.now().isoformat()
    }
    
    success = save_note_db(note_data)
    
    if success:
        return "saved_to_cloud"
    
    # 2. Fallback to Local
    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    if not safe_title: safe_title = "Untitled"
    
    local_note = {
        "title": title,
        "content": content,
        "timestamp": timestamp,
        "drawing": drawing_data
    }
    
    filename = f"{safe_title}_{timestamp}.json"
    with open(os.path.join(NOTES_DIR, filename), 'w') as f:
        json.dump(local_note, f, indent=2)
    return "saved_locally"

def load_notes():
    all_notes = []
    
    # 1. Fetch from DB
    db_notes = fetch_notes()
    if db_notes:
        for n in db_notes:
            all_notes.append({
                "title": n.get('title'),
                "content": n.get('content'),
                "drawing": n.get('drawing_data'),
                "timestamp": n.get('created_at'),
                "source": "☁️ Cloud"
            })
            
    # 2. Fetch from Local (merge/dedupe logic could be added, for now just show both)
    if os.path.exists(NOTES_DIR):
        for f in os.listdir(NOTES_DIR):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(NOTES_DIR, f), 'r') as file:
                        local_n = json.load(file)
                        local_n['source'] = "💻 Local"
                        all_notes.append(local_n)
                except:
                    pass
    
    return sorted(all_notes, key=lambda x: x.get('timestamp', ''), reverse=True)

# --- Sidebar ---
with st.sidebar:
    st.header("📚 Notebook")
    if st.button("➕ New Note"):
        st.session_state.current_note = None
        st.rerun()
    
    st.divider()
    
    notes = load_notes()
    for note in notes:
        icon = note.get('source', '')
        # Truncate title
        display_title = note.get('title', 'Untitled')[:20]
        if st.button(f"{icon} {display_title}", key=f"{note.get('timestamp')}_{display_title}"):
            st.session_state.current_note = note
            st.rerun()

# --- Main Editor ---
current_note = st.session_state.get("current_note", None)

c1, c2 = st.columns([3, 1])
if current_note and 'source' in current_note:
    st.caption(f"Editing from: {current_note['source']}")

with c1:
    title = st.text_input("Title", value=current_note.get("title", "") if current_note else "", placeholder="Meeting Notes...")

with c2:
    mode = st.radio("Mode", ["Text", "Draw/Handwrite"], horizontal=True)

if mode == "Text":
    content = st.text_area("Content", value=current_note.get("content", "") if current_note else "", height=400)
    drawing_data = current_note.get("drawing") if current_note else None
else:
    content = current_note.get("content", "") if current_note else ""
    st.markdown("### ✏️ Canvas")
    
    # Tool Mode Selection (including Eraser)
    tool_col, settings_col = st.columns([1, 1])
    
    with tool_col:
        drawing_mode = st.radio("🔧 Tool", ["✏️ Draw", "🧽 Eraser", "📏 Line", "⬜ Rectangle", "⭕ Circle"], horizontal=True, index=0)
        
        if drawing_mode == "✏️ Draw": mode = "freedraw"
        elif drawing_mode == "🧽 Eraser": mode = "freedraw"  # Eraser uses white color
        elif drawing_mode == "📏 Line": mode = "line"
        elif drawing_mode == "⬜ Rectangle": mode = "rect"
        else: mode = "circle"
    
    with settings_col:
        stroke_width = st.slider("Stroke width: ", 1, 25, 3 if drawing_mode != "🧽 Eraser" else 15)
    
    # Color Presets (disabled for eraser)
    if drawing_mode == "🧽 Eraser":
        stroke_color = "#ffffff"  # White for eraser
        st.info("🧽 Eraser mode - draw to erase")
    else:
        color_choice = st.radio("Ink Color", ["⚫ Black", "🔵 Blue", "🔴 Red", "🟢 Green", "🟡 Yellow", "🎨 Custom"], horizontal=True, index=0)
        
        if color_choice == "⚫ Black": stroke_color = "#000000"
        elif color_choice == "🔵 Blue": stroke_color = "#0000FF"
        elif color_choice == "🔴 Red": stroke_color = "#FF0000"
        elif color_choice == "🟢 Green": stroke_color = "#008000"
        elif color_choice == "🟡 Yellow": stroke_color = "#FFFF00"
        else:
            stroke_color = st.color_picker("Stroke color: ", "#000000")
        
    bg_color = st.color_picker("Background color: ", "#ffffff")
    
    # Create a canvas component
    initial_drawing = current_note.get("drawing") if current_note else None
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        initial_drawing=initial_drawing,
        update_streamlit=True,
        display_toolbar=True,
        height=500,
        drawing_mode=mode,
        key="canvas",
    )
    
    # Handle Canvas Data
    if canvas_result.json_data is not None:
        drawing_data = canvas_result.json_data
    else:
        drawing_data = None

st.divider()

if st.button("💾 Save Note", type="primary"):
    if title:
        status = save_note(title, content, drawing_data)
        if status == "saved_to_cloud":
            st.success("☁️ Note Saved to Cloud!")
        else:
            st.warning("⚠️ Cloud unreachable. Saved locally!")
    else:
        st.error("Please enter a title.")
