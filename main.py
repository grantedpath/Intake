import streamlit as st
from pathlib import Path
from llm_helper import ask_ollama

st.set_page_config(page_title="Health Universe App Intake", layout="wide")
st.title("🧾 Health Universe App Intake Form")

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

with st.sidebar:
    st.header("📄 Load Reference")
    ref_doc = st.file_uploader("Upload reference .md file", type=["md"])
    if ref_doc:
        ref_content = ref_doc.read().decode("utf-8")
        st.session_state["ref_doc"] = ref_content

    st.markdown("---")
    st.header("🧭 Form Progress")
    completed_sections = [k for k, v in st.session_state.form_data.items() if any(v.values())]
    st.text(f"Sections Completed: {len(completed_sections)} / 12")

def show_llm_modal(section_name):
    st.session_state["llm_context"] = section_name
    st.session_state["show_llm_modal"] = True

def render_text_area(section_key, label, key, default=""):
    value = st.text_area(label, value=st.session_state.form_data[section_key].get(key, default))
    st.session_state.form_data[section_key][key] = value

def render_radio(section_key, label, key, options):
    value = st.radio(label, options, index=0 if not st.session_state.form_data[section_key].get(key) else options.index(st.session_state.form_data[section_key][key]))
    st.session_state.form_data[section_key][key] = value

def render_checkbox(section_key, label, key):
    value = st.checkbox(label, value=st.session_state.form_data[section_key].get(key, False))
    st.session_state.form_data[section_key][key] = value

def render_multiselect(section_key, label, key, options):
    value = st.multiselect(label, options, default=st.session_state.form_data[section_key].get(key, []))
    st.session_state.form_data[section_key][key] = value


# Section 1: General Context
with st.expander("📌 Section 1: General Context"):
    section = "Section 1"
    st.session_state.form_data.setdefault(section, {})
    render_text_area(section, "App Name", "app_name", "e.g., Framingham Risk Calculator")
    render_text_area(section, "Purpose & Value", "purpose", "e.g., Estimates 10-year cardiovascular risk using the Framingham equation to guide statin therapy decisions.")
    render_radio(section, "Intended User", "user_type", ["Clinician", "Researcher", "Patient", "Admin", "Other"])
    render_text_area(section, "User Description / Details", "explain_user")
    if st.button("💡 Ask Assistant (Section 1)"):
        show_llm_modal(section)

# Section 2: Core Logic
with st.expander("🧠 Section 2: Core Logic & Computation"):
    section = "Section 2"
    st.session_state.form_data.setdefault(section, {})
    render_multiselect(section, "Underlying Method or Model", "method", ["Clinical Guideline", "Rule-based Logic", "Statistical Model", "ML Model", "LLM", "RAG"])
    render_text_area(section, "Model Logic or Source", "model_logic", "e.g., Logistic regression using systolic BP, age, and smoking status.")
    render_text_area(section, "Input Formatting & Preprocessing", "preprocessing", "e.g., Convert lbs to kg, ensure LDL is in mg/dL, impute missing values.")
    if st.button("💡 Ask Assistant (Section 2)"):
        show_llm_modal(section)

# Section 3: Inputs
with st.expander("📥 Section 3: Inputs & Data Entry"):
    section = "Section 3"
    st.session_state.form_data.setdefault(section, {})
    render_text_area(section, "List User Inputs", "input_list", "e.g., Age (18–89), LDL (mg/dL), Smoker (Yes/No)")
    render_multiselect(section, "Supported Upload Types", "upload_types", ["CSV", "JSON", "PDF", "Image"])
    render_text_area(section, "Expected Schema / Format", "upload_schema", "e.g., CSV with columns: age, smoker, sbp, hdl")
    if st.button("💡 Ask Assistant (Section 3)"):
        show_llm_modal(section)

# Section 4: Outputs
with st.expander("📤 Section 4: Outputs"):
    section = "Section 4"
    st.session_state.form_data.setdefault(section, {})
    render_multiselect(section, "Output Types", "output_types", ["Score", "Recommendation", "Chart", "Table", "Overlay Image", "PDF/CSV/JSON"])
    render_text_area(section, "Output Description", "output_detail", "e.g., Score between 0–1 with interpretation: <0.2 Low, 0.2–0.7 Moderate, >0.7 High risk.")
    if st.button("💡 Ask Assistant (Section 4)"):
        show_llm_modal(section)


# Section 5: Imaging & Overlays
with st.expander("🖼 Section 5: Imaging & Overlays"):
    section = "Section 5"
    st.session_state.form_data.setdefault(section, {})
    render_multiselect(section, "Input Image Formats", "image_formats", ["JPG", "PNG", "DICOM"])
    render_text_area(section, "Preprocessing Steps", "image_preprocessing", "e.g., Resize to 224x224, convert to grayscale, normalize pixel values.")
    render_multiselect(section, "Output Overlays", "output_overlays", ["Bounding Boxes", "Heatmaps", "Labels"])
    render_text_area(section, "Visual Output Experience", "overlay_description", "e.g., Display bounding boxes around detected lesions with confidence scores.")
    if st.button("💡 Ask Assistant (Section 5)"):
        show_llm_modal(section)

# Section 6: Storage & History
with st.expander("💾 Section 6: Storage & History"):
    section = "Section 6"
    st.session_state.form_data.setdefault(section, {})
    render_radio(section, "Storage Mode", "storage_mode", ["Stateless", "Session-based", "Persistent"])
    render_text_area(section, "Storage Logic", "storage_logic", "e.g., Store session results temporarily; allow optional download as CSV.")
    if st.button("💡 Ask Assistant (Section 6)"):
        show_llm_modal(section)

