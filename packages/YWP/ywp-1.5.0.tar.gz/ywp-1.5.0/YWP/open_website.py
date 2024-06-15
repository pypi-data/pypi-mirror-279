import webbrowser

def open_website(url):
    try:
        webbrowser.open(url)
        return "opened"
    except Exception as e:
        print ("An error occurred:", e)
        return "An error occurred:", e