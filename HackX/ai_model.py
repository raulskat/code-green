import os
import cohere
import difflib
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request #, request, jsonify

# Loading the API key from the .env file
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

app = Flask(__name__)

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
@app.route('/api/plagiarism_check', methods=['POST'])
def plagiarism_check():
    """
    API to check for plagiarism and generate feedback.
    """
    try:
        data = request.json
        submitted_answer = data.get('submitted_answer', '')
        original_solution = data.get('original_solution', '')
        question = data.get('question', '')

        # Step 1: Calculate similarity with original solution
        similarity_with_original = calculate_similarity(original_solution, submitted_answer)

        # Step 2: Generate AI solution based on the question
        # try:
        #     ai_response = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "system", "content": "You are an expert coder who generates solutions to programming problems."},
        #             {"role": "user", "content": f"Generate a solution for the following problem:\n\n{question}"}
        #         ],
        #         max_tokens=250,
        #         temperature=0.7
        #     )
        #     ai_generated_solution = ai_response['choices'][0]['message']['content'].strip()
        # except openai.error.OpenAIError as e:
        #     return jsonify({"error": f"Error generating AI solution: {str(e)}"}), 500

        # Step 3: Calculate similarity with AI-generated solution
        # similarity_with_ai = calculate_similarity(submitted_answer, ai_generated_solution, scale=50)

        # Step 4: Determine the threshold
        threshold = determine_threshold(original_solution)

        # Step 5: Calculate the final score
        # final_result = similarity_with_original + similarity_with_ai

        # # Step 6: Generate feedback if plagiarism detected
        # feedback = generate_feedback(submitted_answer, ai_generated_solution) if final_result >= threshold else "No plagiarism detected."

        # Return the response
        # return jsonify({
        #     "question": question,
        #     "submitted_answer": submitted_answer,
        #     "original_solution": original_solution,
        #     "ai_generated_solution": ai_generated_solution,
        #     "similarity_with_original": similarity_with_original,
        #     "similarity_with_ai": similarity_with_ai,
        #     "threshold": threshold,
        #     "final_result": final_result,
        #     "feedback": feedback,
        #     "result": "Plagiarized" if final_result >= threshold else "Not Plagiarized"
        # }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
