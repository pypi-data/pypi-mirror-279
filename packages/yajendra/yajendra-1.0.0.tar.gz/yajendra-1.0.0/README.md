
---

# Ragrid Library

## Overview

Ragrid is a comprehensive library designed to optimize Retrieval-Augmented Generation (RAG) processes. It provides a suite of tools to automatically determine the best parameters for processing specific documents. This includes selecting appropriate chunking techniques, embedding models, vector databases, and Language Model (LLM) configurations.

## Why ragrid ?

Ragrid is a powerful and user-friendly library that empowers researchers and developers to achieve state-of-the-art performance in their RAG workflows. By automating parameter selection, offering a range of intelligent chunking methods, and ensuring seamless compatibility, Ragrid simplifies the RAG process and unlocks its full potential.  If you're looking to streamline your RAG development and achieve optimal results, Ragrid is the perfect library to elevate your Gen AI projects.

## Why we are best?

Ragrid revolutionizes the process of Retrieval-Augmented Generation (RAG) by offering unparalleled efficiency and optimization. With its adaptive chunking capability, Ragrid intelligently selects the most suitable chunking method for each document, ensuring superior performance across diverse datasets. Ragrid eliminates the need for tedious manual best configuration selection, allowing researchers and developers to focus on the core aspects of their Gen AI projects. Moreover, its commitment to continuous improvement ensures that Ragrid remains at the forefront of RAG technology, making it the ultimate choice for streamlining RAG workflows and achieving optimal results in Gen AI tasks.

### Key Features:
- **Adaptive Chunking:** Incorporates four advanced text chunking methodologies to enhance the handling of diverse document structures.
  - Specific Text Splitting
  - Recursive Text Splitting
  - Sentence Window Splitting
  - Semantic Window Splitting
- **Expandability:** Future versions will introduce additional chunking strategies and enhancements based on user feedback and ongoing research.
- **Compatibility:** Designed to seamlessly integrate with a wide range of embedding models and vector databases.

## Getting Started

#### Supported Python versions >= 3.9 and <= 3.11 

### Installation

To get started, install the ragrid library using the following command:

```bash
pip install ragrid
```

To verify the installation and view library details, execute:

```bash
pip show ragrid
```

### Setting Up Your Environment

Before diving into the functionality of ragrid, ensure that your environment variables are properly configured with your OpenAI API key and your Hugging Face token:

```python
import os

os.environ['OPENAI_API_KEY'] = "YOUR_OPENAI_API_KEY"

```
#### Note :- API Key from Free tier OpenAI account is not supported.  
## Usage

The following steps guide you through the process of utilizing the ragrid library to optimize your RAG parameters:

```python
import ragrid as rg

# Specify the path to your PDF document
file_path = "PATH_TO_YOUR_PDF_FILE"

# Initialize the RAG-X instance
model = rg.ChunkEvaluator(file_path)

# Generate the optimal RAG parameters for your document
score_card = model.evaluate_parameters()

# Output the results
print(score_card)
```


## Set parameters for evaluation

If you wish to analyse the performance of your parameters, you can pass the parameters as below:
```python
kwarg = {
        'number_of_questions': 5, # Number of questions used to evaluate the process: type(int)
        'chunk_size': 250, # Chunk size: type(int)
        'chunk_overlap': 0, # Chunk overlap size: type(int)
        'separator': '',  # Separator to be used for chunking if any, type(str)
        'strip_whitespace': False, # Strip white space, type(bool)
        'sentence_buffer_window': 3, # Sentence Buffer window, type(int) 
        'sentence_cutoff_percentile': 80, # Sentence chunk split percentile for spliting context, type(int), range(1,100)
        }

# Specify the path to your PDF document
file_path = "PATH_TO_YOUR_PDF_FILE"

# Initialize the ragrid instance
model = rg.ChunkEvaluator(file_path, **kwargs)

# Generate the optimal RAG parameters for your document
score_card = model.evaluate_parameters()

# Output the results, output will be a pandas dataframe
print(score_card)
```

## Contribution
We are open for contributions and any feedback from the users. Feel free to contact us.

## Contact Us:
If you wish to integarte GenAI into your company, please contact us.

## Struggling to implement Gen AI in your company or product? 
Book a call at https://topmate.io/deepakchawla1307
