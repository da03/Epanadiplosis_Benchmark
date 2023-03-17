"""
Author: Yuntian Deng (dengyuntian@seas.harvard.edu)
This code was generated with the help of GPT-4.

This script evaluates different language models' ability to generate sentences
that demonstrate epanadiplosis, a rhetorical device where the first and last words
of a sentence are the same.
"""

import json
import argparse
import random
import string

import openai

def generate_epanadiplosis(model_name, prompt, temperature=0.7, max_tokens=50):
    """
    Generate an epanadiplosis sentence using the specified language model.

    Args:
        model_name (str): The name of the language model to use.
        prompt (str): The prompt for generating the sentence.
        temperature (float, optional): Sampling temperature for the model. Defaults to 0.7.
        max_tokens (int, optional): Maximum number of tokens in the generated sentence. Defaults to 50.

    Returns:
        str: The generated sentence.
    """
    if model_name == "gpt-3.5-turbo" or model_name == "gpt-4":
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        generated_text = response.choices[0].message.content.strip()
    else:
        response = openai.Completion.create(
            model=model_name,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        generated_text = response.choices[0].text.strip()
    return generated_text

def is_epanadiplosis(sentence):
    """
    Determine if the given sentence demonstrates epanadiplosis.

    Args:
        sentence (str): The sentence to evaluate.

    Returns:
        bool: True if the sentence demonstrates epanadiplosis, False otherwise.
    """
    words = sentence.strip().split()
    first_word = words[0].lower().strip(string.punctuation)
    last_word = words[-1].lower().strip(string.punctuation)
    return first_word == last_word

def evaluate_models(models, prompt, temperature, max_tokens, num_generations):
    """
    Evaluate the specified language models on their ability to generate epanadiplosis sentences.

    Args:
        models (list): List of language models to evaluate.
        prompt (str): The prompt for generating sentences.
        temperature (float): Sampling temperature for the model.
        max_tokens (int): Maximum number of tokens in the generated sentence.
        num_generations (int): The number of sentences to generate per model.

    Returns:
        dict: A dictionary containing evaluation results for each model.
    """
    results = {}
    for model in models:
        success_count = 0
        unique_first_words = 0
        model_results = {
            "prompt": prompt,
            "generations": []
        }
        first_words = set([])

        for _ in range(num_generations):
            generated_sentence = generate_epanadiplosis(model, prompt, temperature)
            success = is_epanadiplosis(generated_sentence)
            first_word = generated_sentence.strip().split()[0].lower().strip(string.punctuation)
            if first_word not in first_words:
                unique_first_words += 1
                first_words.add(first_word)
            if success:
                success_count += 1

            model_results["generations"].append({
                "sentence": generated_sentence,
                "is_epanadiplosis": success
            })

        success_rate = success_count / num_generations
        model_results["success_rate"] = success_rate
        diversity_rate = unique_first_words / num_generations
        model_results["diversity"] = diversity_rate
        results[model] = model_results
        print (f'Model: {model}. Success rate: {success_rate} ({success_count} out of {num_generations}). Diversity: {diversity_rate} ({unique_first_words} out of {num_generations})')

    return results


def parse_arguments():
    """
    Parse command-line arguments using argparse.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Evaluate language models on epanadiplosis generation.")
    parser.add_argument("--api_key", type=str, required=True, help="OpenAI API key")
    parser.add_argument("--models", nargs="+", default=["code-davinci-002", "text-davinci-002", "text-davinci-003", "gpt-3.5-turbo", "gpt-4"], help="List of models to evaluate")
    parser.add_argument("--num_generations", type=int, default=5, help="Number of generations per model")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation")
    parser.add_argument("--max_tokens", type=int, default=50, help="Maximum number of tokens in the generated sentence")
    parser.add_argument("--prompt", type=str, default="Write a sentence with at least 10 words that begins with and ends with the same word:", help="Prompt for generating epanadiplosis sentences")
    parser.add_argument("--output", type=str, default="evaluation_results.json", help="Output file path for the evaluation results")
    return parser.parse_args()

def save_results_to_file(results, output_file):
    """
    Save the evaluation results to a specified file.

    Args:
        results (dict): The evaluation results to save.
        output_file (str): The file path to save the results.
    """
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    args = parse_arguments()
    openai.api_key = args.api_key
    evaluation_results = evaluate_models(args.models, args.prompt, args.temperature, args.max_tokens, args.num_generations)
    save_results_to_file(evaluation_results, args.output)
