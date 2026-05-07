import os
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

def parse_matrix(text):
    if not text: return None
    try:
        rows = text.strip().split("\n")
        matrix = [list(map(float, row.split())) for row in rows]
        return np.array(matrix)
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    matrix_a_text = ""
    matrix_b_text = ""

    if request.method == "POST":
        action = request.form.get("action")
        matrix_a_text = request.form.get("matrix_a", "")
        matrix_b_text = request.form.get("matrix_b", "")
        
        A = parse_matrix(matrix_a_text)
        B = parse_matrix(matrix_b_text)

        try:
            if action == "add":
                if A is not None and B is not None and A.shape == B.shape:
                    result = (A + B).tolist()
                else: error = "Size mismatch for Addition!"
            
            elif action == "subtract":
                if A is not None and B is not None and A.shape == B.shape:
                    result = (A - B).tolist()
                else: error = "Size mismatch for Subtraction!"
            
            elif action == "multiply":
                if A is not None and B is not None and A.shape[1] == B.shape[0]:
                    result = np.dot(A, B).tolist()
                else: error = "Invalid dimensions for Multiplication!"
            
            elif action == "transpose":
                if A is not None:
                    result = A.T.tolist()
                else: error = "Matrix A is invalid!"
            
            elif action == "determinant":
                if A is not None and A.shape[0] == A.shape[1]:
                    det = np.linalg.det(A)
                    result = f"Determinant of A = {det:.2f}"
                else: error = "Determinant requires a square matrix!"

        except Exception as e:
            error = f"Mathematical Error: {str(e)}"

    return render_template("index.html", 
                           result=result, 
                           error=error, 
                           a_val=matrix_a_text, 
                           b_val=matrix_b_text)

if __name__ == "__main__":
    app.run()