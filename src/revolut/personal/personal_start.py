from storage.data import *

class personalMenu():

    def createSession(self):

        clearConsole()
        Logger.normal("Starting session generator...")
        
        from revolut.personal.personal_session_gen import personalSessionGen
        personalSessionGen()

        while True:
            clearConsole()
            print(fg.rs + "Do you wan't to run the 3ds solver now (y,n)?")
            userInput = input("->  ")
            if userInput == "y" or userInput == "Y":
                self.solver()
            elif userInput == "n" or userInput == "N":
                break
            else:
                Logger.error("Please only use y or n")
                time.sleep(3)
                return

    def solver(self):

        clearConsole()
        Logger.normal("Starting 3ds solver...")

        from revolut.personal.personal_solver import personalSolver
        personalSolver()

    def __init__(self) -> None:
        
        while True:
            clearConsole()
            print("1.  Create revolut personal session")
            print("2.  Run revolut personal solver")
            userInput = input("->  ")
            try:
                if int(userInput) == 1:
                    self.createSession()
                    break
                elif int(userInput) == 2:
                    self.solver()
                    break
                else:
                    Logger.error("This is no option, choose 1 or 2")
                    time.sleep(3)
                    return
            except:
                Logger.error("Please only input numbers (1 or 2)")
                time.sleep(3)
                return
