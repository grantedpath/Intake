import streamlit as st
from pathlib import Path
from llm_helper import ask_ollama

st.set_page_config(page_title="Health Universe Intake Tool", layout="wide")
st.title("🧠 Health Universe App Intake Form")

css_file = Path("style.css")
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "form_data" not in st.session_state:
    st.session_state.form_data = {}


with st.sidebar:
    #st.image("logo.png", use_column_width=True)  # Optional: remove if no logo file
    st.markdown("## 🧭 Health Universe Intake")
    st.markdown("Use this form to define a new app for deployment within the Health Universe platform.")
    st.markdown("---")

    st.header("📄 Reference Document")
    uploaded_file = st.file_uploader("Upload .md file", type=["md"])
    if uploaded_file:
        st.session_state["ref_doc"] = uploaded_file.read().decode("utf-8")
    else:
        st.session_state["ref_doc"] = ""

    st.markdown("---")
    st.header("✅ Form Progress")
    completed_sections = sum(bool(v) for v in st.session_state.form_data.values())
    st.write(f"Sections Completed: {completed_sections} / 12")
def render_text_area(section, label, key, placeholder=""):
    value = st.text_area(label, placeholder=placeholder, key=f"{section}_{key}")
    st.session_state.form_data[section][key] = value

def render_radio(section, label, key, options):
    value = st.radio(label, options, key=f"{section}_{key}")
    st.session_state.form_data[section][key] = value

def render_checkbox(section, label, key):
    value = st.checkbox(label, key=f"{section}_{key}")
    st.session_state.form_data[section][key] = value

def render_multiselect(section, label, key, options):
    value = st.multiselect(label, options, key=f"{section}_{key}")
    st.session_state.form_data[section][key] = value

# Section 1: General Context (Detailed)
with st.expander("📌 Section 1: General Context"):
    section = "Section 1"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "App Name", "app_name", "e.g., Framingham Risk Calculator")
        render_text_area(section, "Purpose & Clinical Value", "purpose", "e.g., Estimates cardiovascular risk...")
        render_radio(section, "Who is this app for?", "user_type", ["Clinician", "Researcher", "Patient", "Admin", "Other"])
        render_text_area(section, "User Description / Behavior", "explain_user", "What will the user do? What do they expect?")
        render_radio(section, "Where is it used?", "usage_context", ["Point-of-care", "In clinic", "Patient home", "Research lab", "Other"])
        render_text_area(section, "Related Guidelines or Evidence", "guidelines", "Cite supporting references or literature.")
        if st.button("💡 Ask Assistant (Section 1)"):
            st.session_state["llm_section"] = section
    with right:
        if st.session_state.get("llm_section") == section:
            st.markdown("### 💬 Assistant")
            user_question = st.text_area("Ask your question here", key="q_1")
            if st.button("Get Answer", key="a_1"):
                context = st.session_state.get("ref_doc", "")
                prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
                reply = ask_ollama(prompt)
                st.session_state["llm_response_1"] = reply
            if "llm_response_1" in st.session_state:
                st.write(st.session_state["llm_response_1"])
                if st.button("Insert into Section", key="i_1"):
                    current = st.session_state.form_data[section].get("llm_note", "")
                    st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_1"]
                    st.success("✅ Inserted response into notes.")
            if st.button("Close Assistant", key="c_1"):
                st.session_state["llm_section"] = None


# Section 2: Core Logic & Computation
with st.expander("🧠 Section 2: Core Logic & Computation"):
    section = "Section 2"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_multiselect(section, "What powers the app?", "method_type",
            ["Clinical Guideline", "Rule-based Logic", "Statistical Model", "ML Model", "LLM", "RAG"])
        render_text_area(section, "Model or Rule Description", "model_logic", "Describe logic or model (e.g., logistic regression, scoring system)")
        render_text_area(section, "Model Inputs & Preprocessing", "model_inputs", "E.g., 'LDL in mg/dL, smokers: Yes/No, missing values trigger warning'")
    with right:
        if st.button("💡 Ask Assistant (Section 2)"):
            st.session_state["llm_section"] = section
        if st.session_state.get("llm_section") == section:
            st.markdown("### 💬 Assistant")
            user_question = st.text_area("Ask your question here", key="q_2")
            if st.button("Get Answer", key="a_2"):
                context = st.session_state.get("ref_doc", "")
                prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
                reply = ask_ollama(prompt)
                st.session_state["llm_response_2"] = reply
            if "llm_response_2" in st.session_state:
                st.write(st.session_state["llm_response_2"])
                if st.button("Insert into Section", key="i_2"):
                    current = st.session_state.form_data[section].get("llm_note", "")
                    st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_2"]
                    st.success("✅ Inserted response into notes.")
            if st.button("Close Assistant", key="c_2"):
                st.session_state["llm_section"] = None


