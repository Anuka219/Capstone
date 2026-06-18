# Brief Project Report: MEM & MIM Guide Bot

## 1. Project Overview

Our project is an AI chatbot called **MEM & MIM Guide Bot**. The purpose of the chatbot is to help students get quick and clear answers about the Master programs **Engineering and Management (MEM)** and **Industrial Management (MIM)** at Hochschule Pforzheim.

The chatbot works like a study advisor. Users can ask questions about program structure, admission requirements, deadlines, documents, language requirements, course content, and general application guidance.

## 2. Project Objective

The main objective was to create an interactive chatbot prototype that can:

- Answer common questions about MEM and MIM.
- Compare both programs in a simple way.
- Guide applicants through important admission and application details.
- Give cautious fit-check advice without guaranteeing admission.
- Provide a friendly and modern chat experience.
- Demonstrate how generative AI can support student advising.

## 3. What We Built

We built a web-based chatbot interface with a connected backend. The user can type a question, send it to the bot, and receive an answer in the chat window.

Main features include:

- A clean single-page chatbot website.
- Suggested question buttons for quick interaction.
- Chat bubbles for user and bot messages.
- A program overview section for MEM and MIM.
- AI-generated answers based on a controlled system prompt.
- Backend API endpoint for handling chat requests.
- Optional text-to-speech support using ElevenLabs.
- Memory support for saving simple user corrections.
- A React/Vite prototype version with an animated guide character.
- A rule-based fallback chatbot for testing basic project questions.

## 4. Technologies Used

The project uses both frontend and backend technologies.

Frontend:

- HTML, CSS, and JavaScript for the main chatbot website.
- React and TypeScript for the prototype version.
- Vite for frontend development.
- Tailwind CSS for styling in the React version.

Backend:

- Python for chatbot logic.
- FastAPI for creating the web API.
- Uvicorn for running the backend server.
- HTTPX for calling external AI and voice APIs.
- Python dotenv for loading API keys from environment variables.

AI and voice services:

- OpenRouter or Groq for large language model responses.
- ElevenLabs for optional text-to-speech audio.
- Raphael's HS Pforzheim video recordings as an approved voice source for preparing demo voice samples.

## 5. Implementation Summary

First, we studied the project requirements and identified the type of questions students might ask about MEM and MIM. Then we collected key information such as program duration, credits, language requirements, admission documents, deadlines, and course structure.

After that, we designed the chatbot flow. The frontend was built as a chat interface where users can type questions or click suggested prompts. The backend receives the user message through `/api/chat`, sends it to the AI model with a strict system prompt, and returns a grounded answer.

The system prompt was important because it controls the chatbot's behavior. It tells the bot to act like a friendly study advisor, only answer based on known MEM/MIM facts, avoid inventing details, and remind users to verify official requirements.

We also added optional audio support. When ElevenLabs credentials are available, the backend can convert the bot answer into speech and send audio back to the browser.

For the voice feature, Raphael suggested using his videos from the HS Pforzheim video portal as the main voice source. The planned workflow is to download MP4 files, extract the audio channel, clean the speech samples, and use them only for the educational capstone demo.

## 6. Chatbot Knowledge Base

The chatbot includes information about:

- MEM: Engineering and Management M.Sc.
- MIM: Industrial Management M.Sc.
- Program duration and ECTS.
- Admission requirements.
- Application deadlines.
- Language requirements.
- Important documents.
- Course topics and semester structure.
- Differences between MEM and MIM.
- General application advice.

The bot is designed to answer carefully and avoid giving final admission decisions, because only Hochschule Pforzheim can officially decide admission results.

## 7. User Experience Design

The interface was designed to be simple, friendly, and easy to use. The chatbot page includes a professional color theme, message bubbles, quick suggestion buttons, and a clear input area.

The React prototype also includes an animated character that follows the pointer and reacts to clicks. This was added to make the chatbot feel more interactive and engaging during the presentation.

## 8. Testing and Improvements

We tested the chatbot using common student questions, such as:

- What is MEM?
- What is MIM?
- What are the application deadlines?
- What documents are required?
- What is the difference between MEM and MIM?
- Am I eligible for the program?

We also created a rule-based chatbot version for simple testing without needing an external AI API. This helps demonstrate the chatbot logic even if the AI service is unavailable.

## 9. Limitations

The current project is a prototype, so it has some limitations:

- It depends on external AI APIs for advanced answers.
- Voice output only works when ElevenLabs API credentials are configured.
- Admission information can change, so users must verify details on the official HS Pforzheim website.
- The chatbot can estimate applicant fit, but it cannot make official admission decisions.
- The knowledge base is focused mainly on MEM and MIM information.

## 10. Conclusion

The MEM & MIM Guide Bot shows how an AI chatbot can support students by answering repeated program and application questions in a fast and friendly way. The project combines a modern web interface, Python backend, AI response generation, optional voice output, and structured program knowledge.

Overall, the project demonstrates how generative AI can be used in education to improve access to information and make student advising more interactive.

## Suggested PPT Slide Structure

1. Title: MEM & MIM Guide Bot
2. Project Objective
3. Problem and Motivation
4. What We Built
5. Technologies Used
6. Chatbot Architecture
7. Key Features
8. Demo Questions
9. Limitations
10. Conclusion
