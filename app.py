from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'manager'
app.config['MYSQL_DB'] = 'stardb'

mysql = MySQL(app)

# Initialize the database
def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS star_giver_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(120) NOT NULL,
                suggestion VARCHAR(120),
                stars INT NOT NULL
            );
        ''')
        mysql.connection.commit()
        cur.close()

# Initialize the database when the app starts
@app.before_first_request
def setup():
    init_db()

@app.route('/')
def index():
    # Render the resume and ratings form
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    stars = request.form.get('stars')
    suggestion = request.form.get('suggestion')

    # Check for missing fields
    if not name or not email or not stars:
        return jsonify({'error': 'Name, email, and stars are required!'}), 400

    # Ensure 'stars' is an integer
    try:
        stars = int(stars)
    except ValueError:
        return jsonify({'error': 'Stars must be an integer!'}), 400

    # Insert into database
    cur = mysql.connection.cursor()
    cur.execute('''
        INSERT INTO star_giver_table (name, email, stars, suggestion) VALUES (%s, %s, %d, %s)''', ([name, email, stars, suggestion]))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Rating submitted successfully!'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
