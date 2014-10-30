from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    # Return HTML page 
    return render_template('poly_loc1.html')


if __name__ == '__main__':
    app.run(debug=True)