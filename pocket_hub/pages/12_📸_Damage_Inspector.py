import streamlit as st
import os
import base64
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.set_page_config(page_title="Damage Inspector", page_icon="📸", layout="wide")

st.title("📸 Damage Inspector")
st.caption("Upload BOLs or Vehicle Photos, Mark Damages, and Sign.")

# --- Upload ---
upload_col, controls_col = st.columns([1, 1])

with upload_col:
    bg_image = st.file_uploader("Upload Image (BOL / Vehicle Photo)", type=["png", "jpg", "jpeg"])

with controls_col:
    st.subheader("✏️ Annotation Tools")
    mode = st.radio("Tool", ["freedraw", "line", "rect", "circle", "transform"], horizontal=True)
    stroke_width = st.slider("Stroke width: ", 1, 10, 2)
    
    # Color Presets
    color_choice = st.radio("Color", ["🔴 Red", "🔵 Blue", "⚫ Black", "🟢 Green", "🟡 Yellow", "🎨 Custom"], horizontal=True, index=0)
    
    if color_choice == "🔴 Red": stroke_color = "#FF0000"
    elif color_choice == "🔵 Blue": stroke_color = "#0000FF"
    elif color_choice == "⚫ Black": stroke_color = "#000000"
    elif color_choice == "🟢 Green": stroke_color = "#008000"
    elif color_choice == "🟡 Yellow": stroke_color = "#FFFF00"
    else:
        stroke_color = st.color_picker("Custom color: ", "#FF0000")

# --- Canvas ---
if bg_image:
    image = Image.open(bg_image)
    # Resize for canvas if too big
    w, h = image.size
    aspect = h / w
    canvas_width = 700
    canvas_height = int(canvas_width * aspect)
    
    st.markdown("### Mark Damage & Sign Below")
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_image=image,
        update_streamlit=True,
        display_toolbar=True, # Added Undo/Redo toolbar
        height=canvas_height,
        width=canvas_width,
        drawing_mode=mode,
        key="damage_canvas",
    )
    
    st.divider()
    
    # --- Export ---
    # --- Export ---
    if canvas_result.image_data is not None:
        st.subheader("📤 Save / Share")
        
        # Convert numpy array to image
        result_image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        
        # Composite over background
        bg_resized = image.resize((canvas_width, canvas_height))
        bg_resized.paste(result_image, (0, 0), result_image)
        
        # Save to buffer
        buf = io.BytesIO()
        bg_resized.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        # base64 encode for DB
        b64_img = base64.b64encode(byte_im).decode('utf-8')
        
        col_actions = st.columns([1, 1, 1])
        
        with col_actions[0]:
            st.download_button(
                label="⬇️ Download",
                data=byte_im,
                file_name="annotated_damage.png",
                mime="image/png"
            )
            
        with col_actions[1]:
            # Save to Cloud
            if st.button("☁️ Save to Cloud"):
                import sys
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
                from pocket_core.db import save_inspection_db
                
                inspection_data = {
                    "title": f"Inspection {os.path.basename(bg_image.name)}",
                    "image_data": b64_img,
                    "annotation_data": canvas_result.json_data,
                    "created_at": "now()"
                }
                
                if save_inspection_db(inspection_data):
                    st.success("Saved to Database!")
                else:
                    st.error("Using Local/Offline Mode (DB Unreachable)")
        
        with col_actions[2]:
            email = st.text_input("Email to:", placeholder="claims@insurance.com", label_visibility="collapsed")
            if st.button("📧 Send"):
                st.info("Email simulated.")
else:
    st.info("👈 Upload a Photo or Bill of Lading (BOL) to start.")
