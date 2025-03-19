from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json

        # Inputs
        purchase_amount = float(data.get('purchase_amount', 0))
        furnishing_costs = float(data.get('furnishing_costs', 0))
        levies_rates = float(data.get('levies_rates', 0))
        internet_cost = float(data.get('internet_cost', 0))
        electricity_cost = float(data.get('electricity_cost', 0))
        other_fees = float(data.get('other_fees', 0))
        cleaning_fees = float(data.get('cleaning_fees', 0))
        consumables_cost = float(data.get('consumables_cost', 0))
        occupancy_days = int(data.get('occupancy_days', 0))

        # Assumed bond repayment at 0.929% of purchase price
        bond_repayment = 0.00929 * purchase_amount

        # Total Monthly Expenses
        total_expenses = (
            bond_repayment + levies_rates + internet_cost + 
            electricity_cost + other_fees + cleaning_fees + consumables_cost
        )

        # Airbnb and Booking.com Commission Rates
        airbnb_commission = 0.03  # 3% Airbnb Fee (excluding VAT)
        airbnb_vat = 0.15  # 15% VAT
        airbnb_total_fee = airbnb_commission + (airbnb_commission * airbnb_vat)

        booking_com_commission = 0.15  # 15% Booking.com Fee
        cohost_commission = 0.12  # 12% Co-host fee

        # Nightly rate range
        min_nightly_rate = 1500  # R1,500
        max_nightly_rate = 2500  # R2,500

        results = []

        for nightly_rate in range(min_nightly_rate, max_nightly_rate + 1, 100):
            airbnb_revenue_per_booking = nightly_rate * (1 - airbnb_total_fee) * (1 - cohost_commission)
            booking_com_revenue_per_booking = nightly_rate * (1 - booking_com_commission) * (1 - cohost_commission)

            min_nights_break_even_airbnb = total_expenses / airbnb_revenue_per_booking
            min_nights_break_even_booking = total_expenses / booking_com_revenue_per_booking

            results.append({
                "nightly_rate": nightly_rate,
                "break_even_nights_airbnb": round(min_nights_break_even_airbnb, 2),
                "break_even_nights_booking": round(min_nights_break_even_booking, 2),
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
