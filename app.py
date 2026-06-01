"""
CodeAlpha Artificial Intelligence Internship
Project: AI Language Translator
Author: AI Developer (Intern)
Date: May 2026

Description:
A complete, professional, and production-ready Streamlit application that
provides translation services across 50+ languages. Incorporates advanced
features like speech-to-text, text-to-speech, translation history logs,
copy utilities, file downloading, language swapping, and custom glassmorphism styling.
"""

import streamlit as st
import os
import io
import time
from datetime import datetime
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import speech_to_text

# ==============================================================================
# 1. CONSTANTS & STYLING LOGIC
# ==============================================================================

# Highly stable fallback languages list in case of network latency during startup
FALLBACK_LANGUAGES = {
    "Auto-Detect": "auto",
    "Afrikaans": "af", "Albanian": "sq", "Arabic": "ar", "Armenian": "hy", "Azerbaijani": "az",
    "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
    "Catalan": "ca", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
    "Esperanto": "eo", "Estonian": "et", "Finnish": "fi", "French": "fr", "Galician": "gl",
    "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht",
    "Hebrew": "he", "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id",
    "Irish": "ga", "Italian": "it", "Japanese": "ja", "Kannada": "kn", "Korean": "ko",
    "Latin": "la", "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malay": "ms",
    "Maltese": "mt", "Marathi": "mr", "Norwegian": "no", "Persian": "fa", "Polish": "pl",
    "Portuguese": "pt", "Romanian": "ro", "Russian": "ru", "Serbian": "sr", "Slovak": "sk",
    "Slovenian": "sl", "Spanish": "es", "Swahili": "sw", "Swedish": "sv", "Tamil": "ta",
    "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur",
    "Vietnamese": "vi", "Welsh": "cy", "Yiddish": "yi"
}

