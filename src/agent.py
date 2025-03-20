from langchain_core.messages import SystemMessage
from pydantic import BaseModel
import os
# from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from langgraph.types import Send
from langgraph.checkpoint.memory import MemorySaver
from console import AgentConsole

from schemas import *
from prompts import *
from web_client import WebClient

import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI()
reasoning_llm = ChatOpenAI()

def build_first_queries(state: ReportState): 
    class QueryList(BaseModel):
        queries: List[str]
        
    user_input = state.user_input

    prompt = build_queries.format(user_input=user_input)
    query_llm = llm.with_structured_output(QueryList)
    result = query_llm.invoke(prompt)

    return {"queries": result.queries}

def spawn_researchers(state: ReportState):
    return [Send("single_search", query) 
            for query in state.queries]

def single_search(query: str):
    web_client = WebClient()

    results = web_client.search(query,max_results=1)

    query_results = []
    for result in results:
        url = result["link"]
        url_extraction = web_client.extract(url)

        # print(url_extraction)
        if len(url_extraction["results"]) > 0:
            raw_content = url_extraction["results"][0]["raw_content"]
            prompt = resume_search.format(user_input=console.user_input,
                                        search_results=raw_content)

            llm_result = llm.invoke(prompt)
            query_results += [QueryResult(title=result["title"],
                                    url=url,
                                    resume=llm_result.content)]
    return {"queries_results": query_results}
    

def final_writer(state: ReportState):
    search_results = ""
    references = ""
    for i, result in enumerate(state.queries_results):
        search_results += f"[{i+1}]\n\n"
        search_results += f"Title: {result.title}\n"
        search_results += f"URL: {result.url}\n"
        search_results += f"Content: {result.resume}\n"
        search_results += f"================\n\n"

        references += f"[{i+1}] - [{result.title}]({result.url})\n"
    

    prompt = build_final_response.format(user_input=console.user_input,
                                    search_results=search_results)

  
    llm_result = reasoning_llm.invoke(prompt)
    final_response = llm_result.content + "\n\n References:\n" + references

    return {"final_response": final_response}


builder = StateGraph(ReportState)
builder.add_node("build_first_queries", build_first_queries)
builder.add_node("single_search", single_search)
builder.add_node("final_writer", final_writer)

builder.add_edge(START, "build_first_queries")
builder.add_conditional_edges("build_first_queries", 
                              spawn_researchers, 
                              ["single_search"])
builder.add_edge("single_search", "final_writer")
builder.add_edge("final_writer", END) 

graph = builder.compile()

if __name__ == "__main__":
    console = AgentConsole(graph)
    console.run()