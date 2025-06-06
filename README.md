# AI-Assisted Patient Email Replies

A coding exercise project using **FastAPI** and **React** (Vite + TypeScript) to manage patient emails, generate AI reply suggestions, and send responses.

---

## 🗂 Project Structure

```
Joy Interview App/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   └── email_store.py   # JSON-based email persistence
│   └── tests/               # pytest unit tests for backend
│       └── test_main.py
├── frontend/
│   └── ...                  # Vite + React + TypeScript single-page app
```

---

## 🚀 Features

- 📩 Fetch and display patient emails
- 🤖 Use OpenAI (GPT) to suggest draft replies
- 📝 Edit and send final email replies
- ✅ Confirmation UI and test coverage for backend

---

## 🔧 Backend Setup (FastAPI)

1. **Install dependencies**:

```bash
cd backend
pip install -r requirements.txt
```

2. **Run the FastAPI server**:

```bash
uvicorn app.main:app --reload
```

3. **Environment variables**:
Make sure your OpenAI API key is available via environment:

```bash
export OPENAI_API_KEY=your-key-here
```

---

## 💻 Frontend Setup (Vite + React + TS)

1. **Install dependencies**:

```bash
cd frontend
npm install
```

2. **Start dev server**:

```bash
npm run dev
```

3. **UI Library**:
Uses [Shadcn UI](https://ui.shadcn.com/) + TailwindCSS

---

## 🧪 Running Tests

1. **Install `pytest`**:

```bash
pip install pytest
```

2. **Run tests from project root**:

```bash
cd into backend
pytest
```
---

## 📄 File-Based Email Storage
- Emails are read from a `emails.json` file (in `backend/app/`)
- Sent emails are appended to a `sent.json` file

---

## ✅ Example `.env` for backend
```
OPENAI_API_KEY=sk-...
```

---

## ✍️ Author
Josh Levin

---

