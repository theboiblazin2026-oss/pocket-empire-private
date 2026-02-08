import streamlit as st
import os
import base64
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
from datetime import datetime

st.set_page_config(page_title="Damage Inspector", page_icon="📸", layout="wide")

st.title("📸 Damage Inspector")
st.caption("Capture or Upload BOLs/Vehicle Photos, Mark Damages, Sign, and Generate Custom BOLs.")

# --- Tabs for different modes ---
tab1, tab2, tab3 = st.tabs(["📷 Capture & Annotate", "📝 BOL Data Entry", "📄 Generate BOL"])

with tab1:
    st.subheader("📷 Capture or Upload")
    
    # CSS to make camera view larger
    st.markdown("""
    <style>
    /* Make camera input larger */
    [data-testid="stCameraInput"] > div {
        width: 100% !important;
    }
    [data-testid="stCameraInput"] video,
    [data-testid="stCameraInput"] img {
        width: 100% !important;
        max-width: 600px !important;
        height: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # --- Camera / Upload Options ---
    input_method = st.radio("📥 Input Method", ["📁 Upload File", "📸 Take Photo"], horizontal=True)
    
    if input_method == "📁 Upload File":
        bg_image = st.file_uploader("Upload Image (BOL / Vehicle Photo)", type=["png", "jpg", "jpeg"])
    else:
        st.info("💡 **Tip:** Use your device's native camera for zoom/flash controls, then upload the photo.")
        bg_image = st.camera_input("Take a photo", key="damage_camera")
    
    st.divider()
    
    # Annotation Tools in expander when image is loaded
    with st.expander("✏️ Annotation Tools", expanded=True):
        # Tool Mode Selection (including Eraser)
        drawing_mode = st.radio("🔧 Tool", ["✏️ Draw", "🧽 Eraser", "📏 Line", "⬜ Rect", "⭕ Circle", "🔄 Move"], horizontal=True, index=0)
        
        if drawing_mode == "✏️ Draw": mode = "freedraw"
        elif drawing_mode == "🧽 Eraser": mode = "freedraw"
        elif drawing_mode == "📏 Line": mode = "line"
        elif drawing_mode == "⬜ Rect": mode = "rect"
        elif drawing_mode == "⭕ Circle": mode = "circle"
        else: mode = "transform"
        
        stroke_width = st.slider("Stroke width: ", 1, 15, 2 if drawing_mode != "🧽 Eraser" else 10)
        
        # Color Presets
        if drawing_mode == "🧽 Eraser":
            stroke_color = "#ffffff"
            st.info("🧽 Eraser mode active")
        else:
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
        w, h = image.size
        aspect = h / w
        canvas_width = 700
        canvas_height = int(canvas_width * aspect)
        
        st.markdown("### ✍️ Mark Damage & Sign Below")
        st.caption("Use the toolbar below canvas for Undo/Redo/Clear")
        
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_image=image,
            update_streamlit=True,
            display_toolbar=True,
            height=canvas_height,
            width=canvas_width,
            drawing_mode=mode,
            key="damage_canvas",
        )
        
        st.divider()
        
        # --- Export ---
        if canvas_result.image_data is not None:
            st.subheader("📤 Save / Share")
            
            result_image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            bg_resized = image.resize((canvas_width, canvas_height))
            bg_resized.paste(result_image, (0, 0), result_image)
            
            buf = io.BytesIO()
            bg_resized.save(buf, format="PNG")
            byte_im = buf.getvalue()
            b64_img = base64.b64encode(byte_im).decode('utf-8')
            
            col_actions = st.columns([1, 1, 1])
            
            with col_actions[0]:
                st.download_button(
                    label="⬇️ Download",
                    data=byte_im,
                    file_name=f"damage_{datetime.now().strftime('%Y%m%d_%H%M')}.png",
                    mime="image/png"
                )
                
            with col_actions[1]:
                if st.button("☁️ Save to Cloud"):
                    import sys
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
                    from pocket_core.db import save_inspection_db
                    
                    inspection_data = {
                        "title": f"Inspection {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                        "image_data": b64_img,
                        "annotation_data": canvas_result.json_data,
                        "created_at": "now()"
                    }
                    
                    if save_inspection_db(inspection_data):
                        st.success("✅ Saved to Cloud!")
                    else:
                        st.warning("📱 Saved Locally (Offline Mode)")
            
            with col_actions[2]:
                if st.button("📧 Email"):
                    st.info("Email integration coming soon!")
    else:
        st.info("👈 Upload a Photo or use Camera to capture a BOL / Vehicle Photo.")

with tab2:
    st.subheader("📝 Enter BOL Data")
    st.caption("Fill in missing information from the Bill of Lading")
    
    with st.form("bol_data_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📍 Origin**")
            shipper_name = st.text_input("Shipper Name", placeholder="ABC Shipping Co.")
            shipper_address = st.text_area("Shipper Address", placeholder="123 Main St, City, State, ZIP", height=80)
            pickup_date = st.date_input("Pickup Date")
            
        with col2:
            st.markdown("**📍 Destination**")
            consignee_name = st.text_input("Consignee Name", placeholder="XYZ Receiving Inc.")
            consignee_address = st.text_area("Consignee Address", placeholder="456 Oak Ave, City, State, ZIP", height=80)
            delivery_date = st.date_input("Expected Delivery")
        
        st.divider()
        st.markdown("**📦 Cargo Details**")
        
        cargo_col1, cargo_col2, cargo_col3 = st.columns(3)
        with cargo_col1:
            commodity = st.text_input("Commodity Description", placeholder="Auto Parts")
            pieces = st.number_input("Pieces/Units", min_value=0, value=1)
        with cargo_col2:
            weight = st.number_input("Weight (lbs)", min_value=0, value=0)
            vehicle_info = st.text_input("Vehicle (Y/M/M/VIN)", placeholder="2024 Honda Accord VIN...")
        with cargo_col3:
            hazmat = st.checkbox("⚠️ HazMat")
            special_instructions = st.text_area("Special Instructions", placeholder="Handle with care...", height=80)
        
        submitted = st.form_submit_button("💾 Save BOL Data")
        
        if submitted:
            bol_data = {
                "shipper": {"name": shipper_name, "address": shipper_address},
                "consignee": {"name": consignee_name, "address": consignee_address},
                "dates": {"pickup": str(pickup_date), "delivery": str(delivery_date)},
                "cargo": {"commodity": commodity, "pieces": pieces, "weight": weight, "vehicle": vehicle_info, "hazmat": hazmat, "instructions": special_instructions},
                "created": datetime.now().isoformat()
            }
            st.session_state['bol_data'] = bol_data
            st.success("✅ BOL Data Saved!")
            st.json(bol_data)

with tab3:
    st.subheader("📄 Generate Custom BOL")
    st.caption("Create a professional Bill of Lading when shipper doesn't provide one")
    
    if 'bol_data' in st.session_state and st.session_state['bol_data']:
        bol = st.session_state['bol_data']
        
        # Preview BOL
        st.markdown("### 📋 BOL Preview")
        
        bol_html = f"""
        <div style="background: white; color: black; padding: 20px; border-radius: 8px; font-family: Arial;">
            <h2 style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px;">BILL OF LADING</h2>
            <p><strong>Date:</strong> {bol['dates']['pickup']}</p>
            
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1; border: 1px solid #ccc; padding: 10px;">
                    <h4>SHIPPER</h4>
                    <p>{bol['shipper']['name']}</p>
                    <p>{bol['shipper']['address']}</p>
                </div>
                <div style="flex: 1; border: 1px solid #ccc; padding: 10px;">
                    <h4>CONSIGNEE</h4>
                    <p>{bol['consignee']['name']}</p>
                    <p>{bol['consignee']['address']}</p>
                </div>
            </div>
            
            <h4 style="margin-top: 15px;">CARGO</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #f0f0f0;">
                    <th style="border: 1px solid #ccc; padding: 5px;">Description</th>
                    <th style="border: 1px solid #ccc; padding: 5px;">Pieces</th>
                    <th style="border: 1px solid #ccc; padding: 5px;">Weight</th>
                    <th style="border: 1px solid #ccc; padding: 5px;">Vehicle/VIN</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #ccc; padding: 5px;">{bol['cargo']['commodity']}</td>
                    <td style="border: 1px solid #ccc; padding: 5px;">{bol['cargo']['pieces']}</td>
                    <td style="border: 1px solid #ccc; padding: 5px;">{bol['cargo']['weight']} lbs</td>
                    <td style="border: 1px solid #ccc; padding: 5px;">{bol['cargo']['vehicle']}</td>
                </tr>
            </table>
            
            <p style="margin-top: 10px;"><strong>Special Instructions:</strong> {bol['cargo']['instructions']}</p>
            {'<p style="color: red;">⚠️ HAZMAT CARGO</p>' if bol['cargo']['hazmat'] else ''}
            
            <div style="margin-top: 30px; display: flex; gap: 20px;">
                <div style="flex: 1; border-top: 1px solid black; padding-top: 5px;">
                    <p>Shipper Signature / Date</p>
                </div>
                <div style="flex: 1; border-top: 1px solid black; padding-top: 5px;">
                    <p>Driver Signature / Date</p>
                </div>
            </div>
        </div>
        """
        
        st.markdown(bol_html, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download as PDF"):
                st.info("PDF generation coming soon! For now, take a screenshot or print.")
        with col2:
            if st.button("📧 Email BOL"):
                st.info("Email integration coming soon!")
    else:
        st.warning("⚠️ Please fill out BOL Data in the 'BOL Data Entry' tab first.")
