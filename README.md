# 🚀 👻 Invisible-Channels

**Invisible-Channels** is a Unicode steganography and detection lab that explores how plain-looking text can secretly carry hidden payloads using **zero-width Unicode characters** and **emoji variation selectors**.

> The text looks normal.  
> The data is not.

This project focuses on **both sides of the problem**:
- how covert text channels can be created  
- and how they can be reliably detected  

---

## 🧠 What This Project Explores

Most people think steganography lives in images, audio, or files.

Unicode disagrees.

**Invisible-Channels** demonstrates how:
- zero-width characters can encode binary data  
- emojis can act as high-capacity payload carriers  
- hidden data can survive copy–paste and casual inspection  
- regex-based detection can uncover these covert channels  

This is directly relevant to:
- watermarking research  
- content authenticity (e.g., SynthID-style ideas)  
- security filtering and bypass analysis  
- adversarial text behavior  

---

## 🔬 Techniques Implemented

### 1️⃣ Text Distribution (Word-Level Steganography)

Each word in the cover text carries **one character (8 bits)** of the secret payload.

**Encoding method**
- Zero Width Non-Joiner (ZWNJ) → `0`  
- Zero Width Joiner (ZWJ) → `1`  
- Zero Width Space used as a marker  

**Structure**

This spreads the payload across the sentence, making it difficult to notice without inspection tools.

---

### 2️⃣ Emoji Smuggling (High-Capacity Channel)

Instead of distributing bits across words, this strategy:
- finds an existing emoji in the text  
- appends a hidden binary stream to it  
- uses Variation Selector-16 as a marker  

**Why emojis?**
- they already contain complex Unicode  
- they survive copy–paste extremely well  
- they bypass many naive text filters  

One emoji can carry an entire message invisibly.

---

## 🛡️ Detection Engine (The Important Part)

**Invisible-Channels** is not just about hiding data.

The extraction engine:
- scans for emoji-based payloads first  
- identifies valid marker + bit patterns using regex  
- converts zero-width characters back into binary  
- reconstructs UTF-8 text safely  

If emoji smuggling fails, it falls back to detecting distributed word-level payloads.

This mirrors real-world security tooling:  
**assume adversarial input, verify everything.**

---

## 🧪 Streamlit Demo

A Streamlit interface is included to:
- embed secrets into normal-looking text  
- extract hidden payloads from suspicious input  
- visually demonstrate how invisible channels work  

### Run locally

```bash
pip install streamlit
streamlit run app.py
