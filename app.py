from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

app = Flask(__name__)

# Use the same template as in main.py but keep reviews insertion flexible
template = """
you are an expert in aswering questions about a pizza restaurant.

Here are some relevant reviews:{reviews}
Given the reviews, answer the question: {question}

"""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="phi3")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Attempt to retrieve relevant reviews
    try:
        # vector.retriever may be either a retriever with get_relevant_documents or have invoke
        if hasattr(retriever, 'get_relevant_documents'):
            docs = retriever.get_relevant_documents(question)
        elif hasattr(retriever, 'invoke'):
            docs = retriever.invoke(question)
        else:
            docs = []
    except Exception as e:
        docs = []

    reviews_text = "\n---\n".join([d.page_content if hasattr(d, 'page_content') else str(d) for d in docs])

    # Build prompt and run the model
    inputs = {"reviews": reviews_text, "question": question}
    try:
        chain = prompt | model
        result = chain.invoke(inputs)
        # If result is a dict, try to get text
        if isinstance(result, dict) and 'output_text' in result:
            answer = result['output_text']
        else:
            answer = str(result)
    except Exception as e:
        return jsonify({'error': f'LLM error: {e}'}), 500

    return jsonify({'answer': answer, 'reviews': reviews_text})

if __name__ == '__main__':
    app.run(debug=True)
