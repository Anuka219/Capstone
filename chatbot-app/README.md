# MEM Guide Bot

Interactive AI chatbot prototype for the MEM/MIM AI Capstone 2026 project.

The selected project is the chatbot creation task from the slide deck: create a chatbot that answers questions about MEM and explain the implementation, tools, and methodology during the presentation.

## Features

- MEM capstone FAQ answers for deadline, group size, presentation, tools, and method
- React chat interface with suggested question buttons
- Small animated guide character that follows the pointer
- Character celebration animation on clicks
- Python FastAPI backend with the same rule-based chatbot logic
- Frontend fallback answers if the backend is not running

## Run The App

Install frontend dependencies:

```bash
cd /Users/anukavarsha/Downloads/Capstone/Capstone/chatbot-app
npm install
```

Install backend dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

Start the backend:

```bash
npm run backend
```

Start the frontend in a second terminal:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

## Presentation Notes

Mention these points in the capstone presentation:

- The chatbot answers questions about the MEM chatbot project using a curated rule-based knowledge base.
- The UI is built with React, TypeScript, Vite, and Tailwind CSS.
- The backend is built with Python and FastAPI.
- The animated character follows the pointer and reacts to clicks to make the chatbot more engaging.
- The current limitation is that it is not connected to a live LLM API yet. That can be added later for more flexible answers.
