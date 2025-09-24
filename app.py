from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory data storage for demonstration purposes
bookings = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        guest_name = request.form.get('guest_name')
        room_type = request.form.get('room_type')
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')

        # Calculate the number of nights
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        num_nights = (check_out_date - check_in_date).days

        # Simple pricing logic
        room_rates = {'single': 100, 'double': 150, 'suite': 200}
        total_cost = room_rates[room_type] * num_nights

        # Store booking details
        bookings.append({
            'guest_name': guest_name,
            'room_type': room_type,
            'check_in': check_in,
            'check_out': check_out,
            'total_cost': total_cost
        })

        return redirect(url_for('invoice', guest_name=guest_name, total_cost=total_cost))

    return render_template('booking.html')

@app.route('/invoice')
def invoice():
    guest_name = request.args.get('guest_name')
    total_cost = request.args.get('total_cost')
    return render_template('invoice.html', guest_name=guest_name, total_cost=total_cost)

@app.route('/results')
def results():
    return render_template('results.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)