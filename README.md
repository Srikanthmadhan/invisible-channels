
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
