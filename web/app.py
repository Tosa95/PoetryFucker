from flask import Flask, render_template, request

rhy = None
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        ph = request.form["phrase"]

        return render_template('home.html', titles=rhy.rhyme(ph))

    return render_template("home.html")



def start_web_server(ryhmer, port=4999, host="0.0.0.0"):

    global rhy

    rhy = ryhmer

    app.secret_key = 'secret123'
    app.run(debug=True,port=port,host=host)