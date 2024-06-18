from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from ragrid.library_exceptions import (
    IncorrectQuestionGeneration,
    InvalidAPIKey,
    FreeTierNotAllowed,
)
# from testpackage.document_extractor import DocumentExtractor
from langchain_openai import OpenAI

class EvaluationQuestionGenerator:
    """
    A class to generate questions from a given text using an LLM.
    """

    def __init__(self, document: str, number_of_questions: int):
        self.document = document
        self.number_of_questions = number_of_questions

    def get_evaluation_questions(self) -> list:
        """
        Generate evaluation questions from the given document.

        Returns:
            list: A list of generated evaluation questions.

        Raises:
            QuestionGenerationError: If an error occurs during question generation,
                                     including invalid OpenAI API key.
        """

        try:
            # template = """
            # You are an expert in analysing and finding questions for an assessment.
            # You will be provided with the document, and you need to generate {num_of_questions} question from the document.
            # The answer of the question so generated should be maximum 15-20 words only and directly available in the document.

            # Document: {content}
            # Questions:
            # """
            

            for i in range(4):
                llm = OpenAI()
                llm.invoke('0+1')
            

            template = """
            Here is a passage of text: \n{content}\n Generate a list of {num_of_questions} questions that cover a range of answer lengths, including short, medium, and long answers. Ensure that the questions are diverse and cover various aspects of the text. Don't add the length after questions"
            """
            prompt = PromptTemplate(
                input_variables=["num_of_questions", "content"],
                template=template,
            )

            chain = LLMChain(
                llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0), prompt=prompt
            )

            response = chain.invoke(
                {"num_of_questions": self.number_of_questions, "content": self.document}
            )

            questions_text = response["text"]
            questions_list = questions_text.split("\n")
            questions_list_formatted = [
                question.split(". ", 1)[1] if ". " in question else question
                for question in questions_list
            ]
            try:
                if len(questions_list_formatted) == self.number_of_questions:
                    return questions_list_formatted
            except:
                raise IncorrectQuestionGeneration()

        except Exception as e:
            if e.status_code == 401:
                raise InvalidAPIKey()
            if e.status_code == 429:
                raise FreeTierNotAllowed()
            else:
                raise (f"OpenAI API Error: {e}")
