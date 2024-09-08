from flask import Flask, render_template, request, redirect, url_for
from rule_model import plagiarism_detection
from ai_model import calculate_similarity, generate_feedback

app = Flask(__name__)

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
        
        # Step 2: Pass the data to rule_model for boolean values
        exact_match, variable_renaming, structural_similarity = plagiarism_detection(original_code, submitted_code)
        
        # Step 3: Pass the data to ai_model for similarity score
        similarity_score = calculate_similarity(original_code, submitted_code)
        
        # Step 4: Generate feedback
        feedback = generate_feedback(submitted_code, original_code)

        # Step 5: Redirect to the results page with the computed values
        return redirect(url_for('results', 
                                similarity_score=similarity_score, 
                                exact_match=exact_match, 
                                variable_renaming=variable_renaming, 
                                structural_similarity=structural_similarity, 
                                feedback=feedback))

    return render_template('get_started.html')

@app.route('/results')
def results():
    # Step 6: Retrieve the data passed from the get_started route
    similarity_score = request.args.get('similarity_score', 0, type=int)
    exact_match = request.args.get('exact_match', False, type=bool)
    variable_renaming = request.args.get('variable_renaming', False, type=bool)
    structural_similarity = request.args.get('structural_similarity', False, type=bool)
    feedback = request.args.get('feedback', '')

    # Step 7: Pass the data to the results page
    return render_template('results.html', 
                           similarity_score=similarity_score,
                           exact_match=exact_match,
                           variable_renaming=variable_renaming,
                           structural_similarity=structural_similarity,
                           feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)