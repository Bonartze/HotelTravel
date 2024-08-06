from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub

# Initialize the model (you may need a Hugging Face Hub account for online models)
llm = HuggingFaceHub.from_pretrained("gpt2")

# Create a LangChain with a simple prompt
chain = LLMChain(prompt="Tell me a story about a dragon.", llm=llm)

# Run the chain
result = chain.run()
print("Result:\n", result)
