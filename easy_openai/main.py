import argparse, utils
from openai import OpenAI


def call_llm(
    prompt_message, model_name, openai_api_key, temperature=0.8, return_cost=False
):
    """
    Create an instance of the OpenAI class and use it to generate completions.
    """
    # setup the OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # define llm function
    llm = (
        lambda content: client.chat.completions.create(
            model=model_name,
            temperature=temperature,
            messages=[{"role": "user", "content": content}],
        )
        .choices[0]
        .message.content
    )
    # return the output, either with or without the cost
    if return_cost:
        api_cost = utils.calculate_cost(model_name, prompt_message)
        return llm(prompt_message), api_cost

    return llm(prompt_message)


if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt_message",
        "-p",
        default="Who are you?",
        help="The prompt message to generate completions.",
    )
    parser.add_argument(
        "--model_name",
        "-m",
        default="gpt-4o",
        help="The model name to generate completions.",
    )
    parser.add_argument(
        "--openai_api_key", "-o", required=True, help="The OpenAI API key."
    )
    args = parser.parse_args()

    # Call the main function with the provided arguments
    prompt = args.prompt_message
    output = call_llm(prompt, args.model_name, args.openai_api_key)

    print(f"\nPrompt: {prompt}")
    print(f"Output with {args.model_name}:\n{output}\n")
