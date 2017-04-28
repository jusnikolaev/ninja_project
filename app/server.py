from flask import Flask, render_template, url_for
import jinja2

app = Flask(__name__, static_folder='/Users/jusnikolaev/Desktop/LearnPython/ninja_project/static')
app.jinja_loader = jinja2.FileSystemLoader('/Users/jusnikolaev/Desktop/LearnPython/ninja_project/templates')



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)