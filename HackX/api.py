from flask import Blueprint, jsonify, request
from ai_model import calculate_similarity, determine_threshold

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/plagiarism_check', methods=['POST'])
def plagiarism_check():
    """Endpoint to check plagiarism based on similarity score."""
    data = request.get_json() or {}
    submitted_answer = data.get('submitted_answer', '')
    original_solution = data.get('original_solution', '')

    similarity = calculate_similarity(original_solution, submitted_answer)
    threshold = determine_threshold(original_solution)
    result = 'Plagiarized' if similarity >= threshold else 'Not Plagiarized'

    return jsonify({
        'similarity_with_original': similarity,
        'threshold': threshold,
        'result': result
    })
