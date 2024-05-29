# AI Caddy for Augusta National using ChatGPT-Turbo-3.5 with RAG.

Scraped data and added to chromadb for document retrieval to prevent LLM hallucination.
Gives advice on any hole at Augusta National.

`masters.py` scrapes and stores the data.

`caddy.py` contains the frontend and LLM-querying.

Deployed at [ai-caddy.streamlit.app](https://ai-caddy.streamlit.app/)
