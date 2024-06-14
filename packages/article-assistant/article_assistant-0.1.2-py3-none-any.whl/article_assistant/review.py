import os
from langchain_openai import ChatOpenAI
from agents.agent_utils import initialize_environment, agent_node
from agents.create_agents import create_agents
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage
from typing import Sequence, Annotated, TypedDict
import functools
import operator
from PyPDF2 import PdfReader


class Review:
    class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], operator.add]
        next: str

    def __init__(self):
        initialize_environment()
        self.graph = self.construct_graph()

    def create_supervisor_chain(self, llm):
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser

        members = ["SME_Reviewer", "SME_Search"]
        system_prompt = (
            "You are a lead reviewer tasked with managing a conversation between the"
            " following workers: {members}. Given the following user request,"
            " respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status. When finished,"
            " respond with FINISH."
            " Summarize the findings from both SME_Reviewer and SME_Search into a single paragraph."
        )
        options = ["FINISH"] + members
        function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {
                "title": "routeSchema",
                "type": "object",
                "properties": {
                    "next": {
                        "title": "Next",
                        "anyOf": [
                            {"enum": options},
                        ],
                    }
                },
                "required": ["next"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?"
                    " Or should we FINISH? Select one of: {options}",
                ),
            ]
        ).partial(options=str(options), members=", ".join(members))

        supervisor_chain = (
            prompt
            | llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
        )

        return supervisor_chain

    def construct_graph(self):
        review_agent, search_agent = create_agents()

        review_node = functools.partial(agent_node, agent=review_agent, name="SME_Reviewer")
        search_node = functools.partial(agent_node, agent=search_agent, name="SME_Search")

        workflow = StateGraph(self.AgentState)
        workflow.add_node("SME_Reviewer", review_node)
        workflow.add_node("SME_Search", search_node)

        llm = ChatOpenAI(model="gpt-4-1106-preview")
        supervisor_chain = self.create_supervisor_chain(llm)
        workflow.add_node("supervisor", supervisor_chain)

        members = ["SME_Reviewer", "SME_Search"]
        for member in members:
            workflow.add_edge(member, "supervisor")

        conditional_map = {k: k for k in members}
        conditional_map["FINISH"] = END
        workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)

        workflow.set_entry_point("supervisor")

        return workflow.compile()

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    def review_article(self, pdf_path):
        paper_text = self.extract_text_from_pdf(pdf_path)
        human_message = HumanMessage(content=paper_text)

        agent_outputs = {"SME_Reviewer": [], "SME_Search": [], "Lead_Reviewer": []}

        for s in self.graph.stream({"messages": [human_message]}):
            print("Graph stream output:", s)  # Debugging line
            if "__end__" not in s:
                # Collect and print the outputs from the agents
                if "SME_Reviewer" in s:
                    print("SME_Reviewer invoked")  # Debugging line
                    agent_outputs["SME_Reviewer"].append(s["SME_Reviewer"]["messages"][0].content)

                if "SME_Search" in s:
                    print("SME_Search invoked")  # Debugging line
                    agent_outputs["SME_Search"].append(s["SME_Search"]["messages"][0].content)

                if "supervisor" in s:
                    print("Supervisor invoked")  # Debugging line
                    agent_outputs["Lead_Reviewer"].append(s["supervisor"]["next"])

                print(s)
                print("----")

        # Summarize findings
        findings_summary = self.summarize_findings(agent_outputs)

        # Print the collected outputs
        print("\nSME_Reviewer Outputs:")
        for output in agent_outputs["SME_Reviewer"]:
            print(output)

        print("\nSME_Search Outputs:")
        for output in agent_outputs["SME_Search"]:
            print(output)

        print("\nLead_Reviewer Outputs:")
        for output in agent_outputs["Lead_Reviewer"]:
            print(output)

        print("\nSummary by Lead Reviewer:")
        print(findings_summary)

        return {
            "summary": findings_summary,
            "sme_reviewer": agent_outputs["SME_Reviewer"],
            "sme_search": agent_outputs["SME_Search"],
        }

    def summarize_findings(self, agent_outputs):
        llm = ChatOpenAI(model="gpt-4-1106-preview")
        prompt = (
            "Summarize the following findings into a single paragraph. Ensure that the summary is clear and cohesive.\n\n"
            "SME_Reviewer findings:\n" + "\n".join(agent_outputs["SME_Reviewer"]) + "\n\n"
            "SME_Search findings:\n" + "\n".join(agent_outputs["SME_Search"])
        )
        summary = llm.invoke([HumanMessage(content=prompt)]).content
        return summary
