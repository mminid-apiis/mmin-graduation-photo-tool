import streamlit as st

student_page = st.Page("views/student_upload.py", title="Unggah Foto Wisuda", icon="🎓")
admin_page = st.Page("views/admin_dashboard.py", title="Admin", icon="🗂️")

pg = st.navigation([student_page, admin_page], position="top")
pg.run()
