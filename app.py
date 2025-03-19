from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    # Extract inputs
    purchase_amount = float(data.get("purchaseAmount", 0))
    furnishing_cost = float(data.get("furnishingCost", 0))
    levies_rates = float(data.get("leviesRates", 0))
    internet_cost = float(data.get("internetCost", 0))
    electricity_cost = float(data.get("electricityCost", 0))
    other_fees = float(data.get("otherFees", 0))
    cleaning_fees = float(data.get("cleaningFees", 0))
    consumables_cost = float(data.get("consumablesCost", 0))
    occupancy = int(data.get("occupancy", 0))

    # Bond repayment calculation (0.929% of purchase price)
    bond_payment = purchase_amount * 0.00929

    # Total monthly fixed costs
    total_monthly_costs = (bond_payment + levies_rates + internet_cost + 
                           electricity_cost + other_fees + cleaning_fees + consumables_cost)

    # Minimum and maximum nightly rates
    min_nightly_rate = 1500
    max_nightly_rate = 2500

    # Commission calculations
    airbnb_commission = 0.03 + 0.15  # 3% + 15% VAT
    booking_commission = 0.15  # 15% fee
    co_host_commission = 0.12  # 12% fee

    # Airbnb & Booking.com revenue per night (after fees)
    airbnb_net_rate = min_nightly_rate * (1 - airbnb_commission - co_host_commission)
    booking_net_rate = min_nightly_rate * (1 - booking_commission - co_host_commission)

    # Calculate break-even nights
    airbnb_break_even_nights = round(total_monthly_costs / airbnb_net_rate, 1)
    booking_break_even_nights = round(total_monthly_costs / booking_net_rate, 1)

    # Calculate profit nights (20% increments)
    airbnb_profit_nights = [round((total_monthly_costs * (1 + i)) / airbnb_net_rate, 1) for i in [0.2, 0.4, 0.6, 0.8, 1]]
    booking_profit_nights = [round((total_monthly_costs * (1 + i)) / booking_net_rate, 1) for i in [0.2, 0.4, 0.6, 0.8, 1]]

    return jsonify({
        "bondPayment": round(bond_payment, 2),
        "breakEvenNights": {
            "airbnb": airbnb_break_even_nights,
            "booking": booking_break_even_nights
        },
        "profitNights": {
            "airbnb": airbnb_profit_nights,
            "booking": booking_profit_nights
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