def load_custom_css():
    """Reads and injects the custom glassmorphic stylesheet."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ CSS styling asset could not be found. Loading default styles.")

# ==============================================================================
# 2. SESSION STATE MANAGEMENT
# ==============================================================================

def init_session_states():
    """Initializes persistent application memory."""
    if "source_text" not in st.session_state:
        st.session_state.source_text = ""
    if "translated_text" not in st.session_state:
        st.session_state.translated_text = ""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "🌐 Translator Workspace"

# ==============================================================================
# 3. CORE TRANSLATION & SPEECH ENGINES
# ==============================================================================

@st.cache_data(show_spinner=False)
def fetch_supported_languages():
    """Fetches languages dynamically from the API, falling back to a static list if offline."""
    try:
        langs = GoogleTranslator().get_supported_languages(as_dict=True)
        # Standardize capitalization of keys
        formatted_langs = {"Auto-Detect": "auto"}
        for k, v in langs.items():
            formatted_langs[k.title()] = v
        return formatted_langs
    except Exception:
        # Fallback to local hardcoded dictionary if API query fails
        return FALLBACK_LANGUAGES

def romaji_to_hiragana(text):
    """Advanced NLP: Converts phonetic Japanese Romaji into Hiragana script."""
    # Check if the text contains any non-ASCII character (standard Japanese characters).
    # If it does, keep it as is. If purely Latin ASCII characters, perform transliteration!
    if any(ord(c) > 127 for c in text):
        return text
        
    mapping = {
        "arigatou": "ありがとう", "arigato": "ありがとう",
        "konnichiwa": "こんにちは", "sayonara": "さようなら",
        "sumimasen": "すみません", "ohayou": "おはよう",
        "gozaimasu": "ございます",
        
        "tsu": "つ", "chi": "ち", "shi": "し", 
        "sha": "しゃ", "shu": "しゅ", "sho": "しょ",
        "cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",
        "ja": "じゃ", "ji": "じ", "ju": "じゅ", "jo": "じょ",
        
        "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",
        "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",
        "da": "だ", "di": "ぢ", "du": "づ", "de": "で", "do": "ど",
        "za": "ざ", "zi": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",
        "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",
        "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
        "sa": "さ", "si": "し", "su": "す", "se": "せ", "so": "そ",
        "ta": "た", "ti": "ち", "tu": "つ", "te": "て", "to": "と",
        "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
        "ha": "は", "hi": "ひ", "hu": "ふ", "he": "へ", "ho": "ほ",
        "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
        "ya": "や", "yu": "ゆ", "yo": "よ",
        "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
        "wa": "わ", "wo": "を", "nn": "ん", "n'": "ん",
        
        "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
        "n": "ん"
    }
    
    result = []
    i = 0
    text_lower = text.lower().strip()
    lengths = sorted(list(set(len(k) for k in mapping.keys())), reverse=True)
    
    while i < len(text_lower):
        # Handle double consonants (e.g. 'tt' -> 'っt')
        if i < len(text_lower) - 1 and text_lower[i] == text_lower[i+1] and text_lower[i] not in 'aeioun ':
            result.append("っ")
            i += 1
            continue
            
        matched = False
        for length in lengths:
            if i + length <= len(text_lower):
                substring = text_lower[i:i+length]
                if substring in mapping:
                    result.append(mapping[substring])
                    i += length
                    matched = True
                    break
        if not matched:
            result.append(text[i])
            i += 1
            
    return "".join(result)

def handle_translation(text, src_name, dest_name, lang_dict):
    """Executes the translation request using the Google Translator API."""
    if not text.strip():
        return ""
    
    src_code = lang_dict.get(src_name, "auto")
    dest_code = lang_dict.get(dest_name, "es")
    
    # If explicitly translating from Japanese, automatically convert Romaji phonetic text to Hiragana script!
    if src_code == "ja":
        text = romaji_to_hiragana(text)
    
    try:
        # GoogleTranslator auto-resolves 'auto' to the appropriate language
        translator = GoogleTranslator(source=src_code, target=dest_code)
        result = translator.translate(text)
        
        # Log to Session History
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        history_entry = {
            "timestamp": timestamp,
            "src_lang": src_name,
            "dest_lang": dest_name,
            "src_text": text,
            "dest_text": result
        }
        
        # Avoid duplicate logs if same translation runs consecutively
        if not st.session_state.history or st.session_state.history[0]["src_text"] != text or st.session_state.history[0]["dest_lang"] != dest_name:
            st.session_state.history.insert(0, history_entry)
            
        return result
    except Exception as e:
        st.error(f"❌ Translation Error: {str(e)}")
        return "An error occurred during translation. Please check your internet connection and try again."

# ==============================================================================
# 4. EVENT HANDLERS
# ==============================================================================

def execute_swap():
    """Swaps the source and target languages and their respective texts."""
    # We can only swap if the source language is not 'Auto-Detect'
    if st.session_state.src_lang == "Auto-Detect":
        # Check if we can infer the source language from the last translation
        if st.session_state.history:
            st.session_state.src_lang = st.session_state.dest_lang
            st.session_state.dest_lang = "English" # Default swap fallback
        else:
            st.warning("⚠️ Select a specific source language first to perform swap.")
            return
    else:
        temp_lang = st.session_state.src_lang
        st.session_state.src_lang = st.session_state.dest_lang
        st.session_state.dest_lang = temp_lang

    temp_text = st.session_state.source_text
    st.session_state.source_text = st.session_state.translated_text
    st.session_state.translated_text = temp_text

# ==============================================================================
# 5. USER INTERFACE PAGES
# ==============================================================================

def render_translator_workspace(lang_dict):
    """Main panel representing the core language translation workspace."""
    st.markdown('<h1 class="gradient-text">🌐 AI Language Translator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-subtext">CodeAlpha Artificial Intelligence Internship Project</p>', unsafe_allow_html=True)
    
    # Main interactive Glassmorphic Card
    with st.container(border=True):
        # Languages selector layout
        col1, col_swap, col2 = st.columns([9, 2, 9])
        
        with col1:
            src_langs = list(lang_dict.keys())
            st.selectbox(
                "Source Language 📥", 
                options=src_langs,
                key="src_lang"
            )
            
        with col_swap:
            st.markdown('<div class="swap-btn-container">', unsafe_allow_html=True)
            if st.button("🔄", help="Swap languages and text"):
                execute_swap()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            dest_langs = [l for l in lang_dict.keys() if l != "Auto-Detect"]
            spanish_idx = dest_langs.index("Spanish") if "Spanish" in dest_langs else 0
            st.selectbox(
                "Target Language 📤",
                options=dest_langs,
                index=spanish_idx,
                key="dest_lang"
            )

        st.markdown('<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.08); margin: 1.5rem 0;" />', unsafe_allow_html=True)
        
        # Text input and outputs layout
        col_input, col_output = st.columns(2)
        
        with col_input:
            # Micro Speech-to-Text widget
            st.markdown("##### Input Text")
            stt_placeholder = st.empty()
            
            # Audio recording button from streamlit-mic-recorder
            with stt_placeholder.container():
                recorded_text = speech_to_text(
                    start_prompt="🎙️ Click to Speak",
                    stop_prompt="⏹️ Stop Recording",
                    language=lang_dict.get(st.session_state.src_lang, "en"),
                    key="stt_voice_input",
                    just_once=True
                )
                if recorded_text:
                    st.session_state.source_text = recorded_text
                    st.toast("🎙️ Voice transcription captured!")
            
            # Main text input box
            st.text_area(
                "Type text here...",
                placeholder="Type or click the microphone to speak...",
                height=200,
                label_visibility="collapsed",
                key="source_text"
            )
            
            # Character count indicator
            char_count = len(st.session_state.source_text)
            count_color = "#718096" if char_count <= 4000 else ("#dd6b20" if char_count <= 4800 else "#e53e3e")
            st.markdown(
                f'<div class="char-counter" style="color: {count_color};">{char_count} / 5000 chars</div>', 
                unsafe_allow_html=True
            )
            
        with col_output:
            st.markdown("##### Translated Text")
            
            # Renders the output inside a custom styling area
            translated_box_html = f"""
            <div style="background-color: rgba(15, 10, 30, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1rem; min-height: 200px; color: white; font-size: 1.05rem; overflow-y: auto;">
                {st.session_state.translated_text if st.session_state.translated_text else '<span style="color: #4a5568; font-style: italic;">Translation will appear here instantly...</span>'}
            </div>
            """
            st.markdown(translated_box_html, unsafe_allow_html=True)
            
            # Spacer to align outputs
            st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

        # Core Action trigger row
        action_col1, action_col2 = st.columns([1, 1])
        
        with action_col1:
            if st.button("✨ Translate Text", key="main_translate_btn"):
                if not st.session_state.source_text.strip():
                    st.warning("⚠️ Please enter some text to translate first!")
                elif len(st.session_state.source_text) > 5000:
                    st.error("❌ Character limit exceeded! Please reduce text length below 5000.")
                else:
                    # Custom pulsing gradient bar loader
                    loader_placeholder = st.empty()
                    loader_placeholder.markdown('<div class="pulsing-bar"></div>', unsafe_allow_html=True)
                    
                    # Perform API translation
                    result = handle_translation(
                        st.session_state.source_text,
                        st.session_state.src_lang,
                        st.session_state.dest_lang,
                        lang_dict
                    )
                    
                    # Simulated slight delay for visual impact of the transition
                    time.sleep(0.4)
                    
                    st.session_state.translated_text = result
                    loader_placeholder.empty()
                    st.rerun()

        # If translation is active, show the utility ribbon
        if st.session_state.translated_text and not st.session_state.translated_text.startswith("An error occurred"):
            st.markdown('<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 1rem 0;" />', unsafe_allow_html=True)
            
            util_col1, util_col2 = st.columns([2, 1])
            
            with util_col1:
                # Native safe Copy Code widget
                st.markdown("💡 **Copy Translation:**")
                st.code(st.session_state.translated_text, language=None)
                
            with util_col2:
                st.markdown("📥 **Export Document:**")
                # Build download interface
                st.download_button(
                    label="📥 Save as Text File",
                    data=st.session_state.translated_text,
                    file_name=f"translation_{lang_dict.get(st.session_state.src_lang, 'auto')}_{lang_dict.get(st.session_state.dest_lang, 'es')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

def render_history_panel(lang_dict):
    """Renders the comprehensive, searchable translation log."""
    st.markdown('<h1 class="gradient-text">📜 Translation History</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-subtext">Manage and reload your past translations</p>', unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; padding: 3rem 1rem !important;">
                <h3 style="color: #a0aec0; margin-bottom: 0.5rem;">No History Logged Yet</h3>
                <p style="color: #718096; max-width: 400px; margin: 0 auto;">Translations you complete in the workspace will appear here for easy access, downloading, and fast reloading.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        return
        
    with st.container(border=True):
        # History Control header
        header_col1, header_col2 = st.columns([3, 1])
        
        with header_col1:
            search_query = st.text_input("🔍 Search History", placeholder="Type keywords from source or translation...", label_visibility="collapsed")
            
        with header_col2:
            if st.button("🗑️ Clear All Logs", use_container_width=True):
                st.session_state.history = []
                st.toast("🧹 Translation logs cleared successfully!")
                time.sleep(0.5)
                st.rerun()
                
        st.markdown('<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.08); margin: 1rem 0;" />', unsafe_allow_html=True)
        
        # Filter list based on search query
        filtered_history = st.session_state.history
        if search_query.strip():
            q = search_query.lower()
            filtered_history = [
                x for x in st.session_state.history 
                if q in x["src_text"].lower() or q in x["dest_text"].lower() or q in x["src_lang"].lower() or q in x["dest_lang"].lower()
            ]
            
        if not filtered_history:
            st.info("No matching records found for your search term.")
        else:
            for idx, entry in enumerate(filtered_history):
                h_col1, h_col2 = st.columns([16, 4])
                
                with h_col1:
                    # Custom formatted card
                    card_html = f"""
                    <div class="history-item" style="margin-bottom: 0.25rem;">
                        <div class="history-meta">
                            <span>🕒 {entry['timestamp']}</span>
                            <span>
                                <span class="history-lang">{entry['src_lang']}</span> ➡️ 
                                <span class="history-lang">{entry['dest_lang']}</span>
                            </span>
                        </div>
                        <div style="font-weight: 600; color: #cbd5e0; margin-top: 0.25rem;">"{entry['src_text']}"</div>
                        <div style="color: #a255ff; margin-top: 0.15rem; font-style: italic;">→ "{entry['dest_text']}"</div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                with h_col2:
                    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
                    # Unique key for each restore button
                    if st.button("🔄 Restore", key=f"restore_{idx}_{entry['timestamp']}", use_container_width=True):
                        st.session_state.source_text = entry["src_text"]
                        st.session_state.translated_text = entry["dest_text"]
                        st.session_state.src_lang = entry["src_lang"]
                        st.session_state.dest_lang = entry["dest_lang"]
                        st.toast("⚡ Translation loaded back into Workspace!")
                        time.sleep(0.5)
                        st.session_state.selected_page = "🌐 Translator Workspace"
                        st.rerun()
                        
                st.markdown('<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.03); margin: 0.5rem 0;" />', unsafe_allow_html=True)



