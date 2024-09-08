### README: Advanced Plagiarism Detection System

---

## Project Overview

This project implements an **Advanced Plagiarism Detection System** designed for EdTech platforms and recruitment processes. It detects various forms of plagiarism, including **exact code matches**, **variable renaming**, and **structural changes**. Additionally, the system leverages AI models to compute **semantic similarities** and provides feedback on how to improve submitted code. It also includes features to monitor for **real-time cheating**, such as abnormal typing speed or copy-pasting code.

---

## Features

- **Rule-Based Detection**:
  - Detects **exact matches**, **variable renaming**, and **structural changes** in the submitted code.
- **AI-Driven Detection**:
  - Computes **semantic similarities** between user submissions and existing solutions using AI models (e.g., OpenAI Codex).
  - Provides **feedback** on plagiarism and code improvements.
- **Cheating Detection**:
  - Monitors typing speed and clipboard activity.

---

## Technology Stack

- **Backend**: Python, Flask
- **AI Models**: OpenAI API (Codex)
- **Frontend**: HTML, CSS, JavaScript, Chart.js (for visualizations)
- **Caching**: Redis (optional for optimization)
  
---

## Installation and Setup

### Prerequisites

- Python 3.x
- Flask
- OpenAI API Key
- Optional: Redis (for caching)
  
### Install Dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/plagiarism-detection-system.git
   cd plagiarism-detection-system
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your **OpenAI API Key**:
   - Create an `.env` file in the root directory or export your API key as an environment variable:
     ```bash
     export OPENAI_API_KEY='your-openai-api-key'
     ```

### Run the Application

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Access the app in your browser at:
   ```bash
   http://127.0.0.1:5000/
   ```

---

## Project Structure

```
/project_directory
│
├── app.py                 # Flask application
├── rule_model.py          # Rule-based plagiarism detection logic
├── ai_model.py            # AI model logic for similarity and feedback
├── requirements.txt       # Python dependencies
│
├── static/                
│   ├── css/               # Contains CSS files
│   └── images/            # Image assets for the project
│
└── templates/
    ├── index.html         # Home page
    ├── get_started.html   # Get started page for code input
    └── results.html       # Results page with detection output
```

---

## Workflow

1. **Home Page (`index.html`)**:
   - The landing page with a brief introduction and a button to navigate to the "Get Started" page.

2. **Get Started Page (`get_started.html`)**:
   - Users input their **code**, **question**, and **original solution**.
   - Upon submission, the data is passed to the backend for processing.

3. **Backend Processing (`app.py`)**:
   - The backend calls:
     - `plagiarism_detection()` from **rule_model.py** to calculate boolean values for **exact match**, **variable renaming**, and **structural similarity**.
     - `calculate_similarity()` from **ai_model.py** to compute the plagiarism score for the pie chart.
     - `generate_feedback()` from **ai_model.py** to provide feedback for improving the code.
   - The results are redirected to the **Results Page**.

4. **Results Page (`results.html`)**:
   - Displays:
     - **Boolean values** for plagiarism checks (✔ or ✖).
     - A **pie chart** visualizing plagiarism vs. originality.
     - **Feedback** for improving the code.

---

## Usage

1. Navigate to the **Get Started** page.
2. Enter the **code**, **question**, and **original solution** in their respective fields.
3. Submit the form. The results will be displayed on the **Results** page.
   - The page will display boolean results for **exact match**, **variable renaming**, and **structural similarity**.
   - A **pie chart** visualizes the percentage of originality.
   - A feedback section provides suggestions to avoid plagiarism.

---

## Example

- **Submitted Code**: 
  ```python
  def sum(a, b):
      return a + b
  ```
  
- **Original Code**: 
  ```python
  def add_numbers(x, y):
      return x + y
  ```

- **Results**:
  - **Exact Match**: ✖
  - **Variable Renaming**: ✔
  - **Structural Similarity**: ✔
  - **Feedback**: "Consider using different variable names and restructuring the function logic."

---

## Future Improvements

- **Real-Time Monitoring**: Add functionality to monitor clipboard activity and typing speed.
- **Caching**: Implement Redis caching for frequently submitted solutions to improve performance.
- **Extend AI Model**: Enhance the feedback mechanism by using more advanced AI models for deeper semantic analysis.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Contributors

- [Kanha Gupta]
- [Rahul Shekhawat]
- [Satvik Verma]
- [Tushar Singhal]
```

### Notes:
- Update the **API key** setup section and **Contributors** section with relevant details.
- Include links to GitHub or other project hosting services if applicable.

This README should provide a comprehensive guide to your project's structure, usage, and workflow. Let me know if you need any adjustments!
