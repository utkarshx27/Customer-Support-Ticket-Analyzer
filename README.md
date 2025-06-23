# AI Customer Support Ticket Analyzer

This project uses LLM agents to **analyze customer support tickets**, extracting insights like sentiment, issue type, urgency level, and more. Built with [`pydantic-ai`](https://github.com/pydantic/pydantic-ai) and integrates models like `llama3-70b-8192`.

---

## 🚀 Features

- 🔍 **Summarizes customer issues** into short support-readable form.
- 😠 **Detects sentiment**: positive, neutral, negative.
- 🚨 **Prioritizes tickets** (Critical/P1 to Low/P4) based on customer tier + tone.
- 🏷️ **Classifies issues** into categories (e.g., bug, feature_request, security).
- 📦 Clean, modular pipeline using `pydantic`, `pydantic-ai`, and `Groq/OpenAI`.

---

## 📁 Project Structure

```bash
.
├── app.py               # Main script to run the pipeline
├── test_case.json       # Sample input ticket(s)
├── README.md            # This file
```
## Requirements
Install dependencies using:
```
pip install pydantic-ai groq pydantic
```
How to Run API:
```
python app.py
```

