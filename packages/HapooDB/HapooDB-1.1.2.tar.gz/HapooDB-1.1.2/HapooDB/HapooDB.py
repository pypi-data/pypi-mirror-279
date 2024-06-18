import os



class HapooDB:


    def __init__(self,*title) -> None:
        self.variables = []
        if title:
            self.filename = f"{title[0]}.txt"
        else:
            self.filename = f"HapooDB.txt"
        try:
            try:
                with open(self.filename,"xt") as file:
                    pass

            except IndexError:
                with open(self.filename,"xt") as file:
                    pass
        except FileExistsError: 
            pass

    
    def destroyfile(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)
        else:
            print("!The file, {} does not exist".format(self.filename))

    def declare(self, key, val):
        with open(self.filename, "at") as self.file:
            self.file.write(f"{key}={val}\n")

    def access(self) -> dict:
        with  open(self.filename,"rt") as self.file:
            lines = [line.strip("\n") for line in self.file.readlines()]
            variables = {}
            for line in lines:
                line = [element for element in line.split("=")]
                variables[line[0]] = line[1]
            return variables  
      
    def accessSingle(self,key) -> str:
        key = str(key)
        with open(self.filename,"rt") as self.file:
            lines = [line.strip("\n") for line in self.file.readlines()]
            val = None
            for line in lines:
                if key in line:
                    val = line.split("=")[1]
                    break
                else:
                    continue
            try:
                return val.strip("\n")         
           
            except AttributeError:
                print("!There is no such of key in the DB.")
                return None


    def declareCluster(self,keyValPair:dict) -> None:
        with open(self.filename,"at") as self.file:
            content = list(keyValPair.items())
            for branchlist in content:
                self.file.write(f"{branchlist[0]}={branchlist[1]}\n")   



    def clearFile(self) -> None:
        with open(self.filename,"wt") as self.file:
            self.file.write('')


    def declareEncryption(self,key,value) -> None: 
        key = self.__private_Encrypt(key)
        value = self.__private_Encrypt(value)

        with  open(self.filename,"at") as self.file:
            self.file.write(f"{key}={value}\n")


    def accessEncryption(self,key):
        with open(self.filename,"rt") as self.file:
            lines = [line.strip("\n") for line in self.file.readlines()]
            val = None
            for line in lines:
                if self.__private_Encrypt(key) in line:
                    val = line.split("=")[1]
                else:
                    continue
            try:
                return self.__private_Decrypt(val.strip("\n"))
            except AttributeError:
                print("!There is no such of key in the DB.")
        ##todo
    def changeValue(self,key,changingValue):
        with open(self.filename,"rt") as self.file:
            lines = [line for line in self.file.readlines()]
        for index,line in enumerate(lines):
            if key in line:
                indexOfLine = index
                break
        lines[indexOfLine] = f"{key}={changingValue}\n"
        with open(self.filename, "w") as file: 
            file.write("".join(lines))  
            

    def __private_Encrypt(self,val):
        alphabets = [letter for letter in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"]
        EncodedMsg = []
        for letter in val:
            if letter in val:
                index = alphabets.index(letter)
                newPosition = (index + 3) % 62
                EncodedMsg.append(alphabets[newPosition])
            else:
                EncodedMsg.append(letter)
        return "".join(EncodedMsg)
    def __private_Decrypt(self,val):
        alphabets = [letter for letter in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"]
        EncodedMsg = []
        for letter in val:
            if letter in val:
                index = alphabets.index(letter)
                newPosition = (index - 3) % 62
                EncodedMsg.append(alphabets[newPosition])
            else:
                EncodedMsg.append(letter)
        return "".join(EncodedMsg)
    
    def Listen(self):
        _all_ =["DECLARE","ACCESS_SINGLE","QUIT"]
        print(_all_)

        while True:
            choice = input()
            choice = choice.split(" ")
            print(choice)
            if (x:=choice[0].upper()) == "DECLARE":
                self.declare(choice[1],choice[2])
                print(self.file.closed)
            elif x == "ACCESS_SINGLE":
                print(self.accessSingle(choice[1]))
            elif x == "QUIT":
                break
            


class Arlit:
    @staticmethod
    def CreateFile(name) -> None:
        try:
            with open(name,"xt") as f:
                pass
        except FileExistsError as e:
            pass

    @staticmethod
    def Evaluate(name) -> dict:
        variables = {}
        with open(name, "rt") as file:
            for line in file.readlines():
                line = line.strip("\n")
                variable = line.split("=")
                variables[variable[0]] = variable[1]
        return variables
                

    @staticmethod
    def update(name, variable: dict):
        string = "="
        with open(name,"wt") as f:
            for dictItem in variable.items():
                f.write(f"{string.join(dictItem)}\n")