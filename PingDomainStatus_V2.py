import requests
import csv
from datetime import datetime
import re
import urllib3

# ==> Enter File Domain <==
DomainFile = "DomainRikkei/DomainAllinOne.txt"

def FilterDomain(DomainFile):
    regex = re.compile(r"(^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?)$|([a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5})")
    listDomain = []
    with open(DomainFile, 'r') as infile:
        for domain in infile:
            domain = domain.strip('\n')
            result = regex.match(domain)
            if result != None:
                dataDomain = result.group()
                listDomain.append(dataDomain)

    domainUnique = set(listDomain)
    return domainUnique

def DomainStatusCheck():
    # open results file and write header
    try:
        rfile = open('results.csv', 'w+', newline='')
        dataWriter = csv.writer(rfile, delimiter = ',')
        header = ['Scan Date', 'Domain', 'Status', 'Comment']
        dataWriter.writerow(header)

    except IOError as ioerr:
        print('Please ensure the file is closed.')
        print(ioerr)

    urllib3.disable_warnings()
    i = 1
    for domain in FilterDomain(DomainFile):
        try:
            if "http" not in domain:
                url = "https://"+domain
            else:
                url = domain

            r = requests.get(url, verify=False)
            DomainStatus = r.status_code

            # Comment Domain
            if DomainStatus >= 100 and DomainStatus < 200:
                Comment = "Informational Response – the request was received, continuing process"
            elif DomainStatus >= 200 and DomainStatus < 300:
                Comment = "Successful – the request was successfully received, understood, and accepted"
            elif DomainStatus >= 300 and DomainStatus < 400:
                Comment = "Redirection – further action needs to be taken in order to complete the request"
            elif DomainStatus >= 400 and DomainStatus < 500:
                Comment = "Client Error – the request contains bad syntax or cannot be fulfilled"
            elif DomainStatus >= 500 and DomainStatus < 600:
                Comment = "Server Error – the server failed to fulfil an apparently valid request"
            else:
                Comment = "Unknown Error"

            print("Checking {0}: {1} => {2}".format(i, url, DomainStatus))

            nowDateTime = datetime.now().strftime("%D %H:%M:%S")

            data = [nowDateTime, url, DomainStatus, Comment]

            # yield data
            dataWriter.writerow(data)

            i += 1
        except requests.exceptions.ConnectionError:
            continue
        except KeyboardInterrupt:
            break

DomainStatusCheck()
