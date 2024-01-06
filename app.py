from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from config import db_params  # Import the db_params from the external config module
from flask.helpers import flash

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Query the data from the table
    cursor.execute("SELECT payment_date, birth_date, name, amount, id FROM public_test.payments order by id asc;")
    rows = cursor.fetchall()

    rounded_rows = [(row[0], row[1], row[2], round(row[3], 2),row[4]) for row in rows]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return render_template('index.html', data=rounded_rows)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        payment_date = request.form['payment_date']
        birth_date = request.form['birth_date']
        name = request.form['name']
        amount = request.form['amount']

        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO public_test.payments (payment_date, birth_date, name, amount) VALUES (%s, %s, %s, %s)", (payment_date, birth_date, name, amount))
        conn.commit()  # Commit the changes to the database

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return redirect(url_for('index'))

@app.route('/chart')
def chart():
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Query the data from the table
    cursor.execute("SELECT name, sum(amount) as amount FROM public_test.payments group by name order by amount desc;")

    rows = cursor.fetchall()

    chart_data = {
        'name': [row[0] for row in rows],
        'amount': [round(row[1], 2) for row in rows]
    }

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return render_template('chart.html', chart_data=chart_data)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    if request.method == 'GET':
        # Retrieve the existing data for the specified ID
        cursor.execute("SELECT payment_date, birth_date, name, amount FROM public_test.payments WHERE id = %s", (id,))
        row = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if row:
            return render_template('edit.html', id=id, data=row)
        else:
            flash('Invalid ID')
            return redirect(url_for('index'))

    elif request.method == 'POST':
        # Update the data in the database
        payment_date = request.form['payment_date']
        birth_date = request.form['birth_date']
        name = request.form['name']
        amount = request.form['amount']

        cursor.execute("UPDATE public_test.payments SET payment_date=%s, birth_date=%s, name=%s, amount=%s WHERE id=%s",
                       (payment_date, birth_date, name, amount, id))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return redirect(url_for('index'))

@app.route('/remove/<int:id>')
def remove(id):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Remove the record with the specified ID
    cursor.execute("DELETE FROM public_test.payments WHERE id = %s", (id,))
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

