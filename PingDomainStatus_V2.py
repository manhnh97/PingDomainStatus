import requests
import csv
from datetime import datetime
import re
import urllib3

# ==> Enter File Domain <==
DomainFile = "DomainRikkei/DomainAllinOne.txt"
chunkSize = 3

def DomainStatusCheck(DomainFile):
    data = []
    for domain in FilterDomain(DomainFile):
        try:
            domain = domain.strip('\n')
            print(domain)
            # """
            nowDateTime = datetime.now().strftime("%D %H:%M:%S")
            if 'http' not in domain:
                prefixDomain = 'http://'
                domainCheck = prefixDomain+domain
                DomainStatus = Domain_StatusCode(domainCheck)
                if DomainStatus == 200:
                    data.append([nowDateTime, domainCheck, DomainStatus])
                else:
                    prefixDomain = 'https://'
                    domainCheck = prefixDomain+domain
                    DomainStatus = Domain_StatusCode(domainCheck)
                    if DomainStatus == 200:
                        data.append([nowDateTime, domainCheck, DomainStatus])
                    else:
                        prefixDomain = 'http://www.'
                        domainCheck = prefixDomain+domain
                        DomainStatus = Domain_StatusCode(domainCheck)
                        if DomainStatus == 200:
                            data.append([nowDateTime, domainCheck, DomainStatus])
                        else:
                            prefixDomain = 'https://www.'
                            domainCheck = prefixDomain+domain
                            DomainStatus = Domain_StatusCode(domainCheck)
                            if DomainStatus == 200:
                                data.append([nowDateTime, domainCheck, DomainStatus])
                            else:
                                data.append([nowDateTime, domainCheck, DomainStatus])
            # """
        except ConnectionError:
            print(ConnectionError)

    return data

def Domain_StatusCode(domainCheck):
    http = urllib3.PoolManager()
    r = http.request('GET', domainCheck)
    DomainStatus = r.status
    print(DomainStatus)
    return DomainStatus

def FilterDomain(DomainFile):
    regex = re.compile(r"(^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?)$|([a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5})")
    with open(DomainFile, 'r') as infile:
        for domain in infile:
            domain = domain.strip('\n')
            result = regex.match(domain)
            if result != None:
                dataDomain = result.group()
                # dataDomain = set(result.group())
                yield dataDomain

def main(DomainFile, chunkSize):
    # open results file and write header
    try:
        rfile = open('results.csv', 'w+', newline='')
        dataWriter = csv.writer(rfile, delimiter = ',')
        header = ['Scan Date', 'Domain', 'Status']
        dataWriter.writerow(header)

    except IOError as ioerr:
        print('Please ensure the file is closed.')
        print(ioerr)

    ResultDataDomain = DomainStatusCheck(DomainFile)
    for data in ResultDataDomain:
        dataWriter.writerow(data)

main(DomainFile, chunkSize)
