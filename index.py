from flask import Flask, render_template, request, redirect, url_for, flash
import random, os
from transformers import pipeline
from PIL import Image

#Intialise the app
app = Flask(__name__)
app.secret_key = "supersecretkey123"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

classifier = pipeline("image-classification", model="google/vit-base-patch16-224")



catPlot = [
    "Thinking about pushing a glass of the table.",
    "Just left a hairball on your clean washing.",
    "Tonight will summon the neighborhood cats for a midnight coup.",
    "Knock over your coffee when you’re not looking."]

planNum = len(catPlot)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyse():
    file = request.files["cat_image"]
    if file:

        #Save Image
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Run AI classifier
        img = Image.open(filepath)
        preds = classifier(img)

        # Pick top prediction
        top_pred = preds[0]
        label = top_pred["label"]
        confidence = round(top_pred["score"] * 100, 2)

        # Is it a cat?
        is_cat = "cat" in label.lower()

        # Fake mood: plotting if confidence > 70, else suspicious
        mood = "plotting" if confidence > 70 else "suspicious"

        malice = random.randint(0, 100)
        planChoice = random.randint(0, planNum)
        plan = catPlot[planChoice-1]

        return render_template("result.html", score=malice, plan=plan, label=label, confidence=confidence, is_cat=is_cat, mood=mood, filename=file.filename)
    
    flash("No file uploaded! Please choose a file.")
    return redirect(url_for("index"))  






if __name__ == "__main__":
    app.run(debug=True)