from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            fixed_costs = list(map(float, request.form.getlist("fixed_costs")))
            variable_costs = list(map(float, request.form.getlist("variable_costs")))
            occupancy_rate = float(request.form["occupancy_rate"]) / 100
            profit_margin = float(request.form["profit_margin"]) / 100

            total_fixed = sum(fixed_costs)
            total_variable = sum(variable_costs)
            break_even = total_fixed / occupancy_rate + total_variable

            airbnb_rate = break_even / (1 - 0.03)
            booking_rate = break_even / (1 - 0.15)
            combined_rate = break_even / (1 - ((0.03 + 0.15) / 2))

            return render_template("index.html", airbnb_price=airbnb_rate,
                                   booking_price=booking_rate, combined_price=combined_rate)
        except:
            return "Error: Please enter valid numbers."

    return render_template("index.html", airbnb_price=None, booking_price=None, combined_price=None)

if __name__ == "__main__":
    app.run(debug=True)
