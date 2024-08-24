import re
import sys
import time
import requests
from bs4 import BeautifulSoup
import yaml
import threading
import os
from colorama import Fore, init
import datetime
import random
import numpy as np

# Colors here
init()
os.system("color")
white = Fore.WHITE
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
cyan = Fore.CYAN
magenta = Fore.MAGENTA
blue = Fore.BLUE

colors = (white, yellow, cyan, magenta, blue)
color = random.choice(colors)
# ----------------------------------------------------------------------

# annotations here
plus = white + "     [" + green + "+" + white + "] "
minus = white + "     [" + red + "-" + white + "] "
info = white + "     [" + color + "*" + white + "] "
warn = white + "     [" + yellow + "!" + white + "] "
ask = white + "     [" + cyan + "?" + white + "] "
rightBracket = white + "     ["
leftBracket = white + " ["
closeBracket = white + "] "
# ----------------------------------------------------------------------

# List here
targets = []
allConfigs = []
config1 = []
config2 = []
totalConfigs = []
# -----------------------------------------------------------------------

# All functions here!


def target(site):
    if site.startswith("http://") is True:
        if site.endswith("/") is True:
            site = site[:-1]
            targets.append(site)
        else:
            targets.append(site)
    elif site.startswith("https://") is True:
        if site.endswith("/") is True:
            site = site[:-1]
            targets.append(site)
        else:
            targets.append(site)
    else:
        site = "http://" + site
        if site.endswith("/") is True:
            site = site[:-1]
            targets.append(site)
        else:
            targets.append(site)


def configs(files):
    op = open(files, 'r')
    load = yaml.load(op, Loader=yaml.FullLoader)
    name = load['name']
    for url in load['url']:
        method = load['method']
        if method == "get" or method == "GET":
            status = load['matchers']['status']
            regex = load['matchers']['regex']
            allConfigs.append({"name": name, "url": url, "status": status, "regex": regex})
        elif method == "POST" or method == "POST":
            data = load['data']
            status = load['matchers']['status']
            regex = load['matchers']['regex']
            allConfigs.append({"name": name, "url": url, "data": data, "status": status, "regex": regex})
        else:
            pass

def get(name, url, status, regex):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == status:
            if regex == "":
                op = open("output/output.txt", 'a')
                op.write(url + " [" + name + "]")
                print(plus + green + url + leftBracket + green + name + closeBracket)
                op.close()
            else:
                find = re.search(regex, response.text)
                if str(find.group()) == regex:
                    op = open("output/output.txt", 'a')
                    op.write(url + " [" + name + "]")
                    print(plus + green + url + leftBracket + green + name + closeBracket)
                    op.close()
                else:
                    print(minus + color + url + leftBracket + red + "Request Sent" + closeBracket)
        else:
            print(minus + color + url + leftBracket + red + "Request Sent" + closeBracket)
    except ConnectionError as e:
        print(minus + color + url + leftBracket + red + "Request Sent" + closeBracket)


def post(name, url, data, status, regex):
    try:
        response = requests.post(url, data=data, timeout=2)
        if response.status_code == status:
            if regex == "":
                op = open("output/output.txt", 'a')
                op.write(url + " [" + name + "]")
                print(plus + green + url + leftBracket + green + name + closeBracket)
                op.close()
            else:
                find = re.search(regex, response.text)
                if str(find.group()) == regex:
                    op = open("output/output.txt", 'a')
                    op.write(url + " [" + name + "]")
                    print(plus + green + url + leftBracket + green + name + closeBracket)
                    op.close()
                else:
                    print(minus + color + url + leftBracket + red + "Request Sent" + closeBracket)
        else:
            print(minus + color + url + leftBracket + red + "Request Sent" + closeBracket)
    except ConnectionError as e:
        print(minus + color + url + leftBracket + red + "Request Sent" + closeBracket)


def task1():
    for venom in config1:
        print(venom)
        for targeturl in targets:
            if venom["method"] == "get" or venom["method"] == "GET":
                url = targeturl + venom["urls"]
                get(venom["name"], url, venom["status"], venom["regex"])
            elif venom["method"] == "post" or venom["method"] == "POST":
                url = targeturl + venom["urls"]
                post(venom["name"], url, venom["data"], venom["status"], venom["regex"])
            else:
                pass


