import requests
import csv
from datetime import datetime

# ==> Enter File Domain <==
DomainFile = "DomainFile.txt"


def DomainStatusCheck(domain):
    if "http" not in domain:
        url = "https://"+domain
    else:
        url = domain
    r = requests.get(url)
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

    print("Checking: {0} => {1}".format(url, DomainStatus))

    nowDateTime = datetime.now().strftime("%D %H:%M:%S")

    data = [nowDateTime, url, DomainStatus, Comment]
    
    return data
    

def main(DomainFile):
    # open results file and write header
    try:
        rfile = open('results.csv', 'w+', newline='')
        dataWriter = csv.writer(rfile, delimiter = ',')
        header = ['Scan Date', 'Domain', 'Status', 'Comment']
        dataWriter.writerow(header)

    except IOError as ioerr:
        print('Please ensure the file is closed.')
        print(ioerr)

    ##### CHANGE TO TEXT FILE PATH. ONE DOMAIN PER LINE! #####
    try:
        # read domains from file and pass them to DomainStatusCheck
        with open(DomainFile, 'r') as infile:  # keeping the file open because it shouldnt
                                                # be opened/modified during reading anyway
            for domain in infile:
                domain = domain.strip('\n')
                try:
                    data = DomainStatusCheck(domain)
                    if data:
                        dataWriter.writerow(data)
                except Exception as err:  # keeping it
                    print('Encountered an error but scanning will continue.', err)

    except IOError as ioerr:
        print('Please ensure the file is closed.')
        print(ioerr)
