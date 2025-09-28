from flask import Flask, render_template, request, redirect, url_for, flash
import random, base64
from transformers import pipeline
from PIL import Image
from io import BytesIO



#Intialise the app
app = Flask(__name__)
app.secret_key = "supersecretkey123"
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")




catPlotPlotting = [
    "Strategically waiting until 3am to sprint across the house.",
    "Planning the exact moment to sit on your laptop keyboard.",
    "Calculating how to knock your phone behind the couch forever.",
    "Eyeing the curtains, preparing for a vertical climb.",
    "Plotting to lure you into the kitchen, then demanding nothing.",
    "Choosing the most delicate shelf to perch on and 'accidentally' wobble items.",
    "Timing the perfect jump scare from behind the door.",
    "Organizing a synchronized yowl with the neighbor’s cat.",
    "Pretending to nap while actually waiting for the vacuum to come out.",
    "Scheming to block your view during your favorite show."
]

catPlotDevious = [
    "Clawing the expensive chair while ignoring the scratching post.",
    "Knocking a water glass over with deliberate eye contact.",
    "Unplugging your charger with one subtle tail flick.",
    "Stealing your seat the second you stand up.",
    "Dragging socks around the house as trophies of conquest.",
    "Pawing open the cupboard to scatter snacks everywhere.",
    "Sitting exactly where you were about to put something important.",
    "Scratching at the door, only to walk away when it’s opened.",
    "Pretending to want cuddles, then biting your hand mid-pat.",
    "Plotting to shred toilet paper into a snowy wonderland."
]

catPlotSuspicious = [
    "Watching the ceiling intently as if something lurks above.",
    "Staring at a blank corner until you feel unsettled.",
    "Pausing in the hallway like they’ve seen an intruder.",
    "Following you silently from room to room.",
    "Sitting on the windowsill, glaring at nothing for hours.",
    "Tilting their head as though decoding your every move.",
    "Disappearing for hours, then reappearing with a smug face.",
    "Suddenly bolting across the room for 'no reason.'",
    "Inspecting your shoes like they hold state secrets.",
    "Freezing mid-play, staring straight through you as if plotting deeper schemes."
]


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyse():
    file = request.files["cat_image"]
    if file and file.filename != "":

        img = Image.open(file.stream)

        # Run AI classifier
        preds = classifier(img)

        # Pick top prediction
        top_pred = preds[0]
        label = top_pred["label"]
        confidence = round(top_pred["score"] * 100, 2)

        # Is it a cat?
        is_cat = "cat" in label.lower()

        # Fake mood
        if confidence > 80:
            mood = "plotting"
            moodChoice = catPlotPlotting
            malice = random.randint(50, 100)
        elif confidence > 60:
            mood = "devious"
            moodChoice = catPlotDevious
            malice = random.randint(40, 100)
        else:
            mood = "suspicious"
            moodChoice = catPlotSuspicious
            malice = random.randint(30, 100)

        
        planNum = len(moodChoice)
        planChoice = random.randint(1, planNum)
        plan = moodChoice[planChoice-1]

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return render_template("result.html", score=malice, plan=plan, label=label, confidence=confidence, is_cat=is_cat, mood=mood, filename=file.filename, image_data=img_b64)
    
    flash("Dude... I need an image to analyse.")
    return redirect(url_for("index"))  





# The code below is for local development only and must be removed/commented for deployment to vercel
#if __name__ == "__main__":
#    app.run(debug=True)