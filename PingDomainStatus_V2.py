import requests
import csv
from datetime import datetime

# ==> Enter File Domain <==
DomainFile = "DomainTest.txt"
chunkSize = 3

def DomainStatusCheck(DomainFile):
    data = []
    with open(DomainFile) as infile:
        for domain in infile:
            domain = domain.strip('\n')
            nowDateTime = datetime.now().strftime("%D %H:%M:%S")
            if 'http' not in domain:
                prefixDomain = 'http://'
                domainCheck = prefixDomain+domain
                DomainStatus = Domain_StatusCode(domainCheck)
                if DomainStatus == 200:
                    data.append([nowDateTime, domainCheck, DomainStatus])
                    continue
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

    return data

def Domain_StatusCode(domainCheck):
    r = requests.get(domainCheck)
    DomainStatus = r.status_code
    return DomainStatus

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