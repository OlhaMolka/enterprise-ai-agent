import streamlit as st
import subprocess

from utils.chat import ask_question
from utils.dashboard import create_department_chart

# PAGE CONFIG

st.set_page_config(
    layout="wide",
    page_title="Enterprise AI Agent"
)

# CUSTOM CSS

st.markdown("""
<style>

/* MAIN APP */

.stApp {
    background-color: #f8fafc;
    color: #0f172a;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}

/* SIDEBAR TEXT */

section[data-testid="stSidebar"] * {
    color: #0f172a !important;
}

/* MAIN TITLES */

h1, h2, h3 {
    color: #0f172a !important;
}

/* METRIC CARDS */

[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e2e8f0;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* INPUT */

.stTextInput input {
    background-color: white;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
}

/* BUTTON */

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
}

/* SELECTBOX */

.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

/* INFO BOX */

.stAlert {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR

st.sidebar.title("Departments")

department = st.sidebar.selectbox(
    "Select Department",
    [
        "All",
        "Risk",
        "Compliance",
        "IT"
    ]
)

st.sidebar.markdown("---")

# DOCUMENT UPLOAD

uploaded_file = st.sidebar.file_uploader(
    "Upload Policy Document",
    type=["txt", "pdf"]
)

if uploaded_file is not None:

    save_path = f"documents/{uploaded_file.name}"

    with open(save_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    st.sidebar.success(
        f"{uploaded_file.name} uploaded successfully"
    )

# REINDEX BUTTON

if st.sidebar.button("Reindex Documents"):

    subprocess.run(
        ["python3", "utils/ingest.py"]
    )

    st.sidebar.success(
        "Documents reindexed successfully"
    )

st.sidebar.markdown("---")

# METRICS

st.sidebar.metric(
    "Indexed Documents",
    "3"
)

st.sidebar.metric(
    "Departments",
    "3"
)

# MAIN PAGE

st.title("Enterprise AI Document Agent")

st.markdown(
    "AI-powered semantic search across internal policies and procedures"
)

col1, col2 = st.columns([2,1])

# LEFT COLUMN

with col1:

    st.subheader("AI Assistant")

    st.info(
        f"Active Department Filter: {department}"
    )

    question = st.text_input(
        "Ask a question about risks, compliance or IT security"
    )

    if st.button("Analyze"):

        answer = ask_question(
            question,
            department
        )

        st.markdown(answer)

# RIGHT COLUMN

with col2:

    st.subheader("Analytics Dashboard")

    fig = create_department_chart()

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.metric(
        label="Policies Indexed",
        value="24"
    )

    st.metric(
        label="Risk Alerts",
        value="5"
    )

    st.metric(
        label="Compliance Reviews",
        value="12"
    )
