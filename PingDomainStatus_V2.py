import requests
import csv
import re

DomainFile = "DomainRikkei/rikkei.org.txt"

def main(DomainFile):
    with open(DomainFile) as file:
        for domain in file:
            lines = file.readline()
        # isDomain = re.compile(r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
    # isDomain = re.compile(r"^([a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5})")
            CheckDomain = re.findall(r"^([a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5})", lines)

            print(CheckDomain)





main(DomainFile)