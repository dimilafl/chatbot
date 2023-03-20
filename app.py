from flask import Flask, render_template, request
# import my_chatbot  # Assuming your chatbot code is in a file named my_chatbot.py
# import v16_compundWords  # Assuming your chatbot code is in a file named v16_compundWords.py
import webAppV1_noChartOrHeatmap  # Assuming your chatbot code is in a file named v16_compundWords.py
from webAppV1_noChartOrHeatmap import handle_input


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    response = webAppV1_noChartOrHeatmap.handle_input(user_input)  # Assuming you have a handle_input function in my_chatbot.py that takes user input and returns the chatbot's response
    return response

if __name__ == "__main__":
    app.run(debug=True)
