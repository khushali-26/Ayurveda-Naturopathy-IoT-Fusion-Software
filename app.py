import sqlite3
import random

from flask import Flask, render_template, request, session, send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

app.secret_key = "ayurveda_project_key"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/questionnaire', methods=['POST'])
def questionnaire():

    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")

    return render_template(
        'questionnaire.html',
        name=name,
        age=age,
        gender=gender
    )

@app.route('/analyze', methods=['POST'])
def analyze():

    from datetime import datetime
    today = datetime.now().strftime("%d-%m-%Y")

    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")

    # -------------------------
    # Initialize Scores
    # -------------------------

    vata = 0
    pitta = 0
    kapha = 0
    wellness = 100

    # -------------------------
    # Get Form Data
    # -------------------------

    answers = {}

    answers = {}
    
    question_keys = [
        'p1','p2','p3','p4','p5','p6','p7','p8','p9','p10',
        'v11','v12','v13','v14','v15','v16','v17','v18','v19','v20',
        'n21','n22','n23','n24','n25','n26','n27','n28','n29','n30'
    ]
    
    for key in question_keys:
        answers[key] = int(request.form.get(key, 0))

    # -------------------------
    # VATA CALCULATION
    # -------------------------

    vata += answers['p1'] * 3
    vata += answers['p2'] * 3
    vata += answers['p3'] * 3
    vata += answers['p5'] * 2
    vata += answers['p7'] * 2
    vata += answers['p9'] * 3

    vata += answers['v11'] * 3
    vata += answers['v13'] * 3
    vata += answers['v14'] * 3
    vata += answers['v17'] * 2
    vata += answers['v19'] * 2

    vata += answers['n29'] * 2
    vata += answers['n30'] * 3


    # -------------------------
    # PITTA CALCULATION
    # -------------------------

    pitta += answers['p4'] * 3
    pitta += answers['p6'] * 3
    pitta += answers['p8'] * 3

    pitta += answers['v15'] * 3
    pitta += answers['v16'] * 3
    pitta += answers['v18'] * 3

    pitta += answers['n22'] * 1
    pitta += answers['n27'] * 2
    pitta += answers['n28'] * 1


    # -------------------------
    # KAPHA CALCULATION
    # -------------------------

    kapha += answers['p10'] * 3

    kapha += answers['v12'] * 3
    kapha += answers['v20'] * 3
    kapha += answers['v19'] * 1

    kapha += answers['n23'] * 2
    kapha += answers['n24'] * 3
    kapha += answers['n25'] * 1
    kapha += answers['n26'] * 1
    kapha += answers['n27'] * 1
    kapha += answers['n28'] * 1


    # -------------------------
    # WELLNESS SCORE
    # -------------------------

    wellness -= answers['v11']
    wellness -= answers['v12']
    wellness -= answers['v13']
    wellness -= answers['v14']
    wellness -= answers['v15']
    wellness -= answers['v16']
    wellness -= answers['v17']
    wellness -= answers['v18']
    wellness -= answers['v19']
    wellness -= answers['v20']

    wellness -= answers['n21'] * 3
    wellness -= answers['n22'] * 2
    wellness -= answers['n23'] * 3
    wellness -= answers['n24'] * 3
    wellness -= answers['n25'] * 2
    wellness -= answers['n26'] * 2
    wellness -= answers['n27'] * 3
    wellness -= answers['n28'] * 3
    wellness -= answers['n29'] * 2
    wellness -= answers['n30'] * 2

    if wellness < 0:
        wellness = 0
        wellness_status = "Needs Improvement"
        hydration = "Needs Improvement"

    elif wellness >= 80:
        wellness_status = "Excellent"
        hydration = "Good"
    
    elif wellness >= 60:
        wellness_status = "Good"
        hydration = "Moderate"
        
    elif wellness >= 40:
        wellness_status = "Moderate"
        hydration = "Low"
        
    else:
        wellness_status = "Needs Improvement"
        hydration = "Needs Improvement"


    # -------------------------
    # FIND DOMINANT DOSHA
    # -------------------------

    doshas = {
        "Vata": vata,
        "Pitta": pitta,
        "Kapha": kapha
    }


    dominant_dosha = max(doshas, key=doshas.get)

    body_temp = round(random.uniform(97.5, 99.2), 1)
    steps = random.randint(2000, 10000)

    if dominant_dosha == "Vata":
        heart_rate = random.randint(80, 100)
        sleep_hours = round(random.uniform(4.5, 6.5), 1)

    elif dominant_dosha == "Pitta":
        heart_rate = random.randint(70, 90)
        sleep_hours = round(random.uniform(6.0, 8.0), 1)

    else:  # Kapha
        heart_rate = random.randint(60, 75)
        sleep_hours = round(random.uniform(7.0, 9.0), 1)
    
    conn = sqlite3.connect('wellness.db')

    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO assessments
                   (name, age, gender, vata, pitta, kapha,
                    wellness, dominant_dosha)

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    ( 
                        request.form.get("name"),
                        request.form.get("age"),
                        request.form.get("gender"),
                        vata,
                        pitta,
                        kapha,
                        wellness,
                        dominant_dosha
                    ))

    conn.commit()
    conn.close()

    # -------------------------
    # RECOMMENDATIONS
    # -------------------------

    if dominant_dosha == "Vata":
        recommendation = [
            "Warm cooked foods",
            "Regular sleep schedule",
            "Meditation",
            "Oil massage",
            "Grounding activities"
        ]

    elif dominant_dosha == "Pitta":
        recommendation = [
            "Cooling foods",
            "Avoid excessive spicy meals",
            "Mindfulness practices",
            "Adequate hydration",
            "Stress management"
        ]

    else:
        recommendation = [
            "Regular exercise",
            "Lighter meals",
            "Morning sunlight exposure",
            "Active lifestyle",
            "Reduced sedentary habits"
        ]

    # -------------------------
    # SENSOR BASED INSIGHT
    # -------------------------

    sensor_insight = ""

    if sleep_hours < 5:
        sensor_insight += (
            "Low sleep duration detected. "
            "This may contribute to Vata imbalance and fatigue. "
        )

    if heart_rate > 90:
        sensor_insight += (
            "Elevated heart rate detected. "
            "Stress reduction and relaxation techniques are recommended. "
        )

    if steps < 3000:
        sensor_insight += (
            "Low physical activity detected. "
            "Regular walking or yoga is recommended. "
        )

    if body_temp > 99:
        sensor_insight += (
            "Slightly elevated body temperature detected. "
            "Hydration and adequate rest are advised. "
        )

    if sensor_insight == "":
        sensor_insight = (
            "All simulated sensor readings are within a healthy wellness range."
        )
    
    session['name'] = name 
    session['age'] = age
    session['gender'] = gender

    session['vata'] = vata
    session['pitta'] = pitta
    session['kapha'] = kapha

    session['wellness'] = wellness
    session['wellness_status'] = wellness_status

    session['dominant_dosha'] = dominant_dosha

    session['heart_rate'] = heart_rate
    session['body_temp'] = body_temp
    session['sleep_hours'] = sleep_hours
    session['steps'] = steps
    session['hydration'] = hydration

    session['sensor_insight'] = sensor_insight
    
    session['recommendation'] = recommendation

    return render_template(
        'dashboard.html',
        name=name,
        age=age,
        gender=gender,
        today=today,
        wellness_status=wellness_status,
        vata=vata,
        pitta=pitta,
        kapha=kapha,
        wellness=wellness,
        heart_rate=heart_rate,
        body_temp=body_temp,
        sleep_hours=sleep_hours,
        steps=steps,
        hydration=hydration,
        dominant_dosha=dominant_dosha,
        sensor_insight=sensor_insight,
        recommendation=recommendation
    )


