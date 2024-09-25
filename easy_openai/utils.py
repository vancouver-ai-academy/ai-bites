import tiktoken

# Example pricing (replace with the actual prices from OpenAI)
price_per_1k_tokens = {
    'gpt-4o': 0.005,  # $0.005 per 1K tokens
}

def calculate_cost(model, text):
    # Initialize tiktoken encoding for the specified model
    encoding = tiktoken.encoding_for_model(model)

    # Encode the text to count tokens
    tokens = encoding.encode(text)
    num_tokens = len(tokens)

    # Calculate the cost based on the number of tokens and price per 1K tokens
    cost = (num_tokens / 1000) * price_per_1k_tokens[model]
    
    return cost