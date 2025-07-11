import cohere
import os

COHERE_API_KEY = os.getenv('COHERE_API_KEY', 'your-cohere-api-key-here')
co = cohere.Client(COHERE_API_KEY)

# All Cohere API calls use command-light model

def cohere_generate(prompt, task):
    # Truncate prompt to avoid exceeding Cohere's token limit (max 4081 tokens)
    max_chars = 10000  # ~3500 tokens
    if len(prompt) > max_chars:
        prompt = prompt[:max_chars]
    response = co.generate(
        prompt=prompt,
        max_tokens=512,
        temperature=0.3
    )
    return response.generations[0].text.strip()

# Argument Mining
def argument_mining(text):
    prompt = f"Extract arguments from the following legal text and list them clearly.\n\nText:\n{text}\n\nArguments:" 
    return cohere_generate(prompt, "argument_mining")

# Entity & Relationship Mapping
def entity_relationship_mapping(text):
    prompt = f"Identify all legal entities and their relationships in the following text.\n\nText:\n{text}\n\nEntities and Relationships:"
    return cohere_generate(prompt, "entity_relationship_mapping")

# Clause Explanation
def clause_explanation(text):
    prompt = f"Explain the following legal clause in simple terms.\n\nClause:\n{text}\n\nExplanation:"
    return cohere_generate(prompt, "clause_explanation")

# Summarization
def summarization(text):
    prompt = f"Summarize the following legal text.\n\nText:\n{text}\n\nSummary:"
    return cohere_generate(prompt, "summarization")

# Legal Chatbot
def legal_chatbot(question, context=None):
    prompt = f"You are a legal assistant. Answer the following question based on the context.\n\nContext:\n{context or ''}\n\nQuestion: {question}\n\nAnswer:"
    return cohere_generate(prompt, "legal_chatbot")

# Strategy Suggestions
def strategy_suggestions(text):
    prompt = f"Suggest legal strategies based on the following case details.\n\nCase Details:\n{text}\n\nStrategies:"
    return cohere_generate(prompt, "strategy_suggestions")

# Risk Prediction (returns a risk score and explanation)
def risk_prediction(text):
    prompt = f"Analyze the following legal case and predict the risk involved. Provide a risk score (0-100) and a brief explanation.\n\nCase:\n{text}\n\nRisk Score and Explanation:"
    return cohere_generate(prompt, "risk_prediction")
