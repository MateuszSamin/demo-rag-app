# Demo RAG App

Upload a PDF, ask a question about it, and inspect the passages retrieved for the answer. The app runs locally with a Streamlit interface, a FastAPI backend, Ollama, and a Qdrant database.

## 1. Set up the project

These commands use a macOS or Linux shell. Install Python 3 with venv and pip, Git, Docker, and Ollama. On macOS, launch Docker Desktop and the Ollama app before continuing.

On GitHub, copy the repository's HTTPS URL from **Code**. Replace `REPOSITORY_URL` below with that URL. If you already have a local checkout, open a terminal in its root directory and skip the clone.

```bash
git clone REPOSITORY_URL demo-rag-app
cd demo-rag-app
```

Create a separate Python environment for each part of the app. Run these commands from the directory containing `backend/` and `frontend/`. If you already created either environment, reuse it and run its install command.

```bash
python3 -m venv backend/venv
backend/venv/bin/python -m pip install -r backend/requirements.txt

python3 -m venv frontend/venv
frontend/venv/bin/python -m pip install -r frontend/requirements.txt
```

## 2. Download the Ollama models

```bash
ollama pull nomic-embed-text
ollama pull llama3.1:8b
ollama list
```

Check that both models appear in the list. The backend uses `nomic-embed-text` to embed passages and questions, and `llama3.1:8b` to write answers. Keep Ollama running while using the app. If you run Ollama from the command line, start `ollama serve` in a separate terminal before pulling models.

The reranker, `cross-encoder/ms-marco-MiniLM-L6-v2`, is loaded by Sentence Transformers in the backend. Allow internet access on the first run so it and Docling can download their model and tokenizer files.

## 3. Start Qdrant

Create the database container once. The named volume keeps indexed passages between restarts.

```bash
docker run -d --name qdrant \
  -p 127.0.0.1:6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

If you have already created the container, run `docker start qdrant` instead. Open the [Qdrant dashboard](http://localhost:6333/dashboard) to check that the database is reachable. The backend creates its collection when it indexes the first PDF with usable text.

## 4. Run the backend and frontend

Open **two terminals in the repository root**. Leave both processes running.

**Terminal 1 — FastAPI backend**

```bash
cd backend
venv/bin/python -m uvicorn main:app --reload
```

Wait for `Application startup complete`, then open the [API documentation](http://127.0.0.1:8000/docs). You can test the upload and chat endpoints here independently of Streamlit.

**Terminal 2 — Streamlit frontend**

```bash
cd frontend
venv/bin/python -m streamlit run app.py
```

If your Streamlit entry file has a different name, substitute its filename for `app.py`. Open the local URL printed by Streamlit, usually [http://localhost:8501](http://localhost:8501). The frontend's `BACKEND_URL` should be `"http://localhost:8000"`.

## 5. Try your first question

1. Pick an English PDF with selectable text and a fact you can check, such as a report with a project deadline.
2. Choose the PDF in the sidebar and click **Upload**. Wait for indexing to finish. The first upload can take longer while Docling loads its resources.
3. Ask a specific question, such as **“What deadline does the report give for the first milestone?”**
4. Expand a source below the answer and compare the retrieved passage with the PDF.

During upload, Docling splits the PDF into passages. The backend embeds each passage and stores its text and source metadata in Qdrant. When you ask a question, vector search and BM25 keyword search gather candidates. The cross-encoder ranks them, and the backend sends up to five passages by default to the chat model.

## Stopping and restarting

Press **Ctrl+C** in each application terminal to stop Streamlit and FastAPI. To stop the database, run `docker stop qdrant`. For the next session, start Docker and Ollama, run `docker start qdrant`, and repeat step 4. Installed packages, downloaded models, and data in the Qdrant volume persist between sessions.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Streamlit cannot connect to the backend | Open the API docs on port 8000. Check that `BACKEND_URL` includes both slashes in `http://localhost:8000`. |
| The sidebar shows a 404 while loading documents | Check the list-documents route in the API docs and match its path in the frontend. |
| Ollama reports a missing model | Run `ollama list` and pull the exact model tag used in the backend. |
| Qdrant connection refused | Run `docker ps` and check that the Qdrant container exposes port 6333. |
| Chat raises `KeyError: 'filename'` | Older points may lack source metadata. To test without deleting them, configure a fresh collection name for both indexing and retrieval, restart the backend, and upload the PDF again. |
