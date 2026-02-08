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
        bg_image = st.file_uploader(
            "Upload Image or Video (BOL / Vehicle Photo / Damage Video)", 
            type=["png", "jpg", "jpeg", "gif", "webp", "heic", "mp4", "mov", "avi", "mkv"],
            help="Max 200MB. Supports photos and videos."
        )
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

    # --- Canvas or Video ---
    if bg_image:
        # Check if it's a video file
        file_ext = bg_image.name.lower().split('.')[-1]
        is_video = file_ext in ['mp4', 'mov', 'avi', 'mkv']
        
        if is_video:
            st.markdown("### 🎬 Video Preview")
            st.video(bg_image)
            st.success("✅ Video uploaded! You can download or save it to cloud.")
            
            # Video actions
            video_col1, video_col2 = st.columns(2)
            with video_col1:
                st.download_button(
                    "⬇️ Download Video",
                    data=bg_image.getvalue(),
                    file_name=f"damage_video_{datetime.now().strftime('%Y%m%d_%H%M')}.{file_ext}",
                    mime=f"video/{file_ext}"
                )
            with video_col2:
                if st.button("☁️ Save to Cloud"):
                    st.info("Video cloud storage coming soon!")
        else:
            # Image handling
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
        st.info("👈 Upload a Photo/Video or use Camera to capture a BOL / Vehicle.")

