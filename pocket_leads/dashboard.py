import streamlit as st
import sys
import os

# Ensure local imports work
DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from lead_manager import (
    score_by_identifier, get_score_history, format_score_result, load_data,
    analyze_risk_with_gemini
)

def main():
    try:
        st.set_page_config(
            page_title="🎯 Lead Qualifier",
            page_icon="🎯",
            layout="wide"
        )
    except:
        pass

    st.title("🎯 Lead Qualifier")
    st.caption("Score carriers and companies by authority age, safety rating, and risk factors")
    
    # ... Copying Logic from original file ...
    
    # Create tabs
    tab1, tab2 = st.tabs(["🎯 Single Score", "📊 Batch Processing"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Score a Lead")
            
            # Search type selector
            search_type = st.radio("Search By:", ["MC/DOT Number", "Company Name"], horizontal=True)
            
            if search_type == "MC/DOT Number":
                identifier = st.text_input("Enter MC or DOT Number", placeholder="MC123456 or 1234567")
                search_by_name = False
            else:
                identifier = st.text_input("Enter Company Name", placeholder="ABC Trucking LLC")
                search_by_name = True
            
            if st.button("🔍 Score Lead", use_container_width=True):
                if identifier:
                    with st.spinner("Fetching..."):
                        result = score_by_identifier(identifier, search_by_name=search_by_name)
                    
            identifier = st.text_input("Enter MC Number, DOT Number, or Company Name", placeholder="e.g. MC-123456 or 123456")
        
        if st.button("Analyze Risk", type="primary"):
            if identifier:
                with st.spinner(f"Scouring FMCSA databases for {identifier}..."):
                    result = score_by_identifier(identifier)
                
                if "error" in result:
                    st.error(result['error'])
                else:
                    st.success("Analysis Complete")
                    
                    # Display Result
                    r1, r2 = st.columns([2, 1])
                    with r1:
                        st.markdown(format_score_result(result))
                    
                    with r2:
                        st.metric("Risk Score", f"{result['score']}/100", delta=None)
                        st.markdown(f"**Verdict:** {result['risk_level']}")
                        
                        # AI Deep Dive
                        with st.expander("🤖 Gemini Intelligence"):
                            if st.button("Generate AI Risk Report"):
                                with st.spinner("Gemini is analyzing safety patterns..."):
                                    ai_report = analyze_risk_with_gemini(result.get('carrier_data', {}))
                                    st.markdown(ai_report)

        st.divider()
        st.subheader("Recent History")
        history = get_score_history()
        if history:
            import pandas as pd
            hist_data = []
            for h in reversed(history):
                res = h['result']
                carrier = res.get('carrier_data', {})
                hist_data.append({
                    "ID": h['identifier'],
                    "Company": carrier.get('legal_name', 'Unknown'),
                    "Score": res.get('score'),
                    "Risk": res.get('risk_level')
                })
            st.dataframe(pd.DataFrame(hist_data), use_container_width=True)

    with tab2:
        st.subheader("Batch Score Leads")
        st.markdown("Upload a CSV file with a column named `MC` or `DOT` to score multiple carriers at once.")
        
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file:
            import pandas as pd
            try:
                df = pd.read_csv(uploaded_file)
                
                # Find the column with identifiers
                id_col = None
                for col in df.columns:
                    if col.upper() in ['MC', 'DOT', 'MC_NUMBER', 'DOT_NUMBER', 'IDENTIFIER']:
                        id_col = col
                        break
                
                if not id_col:
                    st.error("Could not find MC or DOT column. Please ensure your CSV has a column named 'MC' or 'DOT'.")
                else:
                    st.info(f"Found identifier column: **{id_col}**")
                    
                    if st.button("🚀 Start Batch Processing", use_container_width=True):
                        results = []
                        total = len(df)
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, row in df.iterrows():
                            identifier = str(row[id_col])
                            status_text.text(f"Processing {i+1}/{total}: {identifier}")
                            
                            result = score_by_identifier(identifier)
                            
                            if "error" not in result:
                                carrier = result.get('carrier_data', {})
                                results.append({
                                    "Identifier": identifier,
                                    "Company": carrier.get('legal_name', 'Unknown'),
                                    "Score": result.get('score'),
                                    "Risk Level": result.get('risk_level')
                                })
                            else:
                                results.append({
                                    "Identifier": identifier,
                                    "Company": "Error",
                                    "Score": 0,
                                    "Risk Level": result.get('error', 'Unknown Error')
                                })
                            
                            progress_bar.progress((i + 1) / total)
                        
                        result_df = pd.DataFrame(results)
                        st.success("Processing Complete!")
                        st.dataframe(result_df)
                        
                        # Download button
                        csv = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "📥 Download Results CSV",
                            csv,
                            "scored_leads.csv",
                            "text/csv",
                            key='download-csv'
                        )
            except Exception as e:
                st.error(f"Error processing CSV: {e}")

if __name__ == "__main__":
    main()
