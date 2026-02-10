import streamlit as st
import webbrowser

st.set_page_config(
    page_title="Pocket Academy",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Pocket Academy")
st.success("**Ready to Launch!**")
st.write("The Academy is hosted on a separate secure cloud server.")

# The Link
url = "https://pocket-empire-private.vercel.app"

st.info("Click below to open the curriculum in a new tab.")

if st.button("🚀 Launch Academy", type="primary", use_container_width=True):
    webbrowser.open_new_tab(url)
    st.markdown(f'<meta http-equiv="refresh" content="0;url={url}">', unsafe_allow_html=True)

st.caption("If the button doesn't work, [click here](" + url + ")")