@app.route('/download_pdf')
def download_report():

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 800, "Wellness Assessment Report")

    pdf.drawString(100, 770, f"Name: {session.get('name')}")
    pdf.drawString(100, 750, f"Age: {session.get('age')}")
    pdf.drawString(100, 730, f"Gender: {session.get('gender')}")

    pdf.drawString(100, 690, f"Vata Score: {session.get('vata')}")
    pdf.drawString(100, 670, f"Pitta Score: {session.get('pitta')}")
    pdf.drawString(100, 650, f"Kapha Score: {session.get('kapha')}")

    pdf.drawString(100, 610, f"Wellness Score: {session.get('wellness')}")
    pdf.drawString(100, 590, f"Status: {session.get('wellness_status')}")

    pdf.drawString(100, 550,
                   f"Dominant Dosha: {session.get('dominant_dosha')}")

    pdf.drawString(100, 500,
                   f"Heart Rate: {session.get('heart_rate')} bpm")

    pdf.drawString(100, 480,
                   f"Body Temperature: {session.get('body_temp')} °F")

    pdf.drawString(100, 460,
                   f"Sleep Hours: {session.get('sleep_hours')}")

    pdf.drawString(100, 440,
                   f"Daily Steps: {session.get('steps')}")

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Wellness_Report.pdf",
        mimetype="application/pdf"
    )

@app.route('/history')
def history():

    conn = sqlite3.connect('wellness.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assessments")

    records = cursor.fetchall()

    conn.close()

    return render_template(
        'history.html',
        records=records
    )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/iot')
def iot():
    return render_template('iot.html')

if __name__ == '__main__':
    app.run(debug=True) 