import os
import openai
import difflib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API key here (you can also set it as an environment variable)
openai.api_key = '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'

def calculate_similarity(text1, text2, scale=100):
    """
    Calculates the similarity between two texts using difflib.
    The scale determines the maximum similarity score (default is 100).
    """
    sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
    similarity_ratio = sequence_matcher.ratio()
    similarity_score = int(similarity_ratio * scale)  # Convert ratio to a scaled score
    print(similarity_ratio)
    return similarity_score


def determine_threshold(original_solution):
    """
    Determines the threshold based on the length of the original solution.
    """
    num_lines = len(original_solution.split('\n'))
    if num_lines <= 10:
        return 135
    else:
        return 120

def generate_feedback(submitted_answer, ai_generated_solution):
    """
    Generates feedback based on the submitted code and AI-generated solution.
    """
    prompt = (
        "Analyze the following submitted code and provide feedback on how it can be improved to avoid plagiarism. "
        "Consider changes to variable names, structure, and comments. "
        "Also, compare it with the AI-generated solution:\n\n"
        "Submitted Code:\n"
        f"{submitted_answer}\n\n"
        "AI-Generated Solution:\n"
        f"{ai_generated_solution}\n\n"
        "Provide detailed recommendations for making the submitted code unique and improving it."
    )
    response = openai.Completion.create(
        engine="gpt-4o-mini",  # You can choose the model here
        prompt=prompt,
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.7
    )
    feedback = response.choices[0].text.strip()
    return feedback


@app.route('/api/plagiarism_check', methods=['POST'])
def plagiarism_check():
    """
    This route handles the plagiarism check by comparing the submitted answer with the original solution
    and generating feedback using AI.
    """
    try:
        data = request.json
        submitted_answer = data['submitted_answer']
        original_solution = data['original_solution']
        question = data['question']

        # Step 1: Calculate similarity with original solution
        similarity_with_original = calculate_similarity(original_solution, submitted_answer)

        # Step 2: Generate AI solution based on the question
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose the model here
            prompt=f"Generate a solution for the following problem:\n\n{question}",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5
        )

        # Get the AI-generated solution
        ai_generated_solution = response.choices[0].text.strip()

        # Calculate similarity score between submitted_answer and AI-generated solution
        similarity_with_ai = calculate_similarity(submitted_answer, ai_generated_solution, scale=50)

        # Determine the threshold based on the original solution's length
        threshold = determine_threshold(original_solution)

        # Calculate the final result as the sum of both similarity scores
        final_result = similarity_with_original + similarity_with_ai

        # Generate feedback if plagiarism is detected
        if final_result >= threshold:
            feedback = generate_feedback(submitted_answer, ai_generated_solution)
            result = (
                f"The program is considered plagiarized. To avoid plagiarism, consider making the following changes: {feedback}"
            )
        else:
            result = "The program is not plagiarized and is ready for evaluation."

        # Return the response to the client
        return jsonify({
            "question": question,
            "submitted_answer": submitted_answer,
            "original_solution": original_solution,
            "ai_generated_solution": ai_generated_solution,
            "similarity_with_original": similarity_with_original,
            "similarity_with_ai": similarity_with_ai,
            "threshold": threshold,
            "final_result": final_result,
            "result": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)