def token_information(data, type='binance'):
    from .open_website import open_website

    if type == 'binance':
        link = "https://bscscan.com/token/" + str(data)
        open_website(link)
        return "opened"
    elif type == 'etherum':
        link = "https://etherscan.io/token/" + str(data)
        open_website(link)
        return "opened"
    elif type == 'geckoterminal':
        link = 'https://ywp.freewebhostmost.com/really/token.php?pool=' + str(data)
        return "opened"
    else:
        return "UnSupported type"