# Section 3: Inputs & Data Entry
with st.expander("📥 Section 3: Inputs & Data Entry"):
    section = "Section 3"
    st.session_state.form_data.setdefault(section, {})
    render_text_area(section, "Structured Input Table", "input_table", "Specify: name, type, range, required, description...")
    render_multiselect(section, "Accepted File Upload Types", "file_types", ["CSV", "JSON", "PDF", "Image"])
    render_text_area(section, "File Schema or Format", "file_schema", "Define expected columns, data shape, or upload validation.")
    render_checkbox(section, "Include Sample File?", "include_sample_file")
    if st.button("💡 Ask Assistant (Section 3)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_3")
        if st.button("Get Answer", key="a_3"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_3"] = reply
        if "llm_response_3" in st.session_state:
            st.write(st.session_state["llm_response_3"])
            if st.button("Insert into Section", key="i_3"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_3"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_3"):
            st.session_state["llm_section"] = None
    

# Section 4: Outputs
with st.expander("📤 Section 4: Outputs"):
    section = "Section 4"
    st.session_state.form_data.setdefault(section, {})
    render_multiselect(section, "What does the app output?", "output_types", ["Score", "Recommendation", "Chart", "Table", "Overlay Image", "Downloadable File"])
    render_text_area(section, "Interpretation Rules or Output Description", "output_notes", "Describe output logic, interpretation, download behavior.")
    if st.button("💡 Ask Assistant (Section 4)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_4")
        if st.button("Get Answer", key="a_4"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_4"] = reply
        if "llm_response_4" in st.session_state:
            st.write(st.session_state["llm_response_4"])
            if st.button("Insert into Section", key="i_4"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_4"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_4"):
            st.session_state["llm_section"] = None
    

# Section 5: Imaging & Overlays
with st.expander("🖼 Section 5: Imaging & Overlays"):
    section = "Section 5"
    st.session_state.form_data.setdefault(section, {})
    render_multiselect(section, "Input Image Formats", "image_formats", ["JPG", "PNG", "DICOM"])
    render_text_area(section, "Preprocessing Steps", "preprocessing", "e.g., normalize, resize, grayscale")
    render_multiselect(section, "Expected Image Output", "image_outputs", ["Bounding boxes", "Heatmaps", "Labeled annotations"])
    if st.button("💡 Ask Assistant (Section 5)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_5")
        if st.button("Get Answer", key="a_5"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_5"] = reply
        if "llm_response_5" in st.session_state:
            st.write(st.session_state["llm_response_5"])
            if st.button("Insert into Section", key="i_5"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_5"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_5"):
            st.session_state["llm_section"] = None
    

# Section 6: Storage & History
with st.expander("💾 Section 6: Storage & History"):
    section = "Section 6"
    st.session_state.form_data.setdefault(section, {})
    render_radio(section, "Data Persistence?", "storage_type", ["Stateless", "Session-based", "Persistent"])
    render_text_area(section, "Download / Retention Logic", "storage_notes", "Who can download or revisit sessions? Retention policy?")
    if st.button("💡 Ask Assistant (Section 6)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_6")
        if st.button("Get Answer", key="a_6"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_6"] = reply
        if "llm_response_6" in st.session_state:
            st.write(st.session_state["llm_response_6"])
            if st.button("Insert into Section", key="i_6"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_6"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_6"):
            st.session_state["llm_section"] = None
    

# Section 7: Document Processing or RAG
with st.expander("📊 Section 7: Document Processing or RAG"):
    section = "Section 7"
    st.session_state.form_data.setdefault(section, {})
    render_multiselect(section, "Upload Format", "doc_formats", ["PDF", "DOCX", "JSON"])
    render_checkbox(section, "Embed at Runtime?", "embed_runtime")
    render_text_area(section, "Embedding Model", "embedding_model", "e.g., openai/text-embedding-ada")
    render_multiselect(section, "Vector DB", "vector_db", ["FAISS", "Chroma", "Weaviate", "Pinecone"])
    render_text_area(section, "LLM Behavior", "rag_role", "What does the LLM do? Summarizer, Q&A, etc.")
    if st.button("💡 Ask Assistant (Section 7)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_7")
        if st.button("Get Answer", key="a_7"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_7"] = reply
        if "llm_response_7" in st.session_state:
            st.write(st.session_state["llm_response_7"])
            if st.button("Insert into Section", key="i_7"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_7"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_7"):
            st.session_state["llm_section"] = None
    

# Section 8: Protocol & Integration Context
with st.expander("🤖 Section 8: Protocol & Integration Context"):
    section = "Section 8"
    st.session_state.form_data.setdefault(section, {})
    render_radio(section, "Modality", "modality", ["Streamlit", "FastAPI", "MCP", "A2A"])
    render_multiselect(section, "If MCP, what fields are needed?", "mcp_fields", ["Age", "Labs", "Problems", "Encounter Info"])
    render_multiselect(section, "If A2A, what is this agent's role?", "a2a_roles", ["Retriever", "Scorer", "Summarizer", "Planner", "Other"])
    if st.button("💡 Ask Assistant (Section 8)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_8")
        if st.button("Get Answer", key="a_8"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_8"] = reply
        if "llm_response_8" in st.session_state:
            st.write(st.session_state["llm_response_8"])
            if st.button("Insert into Section", key="i_8"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_8"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_8"):
            st.session_state["llm_section"] = None
    

# Section 9: External APIs & Secrets
with st.expander("🔐 Section 9: External APIs & Secrets"):
    section = "Section 9"
    st.session_state.form_data.setdefault(section, {})
    render_text_area(section, "External APIs", "external_apis", "List APIs called, authentication details")
    render_text_area(section, "Secrets or API Keys", "secrets", "e.g., OPENAI_API_KEY")
    render_text_area(section, "Timeout / Retry Logic", "timeouts", "Specify fallback or retry logic")
    if st.button("💡 Ask Assistant (Section 9)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_9")
        if st.button("Get Answer", key="a_9"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_9"] = reply
        if "llm_response_9" in st.session_state:
            st.write(st.session_state["llm_response_9"])
            if st.button("Insert into Section", key="i_9"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_9"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_9"):
            st.session_state["llm_section"] = None
    

# Section 10: UI/UX & Branding
with st.expander("🎨 Section 10: UI/UX & Branding"):
    section = "Section 10"
    st.session_state.form_data.setdefault(section, {})
    render_checkbox(section, "Upload Logo?", "logo_upload")
    render_checkbox(section, "Sidebar Navigation?", "use_sidebar")
    render_checkbox(section, "Expandable Sections?", "use_expanders")
    render_checkbox(section, "Custom Theme?", "custom_css")
    render_text_area(section, "Describe Visual Journey", "visual_story", "What should user see first?")
    if st.button("💡 Ask Assistant (Section 10)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_10")
        if st.button("Get Answer", key="a_10"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_10"] = reply
        if "llm_response_10" in st.session_state:
            st.write(st.session_state["llm_response_10"])
            if st.button("Insert into Section", key="i_10"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_10"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_10"):
            st.session_state["llm_section"] = None
    

# Section 11: README Metadata
with st.expander("📄 Section 11: README Metadata"):
    section = "Section 11"
    st.session_state.form_data.setdefault(section, {})
    render_text_area(section, "Use Case", "use_case", "When and why should this be used?")
    render_text_area(section, "Limitations", "limitations", "What can it not do?")
    render_text_area(section, "Evidence / Citations", "evidence", "PMIDs, guidelines, authors")
    render_text_area(section, "Owner Insight", "insight", "Why did you build this?")
    if st.button("💡 Ask Assistant (Section 11)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_11")
        if st.button("Get Answer", key="a_11"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_11"] = reply
        if "llm_response_11" in st.session_state:
            st.write(st.session_state["llm_response_11"])
            if st.button("Insert into Section", key="i_11"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_11"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_11"):
            st.session_state["llm_section"] = None
    

# Section 12: Privacy & Compliance
with st.expander("🛡 Section 12: Privacy & Compliance"):
    section = "Section 12"
    st.session_state.form_data.setdefault(section, {})
    render_checkbox(section, "Handles PHI/PII?", "handles_phi")
    render_checkbox(section, "De-identification Required?", "deid_needed")
    render_multiselect(section, "Regulations", "regulations", ["HIPAA", "GDPR", "Other"])
    render_text_area(section, "Privacy Handling", "privacy_controls", "How is data protected, logged, or restricted?")

    if st.button("💡 Ask Assistant (Section 12)"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key="q_12")
        if st.button("Get Answer", key="a_12"):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state["llm_response_12"] = reply
        if "llm_response_12" in st.session_state:
            st.write(st.session_state["llm_response_12"])
            if st.button("Insert into Section", key="i_12"):
                current = st.session_state.form_data[section].get("llm_note", "")
                st.session_state.form_data[section]["llm_note"] = current + "\n" + st.session_state["llm_response_12"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key="c_12"):
            st.session_state["llm_section"] = None
    

# === Final Submission ===
st.markdown("---")
st.subheader("📝 Review & Export")
if st.button("📤 Submit Form and Generate Markdown"):
    markdown_output = "# 🧾 Completed Intake Form\n"
    for section, fields in st.session_state.form_data.items():
        markdown_output += f"\n## {section}\n"
        for field, value in fields.items():
            markdown_output += f"**{field.replace('_', ' ').title()}:**\n{value}\n\n"
    st.download_button("📄 Download Markdown", data=markdown_output, file_name="intake_form.md")
    st.markdown("### Preview:")
    st.markdown(markdown_output)