# Pizza Reviews QA (Web UI)

This small app provides a web frontend to ask questions about a pizza restaurant. It uses the existing `vector.py` retriever and the `OllamaLLM` model like the original `main.py`.

Files added:
- `app.py`: Flask app serving the UI and `/ask` endpoint.
- `templates/index.html`: Minimal frontend.

Quick start

1. Install requirements

   pip install -r requirements.txt

2. Run the app

   python app.py

3. Open http://localhost:5000 in your browser and ask a question.

Notes and assumptions

- This project expects the `chroma_langchain_db` folder to exist and `vector.py` to create or load the Chroma DB.
- The endpoint attempts to call `retriever.get_relevant_documents(question)` and falls back to `retriever.invoke(question)` if needed.
- If you hit issues with the Ollama model or the LangChain bindings, ensure the `langchain-ollama` package is correctly installed and Ollama is running locally (if required by the package).