from flask import Flask, render_template, request
import os
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__, template_folder="templates")

cred = credentials.Certificate("sec.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://hotel-management-52c60-default-rtdb.firebaseio.com/"
})

firebase_db = db.reference("/")

r1, r2, r3, r4 = 5, 4, 3, 2
msg = ""

@app.route("/", methods=["GET", "POST"])
def home():

    global r1, r2, r3, r4, msg

    if request.method == "POST":

        name = request.form.get("name")
        room = request.form.get("room")

        if not room:
            msg = "No room selected"
        else:
            room = int(room)

            if room == 1 and r1 > 0:
                r1 -= 1
                msg = name + " booked Single room"

            elif room == 2 and r2 > 0:
                r2 -= 1
                msg = name + " booked Double room"

            elif room == 3 and r3 > 0:
                r3 -= 1
                msg = name + " booked Deluxe room"

            elif room == 4 and r4 > 0:
                r4 -= 1
                msg = name + " booked Suite room"

            else:
                msg = "we are sorry there is no room left in this category", name

        firebase_db.push({
            "name": name,
            "room": room,
            "message": msg
        })

    print("DEBUG:", r1, r2, r3, r4)

    return render_template("index.html",
        r1=r1, r2=r2, r3=r3, r4=r4, msg=msg)

if __name__ == "__main__":
    app.run(debug=True)