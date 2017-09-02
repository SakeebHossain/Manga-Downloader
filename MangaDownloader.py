from MangaDownloaderClient import *
import time

client = MangaDownloaderClient()
start = 1

while True:
    
    # print the intro message
    if start == 1:
        start = 0
        print("###################### MangaDownloader ######################\n")
       
        print("Description:")
        print("An application that downloads manga! See 'help' for more details.\n")
        
        print("#############################################################")
        
    user_cmd = input("\n> ")    
    cmd = user_cmd.split(" ")    
        
    
    # if user needs help
    if (cmd[0] == "help"):
        print("###################### MangaDownloader ######################\n")
       
        print("Description:")
        print("An application that downloads manga!\n")
        print("Usage:\n")
        print("help")
        print("    Prints the usage guide.\n")        
        print("search [WORD]")
        print("    Find all manga titles containing [WORD] in its title.\n")
        print("info [TITLE]")
        print("    Prints manga details.\n")        
        print("download [TITLE] [OPTIONS]")
        print("    Downloads all the chapters of the manga with title [TITLE].\n")
        print("    [OPTIONS]:")
        print("        -all")
        print("              downloads all chapters of the manga")
        print("        -range [START] [END]")
        print("              downloads all chapters between [START] and [END]")
        print("        -only [n...]")
        print("              downloads all chapters numbers listed in [n...]\n")
        
        print("#############################################################")  
    
    # if you want info about the manga
    elif (cmd[0] == "info"):
        title = " ".join(cmd[1:])
        client.info(title)
        
    
    # search for a manga title
    elif (cmd[0] == "search"):
        search_terms = " ".join(cmd[1:])
        titles = client.search(search_terms)
        for title in titles:
            print("->", title)
    
    # download a manga title
    elif (cmd[0] == "download"):
        
        # identify the option
        # if option is -all
        if cmd[-1] == "-all":
            title = " ".join(cmd[1:-1])
            client.download_manga(title, ['*'])
            
        # if option is -only
        elif "-only" in cmd:
            ind = cmd.index("-only")
            title = " ".join(cmd[1:ind])
            chapter_list = cmd[ind+1:]
            client.download_manga(title, chapter_list)
            
        # if option is -range
        elif "-range" in cmd:
            ind = cmd.index("-range")
            title = " ".join(cmd[1:ind])
            start = cmd[-2] 
            end = cmd[-1]
            client.download_manga(title, [start, "-", end])
    
    # else, there's something wrong    
    else:
        print("Unrecognized command. See 'help' for more details.")