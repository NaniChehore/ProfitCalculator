from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_min_nightly_rate(data):
    purchase_amount = float(data['purchase_amount'])
    furnishing_costs = float(data.get('furnishing_costs', 0))
    bond_repayment = purchase_amount * 0.00929
    levies_rates = float(data['levies_rates'])
    internet_cost = float(data['internet_cost'])
    electricity_cost = float(data['electricity_cost'])
    other_fees = float(data['other_fees'])
    cleaning_fees = float(data['cleaning_fees'])
    consumables = float(data['consumables'])
    occupancy_rate = int(data['occupancy_rate'])
    
    total_monthly_costs = (bond_repayment + levies_rates + internet_cost +
                           electricity_cost + other_fees + cleaning_fees + consumables)
    
    airbnb_commission = 0.03 * 1.15  # 3% + VAT
    booking_com_commission = 0.15
    co_host_commission = 0.12
    
    min_nightly_rate_airbnb = total_monthly_costs / (occupancy_rate * (1 - airbnb_commission - co_host_commission))
    min_nightly_rate_booking = total_monthly_costs / (occupancy_rate * (1 - booking_com_commission - co_host_commission))
    
    profit_levels = []
    for i in range(0, 101, 20):
        profit = total_monthly_costs * (1 + i / 100)
        nights_needed_airbnb = profit / min_nightly_rate_airbnb
        nights_needed_booking = profit / min_nightly_rate_booking
        profit_levels.append((i, round(nights_needed_airbnb, 2), round(nights_needed_booking, 2)))
    
    return round(min_nightly_rate_airbnb, 2), round(min_nightly_rate_booking, 2), profit_levels

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        min_airbnb, min_booking, profit_levels = calculate_min_nightly_rate(request.form)
        return render_template('index.html', min_airbnb=min_airbnb, min_booking=min_booking, profit_levels=profit_levels)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
