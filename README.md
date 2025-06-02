# Intake


health-universe-intake-form/
│
├── app.py                      # Main Streamlit app entrypoint
├── llm_helper.py              # ask_ollama() integration
├── requirements.txt           # Streamlit + dependencies
├── style.css                  # App styling
├── README.md
│
├── sections/                  # 🔢 One section per file
│   ├── __init__.py
│   ├── section_1.py
│   ├── section_2.py
│   ├── ...
│   └── section_12.py
│
├── components/                # ♻️ Reusable UI components
│   ├── __init__.py
│   ├── inputs.py              # render_text_area, etc.
│   └── assistant.py           # render_llm_assistant()
│
└── utils/                     # 🛠️ Logic for processing/exporting
    ├── __init__.py
    └── form_export.py         # Markdown output formatter
