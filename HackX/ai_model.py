import os
import difflib
import cohere
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

# Loading the API key from the .env file
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

def calculate_similarity(text1, text2, scale=100):
    """
    Calculates the similarity between two texts using difflib.
    The scale determines the maximum similarity score (default is 100).
    """
    sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
    similarity_ratio = sequence_matcher.ratio()
    similarity_score = int(similarity_ratio * scale)  # Convert ratio to a scaled score
    return similarity_score

def determine_threshold(original_solution):
    """
    Determines the threshold based on the length of the original solution.
    """
    num_lines = len(original_solution.split('\n'))
    return 135 if num_lines <= 10 else 120

import difflib

def generate_feedback(submitted_answer, ai_generated_solution):
    """
    Generates feedback based on the submitted code and AI-generated solution.
    """
    # Calculate similarity ratio
    similarity_ratio = difflib.SequenceMatcher(None, submitted_answer, ai_generated_solution).ratio()

    prompt = (
        "You are an expert in analyzing code and providing recommendations to improve its uniqueness and avoid plagiarism.\n\n"
        f"Submitted Code:\n{submitted_answer}\n\n"
        f"AI-Generated Solution:\n{ai_generated_solution}\n\n"
        f"Similarity Ratio: {similarity_ratio:.2f}\n\n"
        "Compare the submitted code with the AI-generated solution and provide bullet points in less than 100 words for making the submitted code unique and improving it."
    )

    try:
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=250,
            temperature=0.7
        )
        feedback = response.generations[0].text.strip()
        return feedback
    except cohere.CohereError as e:
        # This will handle any Cohere-related errors (rate limit, invalid key, etc.)
        feedback = f"Error generating feedback: {str(e)}"
        return feedback