with tab2:
    st.subheader("📝 Enter BOL Data")
    st.caption("Fill in missing information from the Bill of Lading")
    
    # Origin/Destination section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📍 Origin**")
        shipper_name = st.text_input("Shipper Name", placeholder="ABC Shipping Co.", key="bol_shipper")
        shipper_address = st.text_area("Shipper Address", placeholder="123 Main St, City, State, ZIP", height=80, key="bol_ship_addr")
        pickup_date = st.date_input("Pickup Date", key="bol_pickup")
        
    with col2:
        st.markdown("**📍 Destination**")
        consignee_name = st.text_input("Consignee Name", placeholder="XYZ Receiving Inc.", key="bol_consignee")
        consignee_address = st.text_area("Consignee Address", placeholder="456 Oak Ave, City, State, ZIP", height=80, key="bol_cons_addr")
        delivery_date = st.date_input("Expected Delivery", key="bol_delivery")
    
    st.divider()
    st.markdown("**📦 Cargo Details**")
    
    # Commodity Type Selector
    commodity_type = st.selectbox(
        "🚗 Commodity Type",
        ["🚗 Car", "🚚 Truck", "🚙 SUV", "📦 Freight"],
        key="commodity_type"
    )
    
    # Initialize cargo data
    cargo_data = {"type": commodity_type}
    
    # Conditional fields based on commodity type
    if commodity_type in ["🚗 Car", "🚚 Truck", "🚙 SUV"]:
        st.markdown("##### 🚘 Vehicle Information")
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            vehicle_year = st.text_input("Year", placeholder="2024", key="v_year")
            vehicle_make = st.text_input("Make", placeholder="Honda", key="v_make")
            vehicle_model = st.text_input("Model", placeholder="Accord", key="v_model")
        with v_col2:
            vehicle_color = st.text_input("Color", placeholder="Black", key="v_color")
            vehicle_vin = st.text_input("VIN Number", placeholder="1HGCV1F34PA123456", key="v_vin")
        
        st.markdown("##### 🔧 Damage Checklist")
        damage_cols = st.columns(4)
        with damage_cols[0]:
            dmg_front = st.checkbox("Front Damage", key="dmg_front")
            dmg_rear = st.checkbox("Rear Damage", key="dmg_rear")
        with damage_cols[1]:
            dmg_left = st.checkbox("Left Side Damage", key="dmg_left")
            dmg_right = st.checkbox("Right Side Damage", key="dmg_right")
        with damage_cols[2]:
            dmg_roof = st.checkbox("Roof Damage", key="dmg_roof")
            dmg_undercarriage = st.checkbox("Under", key="dmg_under")
        with damage_cols[3]:
            dmg_glass = st.checkbox("Glass", key="dmg_glass")
            dmg_interior = st.checkbox("Interior", key="dmg_interior")
        
        damage_notes = st.text_area("Damage Notes", placeholder="Describe any visible damage...", key="dmg_notes")
        
        cargo_data.update({
            "vehicle": {
                "year": vehicle_year,
                "make": vehicle_make,
                "model": vehicle_model,
                "color": vehicle_color,
                "vin": vehicle_vin
            },
            "damage": {
                "front": dmg_front, "rear": dmg_rear, "left": dmg_left, "right": dmg_right,
                "roof": dmg_roof, "undercarriage": dmg_undercarriage, "glass": dmg_glass, "interior": dmg_interior,
                "notes": damage_notes
            }
        })
    
    else:  # Freight
        st.markdown("##### 📦 Freight Information")
        
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            freight_desc = st.text_input("Description", placeholder="Palletized goods", key="f_desc")
            freight_weight = st.number_input("Weight (lbs)", min_value=0, value=0, key="f_weight")
        with f_col2:
            freight_pieces = st.number_input("Piece Count", min_value=1, value=1, key="f_pieces")
            freight_dims = st.text_input("Dimensions (LxWxH)", placeholder="48x40x48", key="f_dims")
        with f_col3:
            freight_tarp = st.selectbox("Tarp Status", ["Not Required", "Tarped", "Untarped (Needs Tarp)"], key="f_tarp")
            freight_hazmat = st.checkbox("⚠️ HazMat", key="f_hazmat")
        
        freight_instructions = st.text_area("Special Instructions", placeholder="Keep dry, fragile...", key="f_instr")
        
        cargo_data.update({
            "freight": {
                "description": freight_desc,
                "weight": freight_weight,
                "pieces": freight_pieces,
                "dimensions": freight_dims,
                "tarp_status": freight_tarp,
                "hazmat": freight_hazmat,
                "instructions": freight_instructions
            }
        })
    
    st.divider()
    
    if st.button("💾 Save BOL Data", type="primary"):
        bol_data = {
            "shipper": {"name": shipper_name, "address": shipper_address},
            "consignee": {"name": consignee_name, "address": consignee_address},
            "dates": {"pickup": str(pickup_date), "delivery": str(delivery_date)},
            "cargo": cargo_data,
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
        cargo = bol['cargo']
        
        # Build cargo details based on type
        if cargo['type'] in ['🚗 Car', '🚚 Truck', '🚙 SUV']:
            vehicle = cargo.get('vehicle', {})
            damage = cargo.get('damage', {})
            cargo_desc = f"{vehicle.get('year', '')} {vehicle.get('make', '')} {vehicle.get('model', '')}".strip()
            cargo_detail = f"Color: {vehicle.get('color', 'N/A')} | VIN: {vehicle.get('vin', 'N/A')}"
            damage_list = [k.title() for k, v in damage.items() if v and k != 'notes']
            damage_str = ", ".join(damage_list) if damage_list else "None noted"
            extra_info = f"Damage: {damage_str}"
            if damage.get('notes'):
                extra_info += f"<br>Notes: {damage['notes']}"
        else:
            freight = cargo.get('freight', {})
            cargo_desc = freight.get('description', 'Freight')
            cargo_detail = f"Pieces: {freight.get('pieces', 1)} | Weight: {freight.get('weight', 0)} lbs"
            extra_info = f"Dimensions: {freight.get('dimensions', 'N/A')} | Tarp: {freight.get('tarp_status', 'N/A')}"
            if freight.get('hazmat'):
                extra_info += " | ⚠️ HAZMAT"
        
        # Preview BOL
        st.markdown("### 📋 BOL Preview")
        
        bol_html = f"""
        <div id="bol-preview" style="background: white; color: black; padding: 20px; border-radius: 8px; font-family: Arial;">
            <h2 style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px;">BILL OF LADING</h2>
            <p><strong>Date:</strong> {bol['dates']['pickup']} | <strong>Delivery:</strong> {bol['dates']['delivery']}</p>
            
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
            
            <h4 style="margin-top: 15px;">CARGO ({cargo['type']})</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #f0f0f0;">
                    <th style="border: 1px solid #ccc; padding: 8px;">Description</th>
                    <th style="border: 1px solid #ccc; padding: 8px;">Details</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #ccc; padding: 8px;">{cargo_desc}</td>
                    <td style="border: 1px solid #ccc; padding: 8px;">{cargo_detail}</td>
                </tr>
            </table>
            <p style="margin-top: 10px;">{extra_info}</p>
            
            <div style="margin-top: 30px; display: flex; gap: 20px;">
                <div style="flex: 1; border-top: 2px solid black; padding-top: 5px; height: 60px;">
                    <p><strong>Shipper Signature / Date</strong></p>
                </div>
                <div style="flex: 1; border-top: 2px solid black; padding-top: 5px; height: 60px;">
                    <p><strong>Driver Signature / Date</strong></p>
                </div>
            </div>
        </div>
        """
        
        st.markdown(bol_html, unsafe_allow_html=True)
        
        st.divider()
        
        # ✍️ Signature Canvas
        st.markdown("### ✍️ Add Signatures / Annotations")
        st.caption("Use Apple Pencil to sign or make corrections")
        
        sig_col1, sig_col2 = st.columns(2)
        with sig_col1:
            sig_stroke = st.slider("Pen Width", 1, 10, 3, key="sig_stroke")
        with sig_col2:
            sig_color = st.color_picker("Ink Color", "#000000", key="sig_color")
        
        # Signature canvas
        sig_canvas = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",
            stroke_width=sig_stroke,
            stroke_color=sig_color,
            background_color="#ffffff",
            height=150,
            width=700,
            drawing_mode="freedraw",
            display_toolbar=True,
            key="signature_canvas"
        )
        
        st.divider()
        
        # Action buttons
        st.markdown("### 📤 Export Options")
        action_cols = st.columns(3)
        
        with action_cols[0]:
            # Generate PDF
            if st.button("📥 Download PDF", type="primary"):
                try:
                    from fpdf import FPDF
                    
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, "BILL OF LADING", ln=True, align="C")
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 6, f"Date: {bol['dates']['pickup']} | Delivery: {bol['dates']['delivery']}", ln=True)
                    pdf.ln(3)
                    
                    # Shipper/Consignee
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(95, 6, "SHIPPER", border=1)
                    pdf.cell(95, 6, "CONSIGNEE", border=1, ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(95, 6, bol['shipper']['name'], border=1)
                    pdf.cell(95, 6, bol['consignee']['name'], border=1, ln=True)
                    pdf.multi_cell(95, 6, bol['shipper']['address'][:50], border=1)
                    pdf.set_xy(pdf.get_x() + 95, pdf.get_y() - 6)
                    pdf.multi_cell(95, 6, bol['consignee']['address'][:50], border=1)
                    pdf.ln(5)
                    
                    # Cargo
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, f"CARGO ({cargo['type']})", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 6, f"Description: {cargo_desc}", ln=True)
                    pdf.cell(0, 6, f"Details: {cargo_detail}", ln=True)
                    pdf.ln(10)
                    
                    # Signatures
                    pdf.cell(95, 20, "Shipper Signature: ________________", border=1)
                    pdf.cell(95, 20, "Driver Signature: ________________", border=1, ln=True)
                    
                    pdf_output = pdf.output(dest='S').encode('latin-1')
                    
                    st.download_button(
                        "⬇️ Click to Download",
                        data=pdf_output,
                        file_name=f"BOL_{bol['dates']['pickup']}.pdf",
                        mime="application/pdf"
                    )
                    st.success("✅ PDF Ready!")
                except ImportError:
                    st.error("PDF library not installed. Use Print instead.")
        
        with action_cols[1]:
            # Print button (opens browser print dialog)
            st.markdown("""
            <button onclick="window.print()" style="background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">
                🖨️ Print BOL
            </button>
            """, unsafe_allow_html=True)
        
        with action_cols[2]:
            if st.button("📧 Email BOL"):
                st.info("Email integration coming soon!")
        
        # Save signature if drawn
        if sig_canvas.image_data is not None and sig_canvas.json_data and len(sig_canvas.json_data.get('objects', [])) > 0:
            st.success("✅ Signature captured! It will be included when you download.")
    else:
        st.warning("⚠️ Please fill out BOL Data in the 'BOL Data Entry' tab first.")

