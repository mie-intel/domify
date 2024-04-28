import sys
import os
import shutil
import glob
from colorama import Fore, Back, Style

"""
Parameters
"""

# Problem data contain all data about the problem

path = ""
package_path = "package"
required_file = ["runner", "solution", "tc"]
sample_testcases = []
testcases = []

problem_data = {
    "name": "default",
    "code": "A",
    "timelimit": "",
    "memorylimit": "",
    "color": "#FFFFFF",
}

def startMessage(message):
    print(Fore.YELLOW + "START: " + Style.RESET_ALL + message)

def successMessage(message):
    print(Fore.GREEN + "SUCCESS: " + Style.RESET_ALL + message + "\n")

def fileCreatedMessage(title):
    print(Fore.BLUE + "CREATED: " + Style.RESET_ALL + title)

def errorAndTerminate(warning):
    print(Fore.RED + warning + Style.RESET_ALL)
    exit(0)

def checkAvailability():
    # Creating path, and package_path
    global path, package_path, problem_data
    global sample_testcases, testcases

    if len(sys.argv) != 2:
        errorAndTerminate(f"Expected 2 arguments found {len(sys.argv)}")

    splitter_list = ["/", "\\"]
    splitter = ""
    for splitter_item in splitter_list:
        if splitter_item in sys.argv[1]:
            splitter = splitter_item
            break
    path_argument = sys.argv[1].split(splitter)
    path = os.getcwd()
    for item in path_argument:
        path = os.path.join(path, item)
    package_path = os.path.join(path, package_path)

    list_file = os.listdir(path)

    for file in required_file:
        if file not in list_file:
            errorAndTerminate(f"{file} file is not available in {sys.argv[1]}!")
    
    # Checking testcase validity
    list_testcases = os.listdir(os.path.join(path, "tc"))
    if len(list_testcases) % 2 == 1:
        errorAndTerminate("There are only odd numbers of files")
    
    for testcase in list_testcases:
        old_name = testcase.split('_')
        is_sample = ("sample" in old_name)
        is_out = False
        new_name = list(old_name)
        new_name[-1] = new_name[-1].split('.')
        # Renaming
        if new_name[-1][-1] == "out":
            new_name[-1] = new_name[-1][0] + '.ans'
            is_out = True
        else:
            new_name[-1] = '.'.join(new_name[-1])

        new_name = '_'.join(map(str, new_name))
        old_name = '_'.join(map(str, old_name))

        if is_out:
            os.rename(os.path.join(path, "tc", old_name), os.path.join(path, "tc", new_name))
            pass
        
        if is_sample:
            sample_testcases.append(new_name)
        else:
            testcases.append(new_name)

def initialize():
    """
    Initialize everything
        problem_data, etc
    """
    global path, package_path, problem_data

    startMessage("Input Problem Data")
    name        = input("Enter problem name    : ")
    code        = input("Enter problem code    : ")
    timelimit   = input("Enter timelimit (s)   : ")
    memorylimit = input("Enter memorylimit (kb): ")
    color       = input("Enter color (#HEX)    : ")

    if not bool(name):
        errorAndTerminate("Problem must have a name")

    problem_data = {
        "name": name if bool(name) else problem_data["name"],
        "code": code if bool(code) else problem_data["code"],
        "timelimit": timelimit if bool(timelimit) else problem_data["timelimit"],
        "memorylimit": memorylimit if bool(memorylimit) else problem_data["memorylimit"],
        "color": color if bool(color) else problem_data["color"],
    }

    # Hapus folder package kalo ada
    if os.path.exists(package_path):
        shutil.rmtree(package_path)

    # Bikin folder package
    os.mkdir(package_path)

    successMessage("Initializing data")

def createIniFile():
    """
    Create domjudge-problem.ini file
    """
    startMessage("creating domjudge-problem.ini file")
    
    global problem_data
    text = ""

    def add_argument(arg):
        if bool(problem_data[arg]):
            return f"{arg}=\'{problem_data.get(arg)}\'\n"
        else:
            return ""
    
    text = text + add_argument("timelimit")
    text = text + add_argument("memorylimit")
    text = text + add_argument("color")
    
    with open(os.path.join(package_path, "domjudge-problem.ini"), "w") as domjudgeini:
        domjudgeini.write(text)

    fileCreatedMessage("domjudge-problem.ini")
    print("=====================")
    print(text[:-1:])
    print("=====================")
    successMessage("domjudge-problem.ini file has been created successfully!")

def createProblemYaml():
    """
    Create problem.yaml file
    """
    startMessage("creating problem.yaml file")
    global problem_data
    text = ""

    def add_argument(arg):
        if bool(problem_data[arg]):
            return f"{arg}: \"{problem_data.get(arg)}\"\n"
        else:
            return ""
    
    text = text + add_argument("name")
    
    with open(os.path.join(package_path, "problem.yaml"), "w") as domjudgeini:
        domjudgeini.write(text)
    
    fileCreatedMessage("problem.yaml")
    print("=====================")
    print(text[:-1:])
    print("=====================")
    successMessage("problem.yaml file has been created successfully!")

def generateTestCase():
    """
    Moving Test Case
    """
    startMessage("Moving testcase files")
    # Remove folder if exists
    if os.path.exists(os.path.join(path, "package", "data")):
        shutil.rmtree(os.path.join(path, "package", "data"))

    # Create folder
    os.makedirs(os.path.join(path, "package", "data", "sample"))
    os.makedirs(os.path.join(path, "package", "data", "secret"))

    # Moving sample testcases
    if len(sample_testcases):
        print("\n[ SAMPLE TEST CASES ]")
        print("/tc -> /package/data/sample")
    for test in sample_testcases:
        src = os.path.join(path, "tc", test)
        dest = os.path.join(path, "package", "data", "sample", test)
        shutil.move(src, dest)
        print(" ", test)
    
    # Moving testcases
    if len(sample_testcases):
        print("\n[ SECRET TEST CASES ]")
        print("/tc -> /package/data/secret")
    for test in testcases:
        src = os.path.join(path, "tc", test)
        dest = os.path.join(path, "package", "data", "secret", test)
        shutil.move(src, dest)
        print(" ", test)
    
    # delete /tc
    shutil.rmtree(os.path.join(path, "tc"))
    successMessage("finish moving all testcase files")

checkAvailability()
initialize()
createIniFile()
createProblemYaml()
generateTestCase()

print(Fore.GREEN + "FINISH: " + Style.RESET_ALL + "Your domjudge package is ready")
