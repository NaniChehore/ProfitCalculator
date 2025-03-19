from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        purchase_amount = float(request.form.get("purchaseAmount", 0))
        furnishing_cost = float(request.form.get("furnishingCost", 0))
        levies_rates = float(request.form.get("leviesRates", 0))
        internet_cost = float(request.form.get("internetCost", 0))
        electricity_cost = float(request.form.get("electricityCost", 0))
        other_fees = float(request.form.get("otherFees", 0))
        cleaning_fees = float(request.form.get("cleaningFees", 0))
        consumables = float(request.form.get("consumables", 0))
        occupancy_rate = int(request.form.get("occupancyRate", 0))

        # Monthly Bond Repayment
        bond_repayment = purchase_amount * 0.00929

        # Total Monthly Costs
        total_monthly_cost = (bond_repayment + levies_rates + internet_cost +
                              electricity_cost + other_fees + cleaning_fees + consumables)

        # Minimum Nightly Rate Calculation
        min_nightly_rate = total_monthly_cost / max(occupancy_rate, 1)

        # Nights Needed to Break Even
        nights_to_break_even = round(total_monthly_cost / min_nightly_rate)

        # Nights Needed for 20% Profit Increase
        profit_margin = 1.2
        nights_for_20_profit = round((total_monthly_cost * profit_margin) / min_nightly_rate)

        return jsonify({
            "min_rate": round(min_nightly_rate, 2),
            "nights_to_break_even": nights_to_break_even,
            "nights_for_20_profit": nights_for_20_profit
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
