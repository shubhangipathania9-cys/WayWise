from flask import Flask, render_template , request
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/plan")
def plan():
    return render_template("plan.html")

@app.route("/preferences", methods=["GET", "POST"])
def preferences():

    if request.method == "POST":
        destination = request.form["destination"]
        days = request.form["days"]
        travellers = request.form["travellers"]
        budget = request.form["budget"]

        return render_template(
            "preferences.html",
            destination=destination,
            days=days,
            travellers=travellers,
            budget=budget
        )

    return render_template("preferences.html")
@app.route("/generate-itinerary", methods=["POST"])
def generate_itinerary():

    budget_flexibility = request.form["budget_flexibility"]
    emergency_fund = request.form["emergency_fund"]
    accommodation = request.form["accommodation"]
    pace = request.form["pace"]
    destination = request.form["destination"]
    days = request.form["days"]
    travellers = request.form["travellers"]
    budget = request.form["budget"]

    return render_template(
    "itinerary.html",
    destination=destination,
    days=days,
    travellers=travellers,
    budget=budget,
    budget_flexibility=budget_flexibility,
    emergency_fund=emergency_fund,
    accommodation=accommodation,
    pace=pace
)

if __name__ == "__main__":
    app.run(debug=True)