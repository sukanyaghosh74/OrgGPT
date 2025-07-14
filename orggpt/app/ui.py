import streamlit as st
from pathlib import Path
from orggpt.app.loader import load_and_chunk
from orggpt.app.vectorstore import VectorStore
from orggpt.app.chain import MemoRAGChain
from loguru import logger
import uuid

st.set_page_config(page_title="OrgGPT Investment Memo", layout="wide")
st.title("OrgGPT: AI Investment Memo Generator")

if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = VectorStore()
if "chain" not in st.session_state:
    st.session_state["chain"] = MemoRAGChain(st.session_state["vectorstore"])

st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload 10-K, earnings call, or investor letter (PDF/TXT)", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Processing document..."):
        try:
            file_id = str(uuid.uuid4())
            file_path = Path(f"/tmp/{file_id}_{uploaded_file.name}")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            chunks = load_and_chunk(file_path)
            st.session_state["vectorstore"].add_chunks(chunks, doc_id=file_id)
            st.success(f"Uploaded and indexed {uploaded_file.name}.")
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            st.error(f"Failed to process file: {e}")

st.sidebar.header("Query")
default_query = "Generate an investment memo for this company."
user_query = st.sidebar.text_area("Your query", value=default_query, height=80)

if st.sidebar.button("Generate Memo"):
    with st.spinner("Generating investment memo..."):
        try:
            memo = st.session_state["chain"].generate_memo(user_query)
            st.header("Investment Memo")
            for section, content in memo.items():
                st.subheader(section)
                st.markdown(content)
        except Exception as e:
            logger.error(f"Error generating memo: {e}")
            st.error(f"Failed to generate memo: {e}") 