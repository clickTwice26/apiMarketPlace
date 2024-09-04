from colorama import Back, Fore, Style, init

def cout(**kwargs):
    coutData = kwargs
    message = coutData.get('message', "no message given")
    category = coutData.get('category', "info")
    categoryFontColor = {
        "info": Fore.CYAN,
        "success" : Fore.GREEN,
        "error" : Fore.RED
    }
    # print(category)
    categoryFontColor = categoryFontColor.get(category)
    # print(categoryFontColor + "hello")
    print("[+] "+categoryFontColor + " " + category + Style.RESET_ALL + " " + message)
    # print(message)
    
    
if __name__ == "__main__":
    init()
    cout(message="Program Started without any error", category="error")
    # cout()
