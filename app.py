import streamlit as st
import docx2txt
import PyPDF2
import tempfile
from backend.cohere_utils import (
    argument_mining, entity_relationship_mapping, clause_explanation, summarization,
    legal_chatbot, strategy_suggestions, risk_prediction, cohere_generate
)

st.set_page_config(page_title="Legal Document Analyzer", layout="wide")
st.title("Legal Document Analyzer")

uploaded_file = st.file_uploader("1. 📂 Upload PDF/DOCX", type=["pdf", "docx"])
extracted_text = ""

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    if ext == "pdf":
        text = ""
        with open(tmp_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        extracted_text = text
    elif ext == "docx":
        extracted_text = docx2txt.process(tmp_path)
    st.success("File uploaded and text extracted!")
    st.text_area("2. 🔍 Text Extraction", value=extracted_text, height=200, key="extracted_text")
else:
    extracted_text = st.text_area("2. 🔍 Text Extraction", value="", height=200, key="extracted_text")

if extracted_text:
    with st.expander("1. 👥 Entity & Relationship Mapping", expanded=False):
        if st.button("Run Entity & Relationship Mapping"):
            st.session_state['entities'] = entity_relationship_mapping(extracted_text)
        st.text_area("Entities & Relationships", value=st.session_state.get('entities', ''), height=100)

    with st.expander("2. 🧠 Argument Mining", expanded=False):
        if st.button("Run Argument Mining"):
            st.session_state['arguments'] = argument_mining(extracted_text)
        st.text_area("Arguments", value=st.session_state.get('arguments', ''), height=100)

    with st.expander("3. 📄 Clause Explanation", expanded=False):
        if st.button("Run Clause Explanation"):
            st.session_state['clause'] = clause_explanation(extracted_text)
        st.text_area("Clause Explanation", value=st.session_state.get('clause', ''), height=100)

    with st.expander("4. 📝 Summarization", expanded=False):
        if st.button("Run Summarization"):
            st.session_state['summary'] = summarization(extracted_text)
        st.text_area("Summary", value=st.session_state.get('summary', ''), height=100)

    with st.expander("5. Future Steps in the Case", expanded=False):
        if st.button("Run Future Steps"):
            prompt = f"Suggest future steps in the following legal case.\n\nCase:\n{extracted_text}\n\nFuture Steps:"
            st.session_state['future_steps'] = cohere_generate(prompt, "future_steps")
        st.text_area("Future Steps", value=st.session_state.get('future_steps', ''), height=100)

    with st.expander("6. ⚖️ Strategy Suggestions", expanded=False):
        if st.button("Run Strategy Suggestions"):
            st.session_state['strategies'] = strategy_suggestions(extracted_text)
        st.text_area("Strategy Suggestions", value=st.session_state.get('strategies', ''), height=100)

    with st.expander("7. 💬 Legal Chatbot", expanded=False):
        question = st.text_input("Ask a legal question:", key="chatbot_question")
        if st.button("Ask Chatbot"):
            st.session_state['chatbot_answer'] = legal_chatbot(question, extracted_text)
        st.text_area("Chatbot Answer", value=st.session_state.get('chatbot_answer', ''), height=100)

    with st.expander("8. 📈 Risk Prediction", expanded=False):
        if st.button("Run Risk Prediction"):
            st.session_state['risk'] = risk_prediction(extracted_text)
        risk_text = st.session_state.get('risk', '')
        st.text_area("Risk Prediction", value=risk_text, height=100)
        # Extract and display risk scores for Plaintiff and Defendant
        import re
        plaintiff_score = None
        defendant_score = None
        # Try to find 'Plaintiff Risk Score: <number>' and 'Defendant Risk Score: <number>'
        plaintiff_match = re.search(r'plaintiff[^\d]*(100|\d{1,2})', risk_text, re.IGNORECASE)
        defendant_match = re.search(r'defendant[^\d]*(100|\d{1,2})', risk_text, re.IGNORECASE)
        if plaintiff_match:
            plaintiff_score = int(plaintiff_match.group(1))
        if defendant_match:
            defendant_score = int(defendant_match.group(1))
        # Clamp scores
        if plaintiff_score is not None:
            plaintiff_score = max(0, min(plaintiff_score, 100))
            st.progress(plaintiff_score/100, text=f"Plaintiff Risk Score: {plaintiff_score}")
        if defendant_score is not None:
            defendant_score = max(0, min(defendant_score, 100))
            st.progress(defendant_score/100, text=f"Defendant Risk Score: {defendant_score}")
        if plaintiff_score is None and defendant_score is None:
            st.info("No valid Plaintiff or Defendant risk scores found in the response.")
else:
    st.info("Upload a file or paste text to begin.")

