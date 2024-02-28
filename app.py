from flask import Flask, render_template, redirect, request
import socket
import json

app = Flask(__name__)

try:
  database = json.loads(open("database.json", 'r', encoding="utf-8").read())
except:
  open("database.json", 'w', encoding="utf-8").write("{}")
  database = {}

update_database = lambda : open("database.json", 'w', encoding="utf-8").write(json.dumps(database, indent=4))

@app.route('/')
def index():
  return render_template("home.html", data={})

@app.route("/short", methods=["POST","GET"])
def shorter():
  base_url = '/'.join(request.base_url.split("/")[0:3])

  if request.method.lower() == "post":
    url = request.form.get("url").strip()

    if (url==''):
      return render_template("error.html", data={'message':"Don't leave the link null!"})
    else:
      try:
        if url in list(database.values()):
          lid = list(database.keys())[list(database.values()).index(url)]
          short_link = f"{base_url}/{lid}"
        else:
          lid = str(len(database)+1)
          database[lid] = url
          update_database()
          short_link = f"{base_url}/{lid}"
      except:
        return (render_template("error.html", data={"message": "Something is wrong!"}), 300)

    return render_template("short.html", data={ "short_url": short_link }), 200
  
  else:
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
  return (render_template("error.html", data={"message": "Page Not Found"}), 404)

@app.route("/<int:lid>")
def redirect_to_url(lid):
  try:
    return redirect(database[str(lid)])
  except:
    return (render_template("error.html", data={"message": "Something is wrong!"}), 300)

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]
  s.close()
except:
  hostname = socket.gethostname()
  ip = socket.gethostbyname(hostname)

app.run(debug=True, host=ip) if (__name__ == "__main__") else ...