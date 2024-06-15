from flask import Flask

app = Flask(__name__)

def route_flask(location, returnValue):
    try:
        @app.route(location)
        def route_test():
            return returnValue
        return 'done'
    except:
        return 'error'
    
def run(check=False, debug=True, host="0.0.0.0", port="8000"):
    try:
        if check == True:
            if __name__ == "__main__":
                app.run(debug=debug, host=host, port=port)
        else:
            app.run(debug=debug, host=host, port=port)
        return 'done'
    except:
        return 'error'