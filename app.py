from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to establish a connection to the database
def get_db_connection():
    conn = psycopg2.connect(
        dbname="Patient_Register",  # Database name
        user="vaibhav",             # Your username
        password="72258",           # Your password
        host="localhost",           # Your host (if different from localhost)
        port="5432"                 # Your port (if different from 5432)
    )
    return conn

# Route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Retrieve form data
            conn = get_db_connection()  # Get a new database connection
            cursor = conn.cursor()
            # Insert data into database using a parameterized query
            cursor.execute("INSERT INTO patients (first_name, middle_name, last_name, birth_date, gender, mobile, email, address, pincode, aadhar_number, present_condition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (request.form['first_name'], request.form['middle_name'], request.form['last_name'], request.form['birth_date'], request.form['gender'], request.form['mobile'], request.form['email'], request.form['address'], request.form['pincode'], request.form['aadhar_number'], request.form['present_condition']))
            conn.commit()
            cursor.close()
            conn.close()  # Close the database connection
            flash('Patient data saved successfully!', 'success')
            return redirect(url_for('index'))  # Redirect to the index route
        except Exception as e:
            flash(str(e), 'error')  # Flash error message if an exception occurs

    return render_template('index.html')

# Close database connection when the Flask app is shut down
@app.teardown_appcontext
def close_connection(exception):
    pass

if __name__ == '__main__':
    app.run(debug=True)