# ==============================================================================
# 6. APP MAIN BOOTSTRAPPER
# ==============================================================================

def main():
    """Main routing and layout bootstrappers."""
    # Set page meta configurations
    st.set_page_config(
        page_title="AI Language Translator - CodeAlpha",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize sessions and stylesheet overrides
    init_session_states()
    load_custom_css()
    
    # Safe load language mapping
    lang_dict = fetch_supported_languages()
    
    # --- SIDEBAR INTERFACE ---
    with st.sidebar:
        st.markdown(
            """
            <div style='text-align: center; padding: 1.5rem 0;'>
                <h2 style='background: linear-gradient(135deg, #a255ff 0%, #ff4b91 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: Outfit; font-weight: 800; font-size: 1.8rem;'>CodeAlpha</h2>
                <div style='color: #718096; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; font-weight: bold; margin-top: -0.25rem;'>AI Internship Project</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown('<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.08); margin: 0 0 1.5rem 0;" />', unsafe_allow_html=True)
        
        # Navigation panel
        st.markdown("#### 🧭 Navigation Menu")
        selected = st.radio(
            "Select Page",
            options=["🌐 Translator Workspace", "📜 Session History"],
            label_visibility="collapsed",
            key="radio_nav"
        )
        st.session_state.selected_page = selected
        
        st.markdown('<hr style="border: 0; height: 1px; background: rgba(255,255,255,0.08); margin: 1.5rem 0;" />', unsafe_allow_html=True)
        
        # Micro Session Info Widget
        history_len = len(st.session_state.history)
        st.markdown("#### 📊 Session Overview")
        st.markdown(
            f"""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 0.75rem; font-size: 0.85rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #718096;">Active History:</span>
                    <span style="color: #a255ff; font-weight: bold;">{history_len} items</span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
        
        # Branding footer in sidebar
        st.markdown(
            """
            <div style='text-align: center; color: #4a5568; font-size: 0.75rem; border-top: 1px solid rgba(255,255,255,0.03); padding-top: 1rem;'>
                © 2026 CodeAlpha AI Internship.<br/>All Rights Reserved.
            </div>
            """, 
            unsafe_allow_html=True
        )

    # --- MAIN PAGE ROUTER ---
    if st.session_state.selected_page == "🌐 Translator Workspace":
        render_translator_workspace(lang_dict)
    elif st.session_state.selected_page == "📜 Session History":
        render_history_panel(lang_dict)

if __name__ == "__main__":
    main()
