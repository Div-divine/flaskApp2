from flask import Flask, render_template

app = Flask(__name__)

# Create  a route decorator

# Filters
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags

garden =['Tomatoes', 'Yam', 'Orange', 'Apple']

not_fruit = "<h1>Not a fruit</h1>"

@app.route("/")
# def index():
#     return "<h1>Hello World</h1>"
def index():
    return render_template("index.html", garden=garden, not_fruit=not_fruit)

@app.route("/about")
def about():
    return render_template("about.html")

# Example: localhost5000/user/Bob

@app.route("/user/<name>/<surname>")
def user(name, surname):
    return render_template("user.html", name=name, surname=surname)


# Create custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

# Inernal Server Error
@app.errorhandler(500)
def page_not_found(error):
    return render_template("500.html"), 500






if __name__ == '__main__':
    app.run(debug=True)