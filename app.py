import streamlit as st
import re

# --- CORE CONFIGURATION ---
BIT_0 = "\u200c"  # Zero Width Non-Joiner (0)
BIT_1 = "\u200d"  # Zero Width Joiner (1)

# Markers to identify which strategy was used
MARKER_TEXT  = "\u200b"  # Zero Width Space
MARKER_EMOJI = "\ufe0f"  # Variation Selector-16

# --- HELPER: BINARY CONVERSION ---
def bits_to_text(bit_string):
    """Converts a string of 0s and 1s back to UTF-8 text."""
    try:
        chars = [chr(int(bit_string[i:i+8], 2)) for i in range(0, len(bit_string), 8)]
        return "".join(chars)
    except:
        return None

# --- STRATEGY 1: TEXT DISTRIBUTED ---
def embed_text(text, secret):
    words = text.split()
    if len(secret) > len(words):
        return None, f"Cover text too short! You need {len(secret)} words."

    new_words = []
    for i, word in enumerate(words):
        if i < len(secret):
            # 1 char -> 8 bits
            bits = format(ord(secret[i]), '08b')
            # Structure: Word + Marker + 8_Hidden_Bits
            payload = MARKER_TEXT + "".join(BIT_1 if b == '1' else BIT_0 for b in bits)
            new_words.append(word + payload)
        else:
            new_words.append(word)
    return " ".join(new_words), None

# --- STRATEGY 2: EMOJI BURST ---
def embed_emoji(text, secret):
    # Find all emoji-like chunks
    # This regex looks for characters outside standard ASCII
    parts = re.split(r'([^\x00-\x7F]+)', text)
    
    # Locate the first valid emoji/symbol to serve as the carrier
    target_idx = -1
    for i, part in enumerate(parts):
        if any(ord(c) > 127 for c in part):
            target_idx = i
            break
            
    if target_idx == -1:
        return None, "No emojis found in text to hide the payload."

    # Convert ENTIRE secret to one long binary stream
    full_bits = "".join(format(ord(c), '08b') for c in secret)
    
    # Structure: Emoji + Marker + Long_Hidden_Stream
    payload = MARKER_EMOJI + "".join(BIT_1 if b == '1' else BIT_0 for b in full_bits)
    
    parts[target_idx] = parts[target_idx] + payload
    return "".join(parts), None

# --- THE FIX: ROBUST EXTRACTION ---
def extract_robust(text):
    # 1. SEARCH FOR EMOJI SMUGGLING
    # Regex explanation:
    # Look for the Emoji Marker (\ufe0f), followed immediately by 
    # a sequence of strictly ZWJ/ZWNJ characters (our bits).
    # The pattern matches the longest possible chain.
    emoji_pattern = re.compile(f"{MARKER_EMOJI}([{BIT_0}{BIT_1}]+)")
    emoji_matches = emoji_pattern.findall(text)
    
    if emoji_matches:
        # We take the longest match found (in case there are partial fragments)
        longest_match = max(emoji_matches, key=len)
        raw_bits = longest_match.replace(BIT_0, "0").replace(BIT_1, "1")
        decoded = bits_to_text(raw_bits)
        if decoded:
            return "Emoji Strategy", decoded

    # 2. SEARCH FOR TEXT SMUGGLING
    # Regex explanation:
    # Look for the Text Marker (\u200b) followed by exactly 8 ZWJ/ZWNJ chars
    text_pattern = re.compile(f"{MARKER_TEXT}([{BIT_0}{BIT_1}]{{8}})")
    text_matches = text_pattern.findall(text)
    
    if text_matches:
        decoded_chars = []
        for match in text_matches:
            raw_byte = match.replace(BIT_0, "0").replace(BIT_1, "1")
            decoded_chars.append(chr(int(raw_byte, 2)))
        return "Text Strategy", "".join(decoded_chars)

    return None, "No hidden watermark detected."

# --- STREAMLIT UI ---
st.set_page_config(page_title="invisible-channels", page_icon="🕵️")

st.title("invisible-channels")
st.caption("unicode doing crimes again")

tab1, tab2 = st.tabs(["🔒 Embed", "🔓 Extract"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        mode = st.radio("Mode", ["Emoji Smuggling", "Text Distribution"])
        user_text = st.text_area("Cover Text", 
                                 value="Love this! ❤️ 🚀" if mode == "Emoji Smuggling" else "This is a secure channel.",
                                 height=100)
    with col2:
        secret_input = st.text_input("Secret Payload", "Attack at dawn")
        st.info("💡 Tip: Emoji mode is safer for copy-pasting.")
        
    if st.button("Generate Stego-Text"):
        if not user_text or not secret_input:
            st.error("Text and Secret are required.")
        else:
            if mode == "Emoji Smuggling":
                res, err = embed_emoji(user_text, secret_input)
            else:
                res, err = embed_text(user_text, secret_input)
            
            if err:
                st.error(err)
            else:
                st.success("Generated! Copy below:")
                st.code(res, language=None)

with tab2:
    st.write("Paste suspicious text below. The system scans for both strategies.")
    scan_text = st.text_area("Input Text", height=100)
    
    if st.button("Scan for Secrets"):
        if scan_text:
            method, result = extract_robust(scan_text)
            if method:
                st.success(f"✅ Detected: {method}")
                st.markdown(f"### 🔑 Secret: `{result}`")
            else:
                st.warning("❌ No valid hidden data found.")
                st.caption("Ensure you copied the text exactly. Some apps strip invisible characters.")
