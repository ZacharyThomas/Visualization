from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    # Return HTML page 
    return render_template('poly_kenil.html')

@app.route('/white')
def white():
    return render_template('poly_white.html')

@app.route('/west')
def west():
	return render_template('poly_west.html')

if __name__ == '__main__':
    app.run(debug=True)
