# 🫠 OrgGPT

OrgGPT is an **AI-native analyst** designed to revolutionize private equity workflows. It leverages powerful LLMs, vector search, and advanced prompt engineering to transform SEC filings, earnings calls, and investor letters into actionable investment memos.

> Built for investors who think in terms of “conviction”, not clutter.

---

## ✨ Features

* 🔍 **LLM-Powered Analysis**: Extracts insights from complex filings using OpenAI + LangChain.
* 📊 **Deal Memo Generator**: Auto-generates structured, multi-section investment briefs.
* 🌐 **Semantic Search**: Vector-based retrieval over 10-Ks, transcripts, and PDFs.
* 🔧 **Modular Architecture**: Clean Python backend for easy extension.
* 🖋️ **Sleek UI**: Streamlit-based frontend with markdown preview.

---

## 🚀 Quick Start

```bash
# Clone the repo
$ git clone https://github.com/sukanyaghosh74/OrgGPT && cd OrgGPT

# Set up environment
$ python -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt

# Add your OpenAI key
$ echo "OPENAI_API_KEY=your-key-here" > .env

# Run the app
$ streamlit run app/ui.py
```

---

## 🔹 Example Investment Memo

```
**Company Overview:** Microsoft is a global leader in enterprise software, cloud services, and AI tools.

**Financial Highlights:** Revenue grew 14% YoY, with Azure growing at 26%. Operating margin at 38%.

**Risk Factors:** Regulatory scrutiny on antitrust and data practices. Cloud margin pressure from competitors.

**Opportunities:** Generative AI integration across MS365, aggressive cloud market expansion.

**Valuation Notes:** Priced at 32x forward earnings, PEG ratio at 1.8 suggests fair growth premium.
```

---

## 📌 File Structure

```
orggpt/
├── app/
│   ├── loader.py           # Handles file input and chunking
│   ├── vectorstore.py      # Embedding and persistent DB
│   ├── chain.py            # RAG agent logic
│   ├── prompt.py           # Prompt template builder
│   ├── summarizer.py       # Multi-query reducer (optional)
│   └── ui.py               # Streamlit frontend
├── .env
├── run.py
├── requirements.txt
```

---

## 💡 Prompts Used

LLM prompts are designed using Retrieval-Augmented Generation and include:

* “Summarize the business model based on Item 1.”
* “What are the top 3 risks in this document?”
* “Write an investment memo for this company.”

---

## 📈 Tech Stack

* **LLM:** OpenAI GPT-4 / Claude / Mistral (pluggable)
* **Embeddings:** OpenAI `text-embedding-3-small`
* **Vector Store:** ChromaDB (with persistence)
* **Backend:** LangChain, Python 3.10+
* **Frontend:** Streamlit

---

## ✨ What's Next

* [ ] Auto-detect filing sections (e.g. Item 1A, MD\&A)
* [ ] PDF + DOCX export of memos
* [ ] LangGraph-based multi-hop agents
* [ ] Live web ingestion of new filings

---

## 📢 Contributing

PRs welcome! Especially for:

* Prompt engineering
* Agent memory / chaining improvements
* Financial data enrichment

---

## ❤️ Inspiration

OrgGPT was inspired by the pain of digging through hundreds of SEC filings and a belief that investors deserve better tools.

---

## 🩷 Author

Made with 🩷 by Sukanya Ghosh

> "Imagine having a private equity analyst who never sleeps, never misses context, and reasons over everything you've ever read."
