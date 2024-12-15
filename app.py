# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import uuid
from toneAnalyser import ToneAnalyser

# Initialize Flask app
app = Flask(__name__)
# Set upload folder for images
app.config["UPLOAD_FOLDER"] = "static/asset/tone_test/"

# Route for the home page
@app.route('/')
def index():
    return render_template('home.html')


# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the prediction page
@app.route('/predictPage')
def predictPage():
    return render_template('index.html',result='')

# Route to redirect back to home page
@app.route('/backToHome')
def backToHome():
    return render_template('home.html',result='')


# Route for skin tone prediction
@app.route('/skin_tone_predict', methods=["POST"])
def skin_tone_predict():
    
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the uploaded image file
        file = request.files['image']
        print(file)
        # Initialize result variable
        result = ''
        # Check if a file was uploaded
        if file.filename != '':
            filename = f"{str(uuid.uuid4())}.jpg"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            analyzer = ToneAnalyser()
            # Generate a unique filename
        
            # Initialize tone analyser
            analyzer = ToneAnalyser()
            # Analyze the skin tone using the model
            model_output = analyzer.analyse_skin_tone("static/asset/tone_test/"+filename, "jpg")
            # Store the model output in a dictionary
            result ={
                'imageFile':filename,
                'label':model_output["label"],
                'accuracy':model_output["accuracy"],
                'skin_tone':model_output["skin_tone"],
                'dominant_colors':model_output["dominant_colors"],
            }
            # Set success message
            message = 'Image uploaded successfully'
        # Handle case where no image is selected    
        else:
            # Set error message
            message = 'No image selected'
        # Print message for debugging
        print(message)
        # Render the index page with the result
        return render_template('index.html',result=result)



# Run the app if the script is executed
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)

