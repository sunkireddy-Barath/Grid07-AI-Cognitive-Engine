import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

load_dotenv()
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")

@tool
def mock_searxng_search(query: str) -> str:
    """Mock search tool."""
    q = query.lower()
    if "crypto" in q or "bitcoin" in q:
        return "Bitcoin hits new all-time high amid regulatory ETF approvals"
    if "ai" in q or "openai" in q or "model" in q:
        return "OpenAI releases GPT-5, sparks debate about developer job security"
    if "finance" in q or "market" in q or "rate" in q:
        return "Federal Reserve signals two more rate cuts before year end"
    return "Tech stocks surge as AI investment hits record highs"

class AgentState(TypedDict):
    bot_id: str
    persona: str
    search_query: str
    search_result: str
    post_content: str

def decide_search(state):
    prompt = f"Persona: {state['persona']}\nPick a 5-word search topic for today's post."
    state["search_query"] = llm.invoke(prompt).content.strip()
    return state

def web_search(state):
    state["search_result"] = mock_searxng_search.invoke(state["search_query"])
    return state

def draft_post(state):
    prompt = f"""Persona: {state['persona']}
News: {state["search_result"]}
Write a <280 char tweet based on this.
Reply ONLY with this JSON: {{"bot_id": "{state['bot_id']}", "topic": "...", "post_content": "..."}}"""
    state["post_content"] = llm.invoke(prompt).content.strip()
    return state

builder = StateGraph(AgentState)
builder.add_node("decide_search", decide_search)
builder.add_node("web_search", web_search)
builder.add_node("draft_post", draft_post)
builder.add_edge(START, "decide_search")
builder.add_edge("decide_search", "web_search")
builder.add_edge("web_search", "draft_post")
builder.add_edge("draft_post", END)
graph = builder.compile()

if __name__ == "__main__":
    init = {"bot_id": "Bot_A", "persona": "Optimistic tech bot.", "search_query": "", "search_result": "", "post_content": ""}
    print("Graph Output:", graph.invoke(init)["post_content"])
