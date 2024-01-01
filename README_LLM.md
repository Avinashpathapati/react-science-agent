
# Approach

The agent is built using Langchain package. I used Mistral AI LLM Model "mistralai/Mixtral-8x7B-Instruct-v0.1" from Huggingface. Any "Text-Generation task" LLMs from the Huggingface can be used. I have not used any LLM apis like OpenAI(I know this is not a scalable approach) as mentioned. 

To specifically built agent that can master scientific questions, I used "ReAct" style agent. In short, it is called "Reason+Act" agent. Instead of providing the answer directly by itself, the agent first tries to generate multiple possible queries for the user question and fires those queries to the APIs we configured. In this case, I used wikipedia API. In the second step, it generates the summary from the possible answers it got from the first step. In the worst case, If there is no information from the first step, the agent provides the answer directly. Because it uses external tools like Wikipedia to understand and provide information, it can provide quality answers. Also we can easily add more external tools that the agent can use to provide more high quality answers. For example, to provide more sophisticated answers to math questions, we can configure Wolfram Alpha API. 

##
More information on ReAct agent is found in https://arxiv.org/abs/2210.03629

# Packages to install and How to run
pip install -U langchain
pip install -U huggingface_hub
pip install python-dotenv
pip install wikipedia

# RUN

The execute API returns the chatbot response to the question. Note that HUGGINGFACEHUB_API_TOKEN should be set in .env file in this repo. This token is required to access any model from the HuggingfaceHub. "load_dotenv()" automatically sets environment variables from .env file

