from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import web_search
from tools import read_url
from tools import write_report
from config import Settings
from config import SYSTEM_PROMPT

llm = ...

tools = [write_report, web_search, read_url]

memory = MemorySaver()

model = ChatOpenAI(model=Settings.model_name, api_key=Settings.api_key)

agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=memory,
    system_prompt=SYSTEM_PROMPT
)

