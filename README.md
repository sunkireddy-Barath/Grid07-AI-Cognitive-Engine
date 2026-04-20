# Grid07 AI Cognitive Engine

## Setup
- Step 1: Clone the repository to your local machine.
- Step 2: Run `pip install -r requirements.txt` to install dependencies.
- Step 3: Copy `.env.example` to `.env` and add your Groq API key.
- Step 4: Execute the project by running `python main.py`.

## Phase 1: Vector Routing
Cosine similarity is a mathematical measure used to determine how similar two pieces of text are by comparing their vector orientations. In this project, the FAISS index stores the bot personas as high-dimensional vectors for extremely fast retrieval. We use a threshold of 0.85 to ensure that only bots with a meaningful connection to the post content are selected to respond.

## Phase 2: LangGraph Node Structure
[START] → [decide_search] → [web_search] → [draft_post] → [END]

- **decide_search**: The bot analyzes its persona and picks a 5-word search topic.
- **web_search**: A mock search tool retrieves recent news based on the chosen topic.
- **draft_post**: The LLM writes a short, opinionated tweet based on the news and persona.

The TypedDict state carries the bot ID, persona, search queries, results, and the final post content between every node in the graph.

## Phase 3: RAG + Prompt Injection Defense
In this project, RAG uses the previous thread history as context to keep the conversation grounded. The full conversation history and the original post are injected directly into the user prompt for the LLM. The system prompt defends against injection by establishing immutable rules that force the bot to ignore any instructions hidden in user messages. Even if a bot receives an "ignore previous instructions" attack, it will stay in character and continue the debate naturally.

## Tech Stack
Python, LangGraph, LangChain, Groq API, sentence-transformers, FAISS
