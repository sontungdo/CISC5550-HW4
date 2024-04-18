from flask import Flask, render_template, redirect, request, url_for
import requests  

app = Flask(__name__)


@app.route("/")
def show_list():
    # Fetch data from the API route
    resp = requests.get("http://localhost:5001/api/items") 
    resp = resp.json()
    return render_template('index.html', todolist=resp)


@app.route("/add", methods=['POST'])
def add_entry():
    # Send data to the API route
    new_todo = {"what_to_do": request.form["what_to_do"], "due_date": request.form["due_date"]}
    resp = requests.post("http://localhost:5001/api/add", json=new_todo)  
    return redirect(url_for('show_list'))


@app.route("/delete/<item>", methods=['POST'])
def delete_entry(item):
    # Send delete request to the API route
    resp = requests.delete("http://localhost:5001/api/delete/" + item)
    return redirect(url_for('show_list'))


@app.route("/mark/<item>", methods=['POST'])
def mark_as_done(item):
    # Send mark request to the API route
    resp = requests.put("http://localhost:5001/api/mark/" + item)
    return redirect(url_for('show_list'))


if __name__ == "__main__":
    app.run() 
