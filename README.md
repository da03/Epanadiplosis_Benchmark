# Epanadiplosis Benchmark

Benchmarking the performance of various language models in generating [epanadiplosis](https://en.wiktionary.org/wiki/epanadiplosis), i.e., generating sentences that start with and end with the same word. Below is an example from Philippians 4:4:

```
Rejoice in the Lord always: and again I say, Rejoice.
```

Writing such sentences is quite trivial for human writers, yet large language models cannot reliably solve this task yet.

## Dependencies

Install the required dependencies with:

```
pip install -r requirements.txt
```

## Usage

First, make sure that your OpenAI API key is set as an environment variable `API_KEY`:

```
export AI_KEY="my_api_key"
```

Then, run the script using the following command:

```
python main.py --api_key ${API_KEY} --num_generations 100
```

## Results

| Model            | Success Rate↑  (%) | Repetitivenses↓  (%) |
|------------------|--------------------|----------------------|
| code-davinci-002 | 4                  | 63                   |
| text-davinci-002 | 18                 | 89                   |
| text-davinci-003 | 43                 | 67                   |
| gpt-3.5-turbo    | 22                 | 63                   |
| gpt-4            | 92                 | 98                   |

Evaluation metrics:

* Success rate: The proportion of generated sentences that demonstrate epanadiplosis (i.e., using the same word as both the first and last word in the sentence).
* Repetitiveness: The proportion of first words (counting from the second generation) that have been used in previous generations. For example, if all generated sentences start with the same word "Dreams", then this number will be 100%.

The raw generations corresponding to the above results are included in [evaluation_results.json](./evaluation_results.json) as part of the repo. Note that each run will result in different generations since we cannot set the random seed using the OpenAI API.

## Prompt

The prompt used to obtain the results in this benchmark is:

```
Write a sentence with at least 10 words that begins with and ends with the same word:
```

The requirement of "at least 10 words" helps ensure that the generated sentences are of a reasonable length. Without this constraint, some models tend to produce short and ungrammatical phrases.

## Acknolegements

This repository has been inspired by Yao Fu and Litu Ou's [Chain-of-Thought Hub: Measuring LLMs' Reasoning Performance](https://github.com/FranxYao/chain-of-thought-hub).
