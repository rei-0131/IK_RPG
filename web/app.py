from flask import Flask, render_template, request
import os
# ngrok start
# cd C:\Users\REI\Downloads\ngrok-v3-stable-windows-amd64
# .\ngrok http --domain=tops-desired-hog.ngrok-free.app 5000

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.urandom(24)


@app.route("/",methods=["GET", "POST"])
def rpg():
    user_agent = request.headers.get("User-Agent").lower()
    print(user_agent)
    if "mobile" in user_agent:
        return render_template("sp/rpg.html")
    else:
        return render_template("pc/rpg.html")


app.run(host='127.0.0.1', port=5000,debug=False,threaded=True)