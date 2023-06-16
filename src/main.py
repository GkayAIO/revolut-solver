from storage.data import *
while True:
    clearConsole()
    print("Made by: `gkay`")
    print("      ____                  __      __     _____       __               ")
    print("     / __ \___ _   ______  / /_  __/ /_   / ___/____  / /   _____  _____")
    print("    / /_/ / _ \ | / / __ \/ / / / / __/   \__ \/ __ \/ / | / / _ \/ ___/")
    print("   / _, _/  __/ |/ / /_/ / / /_/ / /_    ___/ / /_/ / /| |/ /  __/ /    ")
    print("  /_/ |_|\___/|___/\____/_/\__,_/\__/   /____/\____/_/ |___/\___/_/     \n")
    print("1.  Revolut personal")
    print("2.  Revolut business")
    userInput = input("->  ")
    try:
        if int(userInput) == 1:
            from revolut.personal.personal_start import personalMenu
            personalMenu()
        if int(userInput) == 2:
            from revolut.business.business_start import businessMenu
            businessMenu()
        else:
            Logger.error("Please only use 1 and 2")
            time.sleep(3)
            continue
    except:
        Logger.error("Please only input numbers, no letters")
        time.sleep(3)
        continue
