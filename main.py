import json
# Print packages
import logging
import os
import warnings
from typing import Dict

from dotenv import load_dotenv
# Langchain Libraries
from langchain.agents import initialize_agent  # merge tools and llm
from langchain.agents import load_tools  # coordinate with wikipedia api
from langchain.agents.agent import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFaceHub  # Huggingface models repo

from openfabric_pysdk.context import Ray, State
from openfabric_pysdk.loader import ConfigClass
from openfabric_pysdk.utility import SchemaUtil

from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText

# Sets environment variables from .env file
load_dotenv()


############################################################
# Callback function called on update config
############################################################
def config(configuration: Dict[str, ConfigClass], state: State):
    # TODO Add code here
    pass


def get_model_state() -> AgentExecutor:
    # setup ReAct style agent with Huggingface model
    llm = HuggingFaceHub(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        model_kwargs={"temperature": 0.8},
    )  # Setting to zero minimises hallucinations
    tools = load_tools(["wikipedia"], llm=llm)  # Agent uses wikipedia
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        memory=memory,
        verbose=True,
    )
    return agent_chain


############################################################
# Callback function called on each execution pass
############################################################
def execute(request: SimpleText, ray: Ray, state: State) -> SimpleText:
    # Returns the agent response to user input
    output = []
    if not "agent_exec" in state.__dict__:
        # Only initialize agent first time `execute` is called
        agent_executor = get_model_state()
        setattr(state, "agent_exec", agent_executor)
        # logging.warning(f'{state.__dict__} SEtttttttttttttttttttttt')

    for text in request.text:
        # logging.warning(f'{state.__dict__} raisedxxx an error in his code')
        response = state.__dict__["agent_exec"].run({"input": text})
        output.append(response)

    return SchemaUtil.create(SimpleText(), dict(text=output))
