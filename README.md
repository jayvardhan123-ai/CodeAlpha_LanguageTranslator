# 🌐 Professional AI Language Translator

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Translate](https://img.shields.io/badge/API-Google%20Translate-4285F4.svg?style=for-the-badge&logo=google-translate&logoColor=white)](https://translate.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An enterprise-ready, professional **AI Language Translator** web application engineered for the **CodeAlpha Artificial Intelligence Internship**. This project incorporates state-of-the-art NLP translators, voice command processing, cached text-to-speech audio rendering, session logs, and a sleek, fully responsive modern **Glassmorphism UI/UX** that looks stunning in both light and dark environments.

---

## 🌟 Key Features

### 💎 Main Features
1. **Instant Translation Engine**: Translates complex paragraphs seamlessly using Google Translate's translation servers.
2. **Auto-Language Detection**: Smartly identifies the source language of input text in real-time, removing the need for manual input selection.
3. **Responsive Glassmorphism UI**: Beautiful semi-transparent containers, harmony colors, active glowing states, and responsive styling.
4. **Text-to-Speech (TTS)**: Converts translated text into highly accurate spoken voice using custom audio bytes stream interfaces.
5. **Interactive Language Swap**: A 1-click rotation button that instantly swaps source/target languages and their corresponding texts.
6. **Robust Session History**: Persistent active list containing timestamps, language tags, and search tools.
7. **Document Export & Downloading**: Download completed translations as structured `.txt` files in a single click.
8. **Built-in Character Count**: Real-time character tracker alerting users as they approach API thresholds.
9. **Copy Utility**: Native copy-to-clipboard blocks featuring built-in copy controls.
10. **Developer Portfolio integration**: Sleek CV/showcase panel directly embedded inside the app's routing.

### 🚀 Advanced Capabilities
* **Speech-to-Text Input (STT)**: Speaks directly into the browser to capture voice and automatically transcribe it into the input area.
* **In-Memory Audio Cache**: Tracks and stores generated audio bytes locally. Repeated playbacks do not query external APIs, saving network bandwidth.
* **Filter History Query**: A dynamic text search to look up and filter past translations from the sidebar.
* **Dynamic Restore Callback**: Click "Restore" on any history item to instantly reload its configuration back into the primary workspace!

---

## 🛠️ Technologies Used

- **Python**: Core logic programming language.
- **Streamlit**: Web interface framework.
- **deep-translator**: High-stability Google Translate engine integrations.
- **gTTS**: Google Text-to-Speech audio synthesizer.
- **streamlit-mic-recorder**: Browser-based client microphone capture.
- **HTML5/CSS3**: Custom glassmorphism, pulse loaders, font styling, and layout overrides.

---

## 📂 Project Directory Structure

```text
CodeAlpha_LanguageTranslator/
│
├── app.py                  # Main Python application (modular logic, routing, UI panels)
├── requirements.txt        # Hardened, tested list of dependencies
├── README.md               # Extensive project documentation
│
├── assets/                 # Brand assets and styling files
│   └── styles.css          # Injected custom CSS rules for glassmorphic elements
│
└── screenshots/            # Screenshots directory for GitHub showcase
    ├── workspace.png       # Primary translator UI screenshot
    ├── history.png         # Historical logs panel view
    └── portfolio.png       # Embedded CV showcase panel
```

---

## 💻 Installation & Setup Guide

Ensure you have **Python 3.9 or higher** installed on your operating system.

### 1. Clone or Copy the Repository
```bash
git clone https://github.com/your-username/CodeAlpha_LanguageTranslator.git
cd CodeAlpha_LanguageTranslator
```

### 2. Install Required Dependencies
Run the package manager inside your terminal to install the tested, stable versions of the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
Start the local development server:
```bash
streamlit run app.py
```

The application will launch automatically in your default browser at `http://localhost:8501`.

---

## 📷 Screenshots Section

*Add your visual portfolio screenshots here to draw attention to your GitHub repository!*

| 🌐 Translator Workspace | 📜 Session History | 👨‍💻 Developer Portfolio |
| :---: | :---: | :---: |
| ![Workspace Screenshot](screenshots/workspace.png) | ![History Screenshot](screenshots/history.png) | ![Portfolio Screenshot](screenshots/portfolio.png) |

*(Note: Replace placeholders in the `screenshots/` directory with actual images after running the app!)*

---

## 🚀 Live Demo & Deployment Guide

This project is optimized for direct hosting on the **Streamlit Community Cloud** (which is free and runs seamlessly!):

1. **Push your code to GitHub**: Create a repository containing `app.py`, `requirements.txt`, `README.md`, and `assets/`.
2. **Log into Streamlit**: Visit [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3. **Deploy App**: Select your repository, branch, and set `app.py` as the entrypoint. Click **Deploy**!
4. **Link in LinkedIn**: Embed the deployed URL directly in your CodeAlpha Internship experience description or project list.

---

## 📈 Future Enhancements

- [ ] **Multi-Engine Translation**: Support toggling between Google Translate, DeepL, and MyMemory APIs.
- [ ] **OCR File Translation**: Upload `.pdf` or `.docx` files to translate entire documents.
- [ ] **Offline Translation Mode**: Incorporate local MarianMT models to run translations fully offline.
- [ ] **Custom Voice Avatars**: Offer multiple voice accents (e.g., US, UK, Australia for English) in the Text-to-Speech settings.

---

## 🤝 Acknowledgements

Developed as part of the **CodeAlpha Artificial Intelligence Internship**. Special thanks to the mentors and the CodeAlpha community for providing this structured learning opportunity.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
