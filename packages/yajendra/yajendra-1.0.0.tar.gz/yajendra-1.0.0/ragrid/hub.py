import pandas as pd
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from .tru_lens_evaluator import Chroma, TruLensEvaluator
from .text_chunker import TextChunker
from .document_extractor import DocumentExtractor
from .text_cleaner import TextCleaner
from .evaluation_question_generator import EvaluationQuestionGenerator
from dotenv import load_dotenv
from .library_exceptions import ApiKeyError
import os
from pprint import pprint

load_dotenv()


class ChunkEvaluator:
    """
    A class containing methods for evaluating chunking methods and determining the best parameters.
    """

    def __init__(self, file_path, **kwargs):
        """
        Initialize the ChunkEvaluator with the file path and optional parameters.

        Args:
            file_path (str): The path to the input file.
            **kwargs: Additional keyword arguments for configuring evaluation parameters.

        Raises:
            TypeError: If any parameter does not match the expected data type.
        """
        expected_types = {
            "number_of_questions": int,
            "chunk_size": int,
            "chunk_overlap": int,
            "separator": str,
            "strip_whitespace": bool,
            "sentence_buffer_window": int,
            "sentence_cutoff_percentile": int,
        }
        default_attributes = {
            "number_of_questions": 5,
            "chunk_size": 250,
            "chunk_overlap": 0,
            "separator": "",
            "strip_whitespace": False,
            "sentence_buffer_window": 3,
            "sentence_cutoff_percentile": 80,
        }
        default_attributes.update(kwargs)

        for key, value in default_attributes.items():
            expected_type = expected_types.get(key)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(f"{key} must be of type {expected_type.__name__}")
            setattr(self, key, value)

        self.file_path = file_path

    def __str__(self):
        return self.text

    def reset_params(self):
        """
        Reset the evaluation parameters to default values.

        Returns:
            dict: A dictionary containing the default evaluation parameters.
        """
        return {
            "chunk_size": "-",
            "chunk_overlap": "-",
            "separator": "-",
            "strip_whitespace": "-",
            "sentence_buffer_window": "-",
            "sentence_cutoff_percentile": "-",
        }

    def eval_function(self, chunks, method_name, eval_questions):
        """
        Evaluate the performance of a chunking method using the TruLens framework.

        Args:
            chunks (list): A list of Document objects representing chunks of text.
            method_name (str): The name of the chunking method being evaluated.
            eval_questions (list): A list of evaluation questions.

        Returns:
            float: The evaluation score.
        """
        try:
            embedding_function = SentenceTransformerEmbeddings(
                model_name="sentence-transformers/all-MiniLM-l6-v2"
            )

            db = Chroma.from_documents(chunks, embedding_function)
            score = TruLensEvaluator.trulens_evaluation(
                evaluation_questions=eval_questions,
                vectorstore=db,
                chunking_type=method_name,
            )
            return score

        except Exception as e:
            raise e 

    def rearrangeGrid(self,method_eval_score):
        selected_df_filtered = []
        param_list = [
            "chunk_size",
            "chunk_overlap",
            "separator",
            "strip_whitespace",
            "sentence_buffer_window",
            "sentence_cutoff_percentile",
        ]
        selected_columns = [
            "app_id",
            "input",
            "output",
            "Answer Relevance",
            "Context Relevance",
            "Groundedness",
        ]
        selected_columns.extend(param_list)
        for df in method_eval_score:
            selected_df = df[[col for col in selected_columns if col in df.columns]]
            selected_df_filtered.append(selected_df)
        merged_df = pd.concat(selected_df_filtered, ignore_index=True)
        groupby_columns = ["app_id"] + param_list
        grouped_df = (
            merged_df.groupby(groupby_columns)[
                ["Answer Relevance", "Context Relevance", "Groundedness"]
            ]
            .mean()
            .reset_index()
        )
        grouped_df.columns = ['Chunking Method','Chunk Size','Chunk Overlap','Separator','Strip Whitespace','Sentence Buffer Window',
                              'Window Cutoff Percentile',"Answer Relevance", "Context Relevance", "Groundedness"]
        
        
        return grouped_df
    

    def evaluateResult(self,df):

        df['Average'] = df[['Answer Relevance', 'Context Relevance', 'Groundedness']].mean(axis=1)
        sorted_df = df.sort_values(by='Average', ascending=False)
        return sorted_df['Chunking Method'].head(1)

    def evaluate_and_format_result(self,grouped_df):
        evaluation_matrix = "\n\nThe Evaluation matrix is:\n\n{}".format(grouped_df.to_string(index=False))
        best_chunking_method = "\n\nThe Best chunking method with respect to current parameters is:{}".format(self.evaluateResult(grouped_df).to_string(index=False))
        return evaluation_matrix, best_chunking_method

    
    #*************************Main Function************************
    #*****************************************************************
    def evaluate_parameters(self):
        """
        Determine the best parameters for the chunking method based on performance evaluation.

        Returns:
            pandas.DataFrame: A DataFrame containing the best parameters and their corresponding evaluation scores.
        """
        if 'OPENAI_API_KEY' not in os.environ:
            raise ApiKeyError()
        # Create an instance of DocumentExtractor to extract data from the file
        extractor_instance = DocumentExtractor(
            file_path=self.file_path, parent_instance=self
        )
        # Extract uncleaned text data using the extractor_instance
        uncleaned_text = extractor_instance.extract_data()

        # Create an instance of TextCleaner to clean the unstructured text
        cleaner_instance = TextCleaner(
            uncleaned_text=uncleaned_text, parent_instance=self
        )
        # Clean the unstructured text using the cleaner_instance
        cleaned_text = cleaner_instance.clean_text()

        # Generate evaluation questions using EvaluationQuestionGenerator
        # based on the cleaned text and the specified number of questions
 
        eval_questions = EvaluationQuestionGenerator(
            document=cleaned_text, number_of_questions=self.number_of_questions
        ).get_evaluation_questions()
        

        # Get a list of methods from the TextChunker class that are callable and not private
        methods_list = [
            method
            for method in dir(TextChunker)
            if callable(getattr(TextChunker, method)) and not method.startswith("__")
        ]

        # Create an instance of TextChunker with the cleaned text and parent instance
        chunk_text = TextChunker(clean_text=cleaned_text, parent_instance=self)

        # Initialize an empty list to store evaluation scores for each method
        method_eval_score = []

        # Iterate through the methods in the methods_list
        for method_name in methods_list:

            # Get the method from the chunk_instance by its name
            method = getattr(chunk_text, method_name, None)

            # Check if the method exists
            if method:
                # Call the method to get chunks and parameters
                chunks, params = method()

                # Evaluate the performance of the method using TruLens framework
                model_results = self.eval_function(
                    chunks=chunks,
                    method_name=method_name,
                    eval_questions=eval_questions,
                )
                # Create a DataFrame containing the parameters
                params_df = pd.DataFrame([params])
                # Repeat the parameters DataFrame for each model result
                repeated_params_df = pd.concat(
                    [params_df] * len(model_results), ignore_index=True
                )

                out = pd.concat([model_results, repeated_params_df], axis=1)
                method_eval_score.append(out)
                
        evaluation_matrix, best_chunking_method = self.evaluate_and_format_result(self.rearrangeGrid(method_eval_score)) 

        return "{}{}".format(evaluation_matrix, best_chunking_method)   
            
    
