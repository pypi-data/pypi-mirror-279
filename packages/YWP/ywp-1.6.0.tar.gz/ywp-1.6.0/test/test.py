from flask import Flask, render_template, request

app = Flask(__name__)

def route_flask(location, returnValue):
    @app.route(location)
    def route_test():
        return returnValue
    
def run(check=False, debug=True, host="0.0.0.0", port="8000"):
    if check == True:
        if __name__ == "__main__":
            app.run(debug=debug, host=host, port=port)
    else:
        app.run(debug=debug, host=host, port=port)

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route("/get")
# def get_bot_response():
#     userText = request.args.get('msg')
#     return str(process(userText))

# if __name__ == "__main__":
#     app.run(debug=True)
