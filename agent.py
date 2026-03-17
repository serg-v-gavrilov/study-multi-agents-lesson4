from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import web_search
from tools import read_url
from tools import write_report
from config import Settings
from config import SYSTEM_PROMPT

tools = [write_report, web_search, read_url]

memory = MemorySaver()

model = ChatOpenAI(model=Settings.model_name, api_key=Settings.api_key, temperature=0)

agent = create_react_agent(
    model=model,
    tools=tools,
    checkpointer=memory,
    prompt=SYSTEM_PROMPT
)

