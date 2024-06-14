from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from .agent_utils import create_agent

def create_agents():
    llm = ChatOpenAI(model="gpt-4-1106-preview")

    tavily_tool = TavilySearchResults(max_results=5)
    python_repl_tool = PythonREPLTool()

    review_agent = create_agent(
        llm,
        [python_repl_tool],
        """
        You are a subject matter expert reviewing an article. You may use Python code to analyze data. 
        You will generate a recommendation for the writer about their article.
        """
    )
    search_agent = create_agent(
        llm,
        [tavily_tool],
        """You are a subject matter expert who searches the internet to find relevant articles.
         Search the internet about the users topic and description.
         Find similar articles, and use those to and make recommendations about the users article."""
    )

    # print("Review Agent and Search Agent created successfully")
    # print("Tavily Tool:", tavily_tool)
    # print("Python REPL Tool:", python_repl_tool)

    return review_agent, search_agent
