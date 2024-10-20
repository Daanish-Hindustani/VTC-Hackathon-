from langchain.agents import Tool
from langchain.agents.conversational.base import ConversationalAgent
from langchain.agents import AgentExecutor
from tools import tools
from datetime import datetime


class Agent():
    def __init__(self, llm) -> None:
        self.prefix = """
                You are a skilled recruiter for Valorant esports. Based on the input, use the tools to gather relevant data and construct a response.
                Leagues: "game-changers", "vct-international", "vct-challengers"
                Categories for query_tool: "leagues", "tournaments", "players", "teams"
                Use snake_case for query_key (e.g., first_name). You can query using query_value without a query_key.
                To condense data, provide important_fields (optional): a list of key fields to summarize; defaults to None.
                Ask follow-up questions if the input is unclear, and feel free to make general assumptions.
                PLS KEEP ANSWERS 50 word or less, be to the point.

                """
        self.ai_prefix = "Agent"
        self.human_prefix = "User"
        self.llm = llm
        self.agent = self.create_agent()

    def create_agent(self):
        agent = ConversationalAgent.from_llm_and_tools(
            llm=self.llm,
            tools=tools,
            prefix=self.prefix,
            ai_prefix=self.ai_prefix,
            human_prefix=self.human_prefix
        )
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True)
        return agent_executor

    def run(self, input):
        return self.agent.run(input=input)
    
