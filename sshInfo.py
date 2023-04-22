import csv,sys


#this returns a list of list specifying all details in the csv
def fetchConnectionParameter(fileName="MgmtDetails.csv"):
    routers=[]
    try:
        with open(fileName,mode='r') as file:
            routerList=csv.reader(file)
            headers = next(routerList, None)
            for router in routerList:
                r={
                    'device_type': router[6],
                    'host': router[1],
                    'username':router[2],
                    'password':router[3],
                    'secret': router[4],
                    'port':router[5]
                }
                routers.append(r)
            return routers
    except FileNotFoundError:
        print("File not found at the path : "+file)
        sys.exit()
    except Exception as e:
        print(e)
        sys.exit()

def getHostNames(fileName="MgmtDetails.csv"):
    hostnames=[]
    try:
        with open(fileName,mode='r') as file:
            routerList=csv.reader(file)

            for router in routerList:
                hostnames.append(router[0])
            return hostnames
    except FileNotFoundError:
        print("file not found at the path : "+file)
        sys.exit()
    except Exception as e:
        print(e)
        sys.exit()

fetchConnectionParameter()