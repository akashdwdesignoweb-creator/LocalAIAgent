from langchain_ollama import OllamaLLM        
from langchain_core.prompts import ChatPromptTemplate  
from vector import retriever  #importing the retriever from vector.py

model = OllamaLLM(model="phi3")          ##lightest model found on ollama

template= """
you are an expert in aswering questions about a pizza restaurant.

Here are some relevant reviews:{reviews}
Given the reviews, answer the question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)           #passing the template to the prompt
chain = prompt | model      #chaining the prompt with the model

while True:                                      #loop to keep asking questions
    print("\n\n ---------------------------------------------------------")
    question = input("What is your question? (q to quit): ")
    print("\n\n")
    if question.lower() == 'q':
        break
    reviews= retriever.invoke(question)          #retrieving relevant reviews from the db
    result = chain.invoke({"reviews":[], "question": question})     #passing the reviews and question to the chain
    print(result)