# Section 7: Document Processing or RAG
with st.expander("📊 Section 7: Document Processing or RAG"):
    section = "Section 7"
    st.session_state.form_data.setdefault(section, {})
    render_multiselect(section, "Document Formats", "doc_formats", ["PDF", "DOCX", "JSON"])
    render_radio(section, "Embed Docs at Runtime?", "embed_docs", ["Yes", "No"])
    render_text_area(section, "Embedding Model", "embedding_model", "e.g., all-MiniLM-L6-v2")
    render_multiselect(section, "Vector DB", "vector_db", ["FAISS", "Chroma", "Weaviate", "Pinecone"])
    render_text_area(section, "RAG Logic", "rag_logic", "e.g., Chunk documents by headings; embed on upload; query with top_k=3")
    if st.button("💡 Ask Assistant (Section 7)"):
        show_llm_modal(section)

# Section 8: Protocol & Integration
with st.expander("🤖 Section 8: Protocol & Integration Context"):
    section = "Section 8"
    st.session_state.form_data.setdefault(section, {})
    render_radio(section, "App Type", "app_type", ["Streamlit", "FastAPI", "MCP", "A2A"])
    render_multiselect(section, "MCP Context Fields", "mcp_fields", ["Patient", "Labs", "Problems", "Encounter"])
    render_text_area(section, "A2A Role", "a2a_role", "e.g., Retriever, Planner, Summarizer")
    render_text_area(section, "Agent IO Schema", "agent_io", "e.g., Input: {labs, age}; Output: plan_summary")
    if st.button("💡 Ask Assistant (Section 8)"):
        show_llm_modal(section)


# Section 9: External APIs & Secrets
with st.expander("🔐 Section 9: External APIs & Secrets"):
    section = "Section 9"
    st.session_state.form_data.setdefault(section, {})
    render_text_area(section, "External APIs Used", "apis_used", "e.g., OpenAI for text generation, ClinicalTrials.gov for research data")
    render_text_area(section, "Secrets Required", "secrets", "e.g., OPENAI_API_KEY, DICOM_API_SECRET")
    render_text_area(section, "Authentication & Error Handling", "auth_error", "e.g., Use API key via header, retry up to 3x with exponential backoff")
    if st.button("💡 Ask Assistant (Section 9)"):
        show_llm_modal(section)

# Section 10: UI/UX & Branding
with st.expander("🎨 Section 10: UI/UX & Branding"):
    section = "Section 10"
    st.session_state.form_data.setdefault(section, {})
    render_checkbox(section, "Include Logo?", "logo")
    render_checkbox(section, "Use Sidebar Navigation?", "sidebar_nav")
    render_checkbox(section, "Use Custom CSS?", "custom_css")
    render_text_area(section, "Layout and Style Notes", "ui_notes", "e.g., Show summary in sidebar, use tabs for each stage, apply clean clinical colors")
    if st.button("💡 Ask Assistant (Section 10)"):
        show_llm_modal(section)

# Section 11: README Metadata
with st.expander("📄 Section 11: README Metadata"):
    section = "Section 11"
    st.session_state.form_data.setdefault(section, {})
    render_text_area(section, "Use Case", "readme_use", "e.g., Primary care clinicians assessing cardiovascular risk")
    render_text_area(section, "Limitations", "readme_limit", "e.g., Not validated for patients under 18 or with incomplete labs")
    render_text_area(section, "Evidence or References", "readme_refs", "e.g., Wilson et al. 1998 Framingham Heart Study")
    render_text_area(section, "Owner's Insight", "readme_owner", "e.g., Built during pilot with Health Universe for risk tool validation")
    if st.button("💡 Ask Assistant (Section 11)"):
        show_llm_modal(section)

# Section 12: Privacy & Compliance
with st.expander("🛡 Section 12: Privacy & Compliance"):
    section = "Section 12"
    st.session_state.form_data.setdefault(section, {})
    render_radio(section, "Handles PHI/PII?", "handles_phi", ["Yes", "No"])
    render_radio(section, "Requires Anonymization?", "anonymize", ["Yes", "No"])
    render_multiselect(section, "Compliance Standards", "compliance", ["HIPAA", "GDPR", "Other"])
    render_text_area(section, "Privacy Measures", "privacy_notes", "e.g., Mask names and MRNs, encrypt stored outputs, restrict access to authorized users")
    if st.button("💡 Ask Assistant (Section 12)"):
        show_llm_modal(section)
        
# Final Submit and Markdown Export
st.markdown("---")
st.subheader("📦 Final Submission")

if st.button("🚀 Submit & Generate Spec"):
    export_lines = ["# Health Universe App Intake Form"]
    for section, content in st.session_state.form_data.items():
        export_lines.append(f"\n## {section}")
        for key, value in content.items():
            if isinstance(value, list):
                export_lines.append(f"**{key.replace('_', ' ').title()}**: {', '.join(value)}")
            else:
                export_lines.append(f"**{key.replace('_', ' ').title()}**: {value}")
    export_md = "\n".join(export_lines)
    st.download_button("📥 Download Markdown File", export_md, file_name="health_universe_intake.md")
    st.success("✅ Your intake spec has been generated. You can download it above.")