def task2():
    for venom in config2:
        print(venom)
        for targeturl in targets:
            if venom["method"] == "get" or venom["method"] == "GET":
                url = targeturl + venom["urls"]
                get(venom["name"], url, venom["status"], venom["regex"])
            elif venom["method"] == "post" or venom["method"] == "POST":
                url = targeturl + venom["urls"]
                post(venom["name"], url, venom["data"], venom["status"], venom["regex"])
            else:
                pass


# ----------------------------------------------------------------------------------------
# Target Formatting
isList = ""
isList += ask + color + "Do you have the target list?\n"
isList += rightBracket + green + "1" + closeBracket + green + "Yes\n"
isList += rightBracket + green + "2" + closeBracket + green + "No\n"
print(isList)
choice = input(plus + color + "Enter an option to continue: ")

if choice == "1":
    targetList = input(plus + "Enter the target list path: ")
    print(" ")
    if os.path.exists(targetList) is True:
        file = open(targetList, 'r').readlines()
        print(white + color + "File Found: " + green + "True")
        print(white + color + "Total Targets: " + green + str(len(file)))
        for sites in file:
            target(sites)
    else:
        print(minus + red + "File not found! Exiting Now! Bye!")
        time.sleep(30)
        sys.exit()
elif choice == "2":
    targetList = input(plus + color + "Enter the target: ")
    target(targetList)
else:
    print(minus + red + "I don't understand you! Exiting Now!! Bye!")
    time.sleep(30)
    sys.exit()
# ----------------------------------------------------------------------------

exploitList = ""
exploitList += rightBracket + "1" + closeBracket + color + "Cnvd and Cves\n"
exploitList += rightBracket + "2" + closeBracket + color + "Logins and Panels\n"
exploitList += rightBracket + "3" + closeBracket + color + "Files and tokens Exposures\n"
exploitList += rightBracket + "4" + closeBracket + color + "Fuzzing!\n"
exploitList += rightBracket + "5" + closeBracket + color + "Security Misconfigurations!\n"
exploitList += rightBracket + "6" + closeBracket + color + "Takeover\n"
exploitList += rightBracket + "7" + closeBracket + color + "Vulnerabilities\n"
exploitList += rightBracket + "8" + closeBracket + color + "All\n"
print(exploitList)
print(" ")
choice = input(plus + color + "Enter an option to continue: ")
if choice == "1":
    os.chdir("configs/cnvd&cve")
    config = os.listdir()
    for file in config:
        configs(file)
    if __name__ == "__main__":
        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Done!")
elif choice == "2":
    os.chdir("configs/login&panels")
    config = os.listdir()
    for file in config:
        configs(file)
    if __name__ == "__main__":
        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Done!")
elif choice == "3":
    os.chdir("configs/file&tokens")
    config = os.listdir()
    for file in config:
        configs(file)
    if __name__ == "__main__":
        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Done!")
elif choice == "4":
    os.chdir("configs/fuzzing")
    config = os.listdir()
    for file in config:
        configs(file)
    if __name__ == "__main__":
        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Done!")
elif choice == "5":
    os.chdir("configs/misconfig")
    config = os.listdir()
    for file in config:
        configs(file)
    if __name__ == "__main__":
        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Done!")
elif choice == "6":
    os.chdir("configs/takeover")
    config = os.listdir()
    for file in config:
        configs(file)
    if __name__ == "__main__":
        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Done!")
elif choice == "7":
    os.chdir("configs/vulnerabilities")
    config = os.listdir()
    for file in config:
        configs(file)
    if __name__ == "__main__":
        t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Done!")
elif choice == "8":
    os.chdir("configs/all")
    config = os.listdir()
    for file in config:
        configs(file)
    print(allConfigs)
else:
    print(minus + red + "I don't understand you! Exiting now! Bye!")
    time.sleep(30)
    sys.exit()


# new 