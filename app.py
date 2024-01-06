from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from config import db_params  # Import the db_params from the external config module

app = Flask(__name__)

# Remove the local definition of db_params in this file

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

# @app.route('/update', methods=['POST'])
# def update():
#     if request.method == 'POST':
#         data = request.get_json()
#         updated_value = data.get('updatedValue')
#         column_name = data.get('columnName')
#         record_id = data.get('id')

#         try:
#             # Whitelist of allowed column names
#             allowed_columns = ['payment_date', 'birth_date', 'name', 'amount']

#             # Check if the column_name is allowed
#             if column_name not in allowed_columns:
#                 return jsonify({'error': 'Invalid column name'})

#             # Connect to the PostgreSQL database using your db_params
#             conn = psycopg2.connect(**db_params)
#             cursor = conn.cursor()

#             # Construct the SQL query using a parameterized query
#             # This ensures that user input is properly escaped and quoted
#             sql_query = f"UPDATE public_test.payments SET {column_name} = %s WHERE id = %s;"

#             # Execute the query with the updated value and the 'id' as a condition
#             cursor.execute(sql_query, (updated_value, record_id))
#             conn.commit()

#             # Close the cursor and connection
#             cursor.close()
#             conn.close()

#             return jsonify({'message': f'{column_name} updated successfully'})

#         except Exception as e:
#             # Handle any database connection or query errors
#             return jsonify({'error': str(e)})

@app.route('/chart')
def chart():
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Query the data from the table
    cursor.execute("SELECT name, sum(amount) as amount FROM public_test.payments group by name order by amount desc;")
 #   cursor.execute("SELECT payment_date, sum(amount) as amount FROM public_test.payments group by payment_date order by payment_date asc;")

    rows = cursor.fetchall()
#    rows_line_chart = cursor.fetchall()

    chart_data = {
        'name': [row[0] for row in rows],
        'amount': [round(row[1], 2) for row in rows]
    }

#    line_chart_data = {
#        'payment_date': [row[0] for row in rows_line_chart],
#        'amount': [round(row[1], 2) for row in rows_line_chart]        
#    }

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return render_template('chart.html', chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)

