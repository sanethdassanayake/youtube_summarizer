import streamlit as st
from process import process_video
from config import init_api

def init_session_state():
    """Initialize session state variables"""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "error" not in st.session_state:
        st.session_state.error = ""
    if "vid_link" not in st.session_state:
        st.session_state.vid_link = ""
    if "last_url" not in st.session_state:
        st.session_state.last_url = ""

def main():
    # Initialize API and session state
    try:
        init_api()
    except ValueError as e:
        st.error(str(e))
        return

    init_session_state()
    
    st.title("YouTube Video Summarizer")

    # Layout
    col1, col2 = st.columns([4, 1])
    with col1:
        yt_link = st.text_input("", placeholder="Enter YouTube video link")
        st.session_state.vid_link = yt_link
    
    with col2:
        st.write('<style>div.stButton > button {margin-top: 12px;}</style>', unsafe_allow_html=True)
        if st.button("Summarize", use_container_width=True):
            with st.spinner("Working..."):
                summary, error = process_video(yt_link)
                if error:
                    st.session_state.error = error
                    st.session_state.summary = ""
                else:
                    st.session_state.summary = summary
                    st.session_state.error = ""
                    st.toast("Summary generated successfully!", icon="🚀")

    # Display components
    if st.session_state.error:
        st.error(st.session_state.error)

    if st.session_state.vid_link:
        st.video(st.session_state.vid_link)

    if st.session_state.summary:
        st.subheader("Summary")
        st.write(st.session_state.summary)

    # Update session state
    if yt_link and yt_link != st.session_state.last_url:
        st.session_state.last_url = yt_link

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 10px;">
            Made with ❤️ by Saneth Dassanayake
        </div>
        <div style="text-align: center;">
            <a href="https://github.com/sanethdassanayake" target="_blank">GitHub</a> |
            <a href="https://www.instagram.com/sanethdassanayake/" target="_blank">Instagram</a> |
            <a href="https://x.com/SanethDa" target="_blank">X (Twitter)</a> |
            <a href="https://discord.gg/SEzWsCQrRy" target="_blank">Discord</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()