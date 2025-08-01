from flask import Flask, render_template, request, redirect, url_for, jsonify
from rule_model import plagiarism_detection
from ai_model import calculate_similarity, generate_feedback
from api import api_bp
import urllib.parse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(api_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        # Step 1: Get the form data from the user
        submitted_code = request.form['code']
        original_code = request.form['original_code']
        question = request.form['question']
        logger.info("Received code submission for question: %s", question)

        # Step 2: Pass the data to rule_model for boolean values
        exact_match, variable_renaming, structural_similarity = plagiarism_detection(original_code, submitted_code)

        # Step 3: Pass the data to ai_model for similarity score
        similarity_score = calculate_similarity(original_code, submitted_code)
        logger.info(
            "Plagiarism check results - similarity: %s, exact_match: %s, variable_renaming: %s, structural_similarity: %s",
            similarity_score,
            exact_match,
            variable_renaming,
            structural_similarity,
        )

        # Step 4: Redirect to the results page with the computed values
        return redirect(url_for('results', 
                                similarity_score=similarity_score, 
                                exact_match=exact_match, 
                                variable_renaming=variable_renaming,
                                structural_similarity=structural_similarity,
                                submitted_code=urllib.parse.quote(submitted_code),
                                original_code=urllib.parse.quote(original_code)
                                
                                ))

    return render_template('get_started.html')

@app.route('/results')
def results():
    # Step 6: Retrieve the data passed from the get_started route
    similarity_score = request.args.get('similarity_score', 0, type=int)
    
    
    exact_match = request.args.get('exact_match', 'False') == 'True'
    variable_renaming = request.args.get('variable_renaming', 'False') == 'True'
    structural_similarity = request.args.get('structural_similarity', 'False') == 'True'
    submitted_code = urllib.parse.unquote(request.args.get('submitted_code', ''))
    original_code = urllib.parse.unquote(request.args.get('original_code', ''))

    logger.info(
        "Rendering results - similarity: %s, exact_match: %s, variable_renaming: %s, structural_similarity: %s",
        similarity_score,
        exact_match,
        variable_renaming,
        structural_similarity,
    )


    # Step 7: Pass the data to the results page
    return render_template('results.html', 
                           similarity_score=similarity_score,
                           exact_match=exact_match,
                           variable_renaming=variable_renaming,
                           structural_similarity=structural_similarity,
                           feedback="",
                           submitted_code=submitted_code,
                           original_code=original_code
                           
                        )
@app.route('/generate_feedback', methods=['POST'])
def generate_feedback_route():
    data = request.get_json()
    submitted_code = data['submitted_code']
    original_code = data['original_code']
    logger.info("Generating feedback")
    feedback = generate_feedback(submitted_code, original_code)
    return jsonify({'feedback': feedback})

if __name__ == '__main__':
    app.run(debug=True)
