def open_website(url):
    import webbrowser
    try:
        webbrowser.open(url)
        return "opened"
    except Exception as e:
        print ("An error occurred:", e)
        return "An error occurred:", e