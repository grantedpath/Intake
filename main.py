import streamlit as st
from pathlib import Path
from llm_helper import ask_ollama

st.set_page_config(page_title="Health Universe Intake Tool", layout="wide")
st.title("🧠 Health Universe App Intake Form")

# Style
css_file = Path("style.css")
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Sidebar
with st.sidebar:
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

# Reusable render functions
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

def render_llm_assistant(section, qkey, akey, ikey, insert_field):
    if st.button("💡 Ask Assistant", key=f"ask_{section}"):
        st.session_state["llm_section"] = section
    if st.session_state.get("llm_section") == section:
        st.markdown("### 💬 Assistant")
        user_question = st.text_area("Ask your question here", key=qkey)
        if st.button("Get Answer", key=akey):
            context = st.session_state.get("ref_doc", "")
            prompt = f"You are helping a user complete the section '{section}' of a healthcare app intake form.\n\nReference:\n{context}\n\nUser question: {user_question}"
            reply = ask_ollama(prompt)
            st.session_state[f"llm_response_{section}"] = reply
        if f"llm_response_{section}" in st.session_state:
            st.write(st.session_state[f"llm_response_{section}"])
            if st.button("Insert into Section", key=ikey):
                current = st.session_state.form_data[section].get(insert_field, "")
                st.session_state.form_data[section][insert_field] = current + "\n" + st.session_state[f"llm_response_{section}"]
                st.success("✅ Inserted response into notes.")
        if st.button("Close Assistant", key=f"close_{section}"):
            st.session_state["llm_section"] = None


def section2():
    with st.expander("🧠 Section 2: Core Logic & Computation"):
        section = "Section 2"
        st.session_state.form_data.setdefault(section, {})
        render_multiselect(section, "What powers the app?", "method_type", ["Clinical Guideline", "Rule-based Logic", "Statistical Model", "ML Model", "LLM", "RAG"])
        render_text_area(section, "Model or Rule Description", "model_logic")
        render_text_area(section, "Model Inputs & Preprocessing", "model_inputs")
        render_llm_assistant(section, "q_2", "a_2", "i_2", "model_logic")

def section3():
    with st.expander("📥 Section 3: Inputs & Data Entry"):
        section = "Section 3"
        st.session_state.form_data.setdefault(section, {})
        render_text_area(section, "Structured Input Table", "input_table")
        render_multiselect(section, "Accepted File Upload Types", "file_types", ["CSV", "JSON", "PDF", "Image"])
        render_text_area(section, "File Schema or Format", "file_schema")
        render_checkbox(section, "Include Sample File?", "include_sample_file")
        render_llm_assistant(section, "q_3", "a_3", "i_3", "input_table")

def section4():
    with st.expander("📤 Section 4: Outputs"):
        section = "Section 4"
        st.session_state.form_data.setdefault(section, {})
        render_multiselect(section, "What does the app output?", "output_types", ["Score", "Recommendation", "Chart", "Table", "Overlay Image", "Downloadable File"])
        render_text_area(section, "Interpretation Rules or Output Description", "output_notes")
        render_llm_assistant(section, "q_4", "a_4", "i_4", "output_notes")

def section5():
    with st.expander("🖼 Section 5: Imaging & Overlays"):
        section = "Section 5"
        st.session_state.form_data.setdefault(section, {})
        render_multiselect(section, "Input Image Formats", "image_formats", ["JPG", "PNG", "DICOM"])
        render_text_area(section, "Preprocessing Steps", "preprocessing")
        render_multiselect(section, "Expected Image Output", "image_outputs", ["Bounding boxes", "Heatmaps", "Labeled annotations"])
        render_llm_assistant(section, "q_5", "a_5", "i_5", "preprocessing")

def section6():
    with st.expander("💾 Section 6: Storage & History"):
        section = "Section 6"
        st.session_state.form_data.setdefault(section, {})
        render_radio(section, "Data Persistence?", "storage_type", ["Stateless", "Session-based", "Persistent"])
        render_text_area(section, "Download / Retention Logic", "storage_notes")
        render_llm_assistant(section, "q_6", "a_6", "i_6", "storage_notes")

def section7():
    with st.expander("📊 Section 7: Document Processing or RAG"):
        section = "Section 7"
        st.session_state.form_data.setdefault(section, {})
        render_multiselect(section, "Upload Format", "doc_formats", ["PDF", "DOCX", "JSON"])
        render_checkbox(section, "Embed at Runtime?", "embed_runtime")
        render_text_area(section, "Embedding Model", "embedding_model")
        render_multiselect(section, "Vector DB", "vector_db", ["FAISS", "Chroma", "Weaviate", "Pinecone"])
        render_text_area(section, "LLM Behavior", "rag_role")
        render_llm_assistant(section, "q_7", "a_7", "i_7", "rag_role")

def section8():
    with st.expander("🤖 Section 8: Protocol & Integration Context"):
        section = "Section 8"
        st.session_state.form_data.setdefault(section, {})
        render_radio(section, "Modality", "modality", ["Streamlit", "FastAPI", "MCP", "A2A"])
        render_multiselect(section, "If MCP, what fields are needed?", "mcp_fields", ["Age", "Labs", "Problems", "Encounter Info"])
        render_multiselect(section, "If A2A, what is this agent's role?", "a2a_roles", ["Retriever", "Scorer", "Summarizer", "Planner", "Other"])
        render_llm_assistant(section, "q_8", "a_8", "i_8", "modality")

def section9():
    with st.expander("🔐 Section 9: External APIs & Secrets"):
        section = "Section 9"
        st.session_state.form_data.setdefault(section, {})
        render_text_area(section, "External APIs", "external_apis")
        render_text_area(section, "Secrets or API Keys", "secrets")
        render_text_area(section, "Timeout / Retry Logic", "timeouts")
        render_llm_assistant(section, "q_9", "a_9", "i_9", "external_apis")

def section10():
    with st.expander("🎨 Section 10: UI/UX & Branding"):
        section = "Section 10"
        st.session_state.form_data.setdefault(section, {})
        render_checkbox(section, "Upload Logo?", "logo_upload")
        render_checkbox(section, "Sidebar Navigation?", "use_sidebar")
        render_checkbox(section, "Expandable Sections?", "use_expanders")
        render_checkbox(section, "Custom Theme?", "custom_css")
        render_text_area(section, "Describe Visual Journey", "visual_story")
        render_llm_assistant(section, "q_10", "a_10", "i_10", "visual_story")

def section11():
    with st.expander("📄 Section 11: README Metadata"):
        section = "Section 11"
        st.session_state.form_data.setdefault(section, {})
        render_text_area(section, "Use Case", "use_case")
        render_text_area(section, "Limitations", "limitations")
        render_text_area(section, "Evidence / Citations", "evidence")
        render_text_area(section, "Owner Insight", "insight")
        render_llm_assistant(section, "q_11", "a_11", "i_11", "use_case")

def section12():
    with st.expander("🛡 Section 12: Privacy & Compliance"):
        section = "Section 12"
        st.session_state.form_data.setdefault(section, {})
        render_checkbox(section, "Handles PHI/PII?", "handles_phi")
        render_checkbox(section, "De-identification Required?", "deid_needed")
        render_multiselect(section, "Regulations", "regulations", ["HIPAA", "GDPR", "Other"])
        render_text_area(section, "Privacy Handling", "privacy_controls")
        render_llm_assistant(section, "q_12", "a_12", "i_12", "privacy_controls")

# Render all 12 sections
section1()
section2()
section3()
section4()
section5()
section6()
section7()
section8()
section9()
section10()
section11()
section12()

# Final export
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
