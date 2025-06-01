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
    st.header("📄 Reference Document")
    uploaded_file = st.file_uploader("Upload .md file", type=["md"])
    if uploaded_file:
        st.session_state["ref_doc"] = uploaded_file.read().decode("utf-8")
    else:
        st.session_state["ref_doc"] = ""
    st.markdown("---")
    st.header("🧭 Form Progress")
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

with st.expander("📌 Section 2: Core Logic"):
    section = "Section 2"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_2", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 2)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 3: Inputs & Data Entry"):
    section = "Section 3"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_3", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 3)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 4: Outputs"):
    section = "Section 4"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_4", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 4)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 5: Overlays / Imaging"):
    section = "Section 5"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_5", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 5)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 6: Storage & Retrieval"):
    section = "Section 6"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_6", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 6)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 7: Reference / RAG"):
    section = "Section 7"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_7", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 7)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 8: App Modality"):
    section = "Section 8"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_8", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 8)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 9: APIs & Plugins"):
    section = "Section 9"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_9", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 9)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 10: UI & UX"):
    section = "Section 10"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_10", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 10)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 11: README Insights"):
    section = "Section 11"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_11", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 11)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 12: Privacy & Compliance"):
    section = "Section 12"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Describe this section's design and goals", "desc_12", "Explain how this applies to the app.")
        if st.button("💡 Ask Assistant (Section 12)"):
            st.session_state["llm_section"] = section
    with right:
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


# Expanding Sections 2–12 with full detail...

# Section 2: Core Logic
with st.expander("📌 Section 2: Core Logic"):
    section = "Section 2"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "What is the logic model used?", "model_description", "e.g., Logistic regression, Rule-based tree, etc.")
        render_text_area(section, "Formula or algorithm details", "formula", "Include equation or clinical logic breakdown.")
        render_text_area(section, "Input dependencies", "input_dependencies", "What does this logic depend on? E.g., age, BP, labs.")
        render_radio(section, "Can logic run with missing inputs?", "handle_missing", ["Yes", "No", "Depends"])
        render_text_area(section, "Default values or assumptions", "defaults", "e.g., Average values for age, BMI, etc.")
        if st.button("💡 Ask Assistant (Section 2)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 3: Inputs & Data Entry"):
    section = "Section 3"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Required User Inputs", "required_inputs", "e.g., Age, Gender, Smoker")
        render_text_area(section, "Acceptable Input Formats", "input_formats", "e.g., Free text, Dropdowns, Files")
        render_text_area(section, "Optional Inputs", "optional_inputs", "e.g., BP, HbA1c if available")
        render_text_area(section, "File Types Accepted", "file_types", "e.g., .csv, .json, DICOM")
        if st.button("💡 Ask Assistant (Section 3)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 4: Outputs"):
    section = "Section 4"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Output Values or Categories", "output_values", "e.g., Risk score, Yes/No")
        render_text_area(section, "Display Format", "display_format", "e.g., Bar chart, Text result")
        render_text_area(section, "Interpretation Guidance", "interpretation", "e.g., 10% = moderate risk")
        if st.button("💡 Ask Assistant (Section 4)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 5: Overlays / Imaging"):
    section = "Section 5"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Visual Output Types", "visual_types", "e.g., Heatmap, Annotation")
        render_text_area(section, "Image Input Requirements", "image_inputs", "e.g., Resolution, Modality")
        render_text_area(section, "Overlay Formats", "overlay_format", "e.g., JSON mask, Bounding box")
        if st.button("💡 Ask Assistant (Section 5)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 6: Storage & Retrieval"):
    section = "Section 6"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Is Data Stored?", "data_storage", "Yes/No/Temporarily")
        render_text_area(section, "Storage Mechanism", "storage_method", "e.g., Local cache, cloud S3")
        render_text_area(section, "Retrieval Capability", "retrieval", "e.g., By user ID, session")
        if st.button("💡 Ask Assistant (Section 6)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 7: Reference / RAG"):
    section = "Section 7"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Will app use reference documents?", "use_docs", "Yes/No")
        render_text_area(section, "Document Type", "doc_type", "e.g., Clinical guidelines, PDFs")
        render_text_area(section, "Search Method", "search_method", "e.g., Embedding + cosine similarity")
        if st.button("💡 Ask Assistant (Section 7)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 8: App Modality"):
    section = "Section 8"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "App Type", "app_type", "Streamlit, FastAPI, A2A, MCP")
        render_text_area(section, "Interaction Style", "interaction", "Form, Chat, Upload, Clickable map")
        if st.button("💡 Ask Assistant (Section 8)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 9: APIs & Plugins"):
    section = "Section 9"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "External APIs Used", "external_apis", "e.g., OpenFDA, PubMed")
        render_text_area(section, "Plugins Needed", "plugins", "e.g., Image viewer, Text summarizer")
        if st.button("💡 Ask Assistant (Section 9)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 10: UI & UX"):
    section = "Section 10"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Instructions or Tooltips Needed?", "tooltips", "Yes/No")
        render_text_area(section, "User Feedback Areas", "feedback", "e.g., Confidence, Notes")
        render_text_area(section, "Styling Requirements", "styling", "e.g., Color palette, CSS file")
        if st.button("💡 Ask Assistant (Section 10)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 11: README Insights"):
    section = "Section 11"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "Use Cases", "use_cases", "e.g., Cardiovascular screening in primary care")
        render_text_area(section, "Limitations", "limitations", "e.g., Cannot handle non-binary genders")
        render_text_area(section, "Evidence Source", "evidence", "e.g., Framingham 2008")
        render_text_area(section, "Developer Notes", "notes", "What should developers keep in mind?")
        if st.button("💡 Ask Assistant (Section 11)"):
            st.session_state["llm_section"] = section
    with right:
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

with st.expander("📌 Section 12: Privacy & Compliance"):
    section = "Section 12"
    st.session_state.form_data.setdefault(section, {})
    left, right = st.columns([2, 1])
    with left:
        render_text_area(section, "PHI Used?", "phi", "Yes/No")
        render_text_area(section, "Anonymization Steps", "anonymize", "e.g., Remove name, DOB")
        render_text_area(section, "Compliance Type", "compliance", "e.g., HIPAA, GDPR")
        if st.button("💡 Ask Assistant (Section 12)"):
            st.session_state["llm_section"] = section
    with right:
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
