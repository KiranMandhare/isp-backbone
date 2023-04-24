
import csv,yaml


def getIPandSubnet(ipaddress,wildcard=False):
    subnetMask={
      "32": "255.255.255.255",
      "24": "255.255.255.0",
      "30": "255.255.255.252",
    }
    invertedSubnetMask = {
      "32": "0.0.0.0",
      "24": "0.0.0.255",
      "30": "0.0.0.3"
    }
    ip = ipaddress.split("/")[0]
    subnet  = ipaddress.split("/")[1]

    if wildcard:
        return ip+" "+invertedSubnetMask[subnet]
    else:
        return ip+" "+subnetMask[subnet]

def generateVarFile(OSPFcsvFileName="ospfConfig.csv",BGPPeeringcsvFileName="bgpConfig.csv", BGPAdvcsvFileName="bgpAdvConfig.csv"):
    oneTab = "\n  "
    twoTab = "\n    "
    threeTab = "\n      "

    variables = """routers:"""

    with open(OSPFcsvFileName,"r") as csvFile:
        csvFileReader = csv.DictReader(csvFile)
        #next(csvFileReader)
        interfaces=""
        loopbacks=""
        ospfProcess={}
        bgp={}
        uniqueRouters = {}
        #iteration=0
        currentRouter = ""
        for row in csvFileReader:
            #print(str(iteration)+"  "+str(uniqueRouters))
            #iteration+=1
            if row["Hostname"] not in uniqueRouters:
                uniqueRouters[row["Hostname"]] = True
                variables+=interfaces
                variables+=loopbacks
                if ospfProcess:
                    variables+= oneTab+"  ospf:"
                    for process in ospfProcess.keys():
                        variables+= twoTab+"- processID: "+process
                        variables+= twoTab+"  networks:"
                        for ipAddress,area in ospfProcess[process]:
                            variables+= threeTab+"- "+getIPandSubnet(ipAddress,wildcard=True)+" area "+area

                    #bgp config addition
                    variables+= oneTab+"  bgp:"
                    with open(BGPPeeringcsvFileName,"r") as bgpCSVFile:
                        bgpCSVFileReader = csv.DictReader(bgpCSVFile)
                        ASNumber=False
                        for bgpRow in bgpCSVFileReader:
                            print(bgpRow)
                            print(currentRouter)
                            print(bgpRow['Hostname'])
                            if currentRouter == bgpRow['Hostname']:
                                if ASNumber is False:
                                    ASNumber=True
                                    variables+= twoTab+"- ASNumber: "+bgpRow['ASNumber']
                                    variables+= twoTab+"  neighbors:"
                                
                                variables+= threeTab+"- "+bgpRow['NeighborIP']+" remote-as "+bgpRow['NeighborAS']
                                variables+= threeTab+"- "+bgpRow['NeighborIP']+" update-source loopback 0"
                                if bgpRow['ASNumber'] !=  bgpRow['NeighborAS']:
                                    #ebgp
                                    variables+= threeTab+"- "+bgpRow['NeighborIP']+" ebgp-multihop "+bgpRow['TTL'] 
                            #print(variables)
                    with open(BGPAdvcsvFileName,"r") as bgpCSVFile:
                        bgpCSVFileReader = csv.DictReader(bgpCSVFile)
                        networks = False
                        for bgpRow in bgpCSVFileReader:
                            if currentRouter == bgpRow['Hostname']:
                                if networks is False:
                                    networks= True
                                    variables+= twoTab+"  networks:"
                                generatedIPandSubnet = getIPandSubnet(bgpRow['NetworkToAdvertise']).split()
                                variables+= threeTab+"- "+generatedIPandSubnet[0]+" mask "+generatedIPandSubnet[1]

                variables  += oneTab+"- hostname: "+row["Hostname"]
                variables  += oneTab+"  enable_secret: password"
                interfaces = oneTab+"  interfaces:"
                loopbacks  = oneTab+"  loopbacks:"
                ospfProcess = {}


            if row["Interface Type"] == "Loopback":
                print(row["Interface Type"])
                loopbacks += twoTab + "- name: "+row["Interface Name"]
                loopbacks += twoTab + "  ip: "+getIPandSubnet(row["IP/Subnet"])
            else:
                interfaces+= twoTab + "  "+row["Interface Type"]+row["Interface Name"]+": "+getIPandSubnet(row["IP/Subnet"])

            if row["OSPF Enabled"] == "Yes":
                if row["OSPF Process Id"] not in ospfProcess:
                    ospfProcess[row["OSPF Process Id"]] = []
                    ospfProcess[row["OSPF Process Id"]].append((row["IP/Subnet"],row["OSPF Area"]))
                else:
                    ospfProcess[row["OSPF Process Id"]].append((row["IP/Subnet"],row["OSPF Area"]))
            currentRouter=row["Hostname"]

    variables+=interfaces
    variables+=loopbacks
    if ospfProcess:
        variables+= oneTab+"  ospf:"
        for process in ospfProcess.keys():
            variables+= twoTab+"- processID: "+process
            variables+= twoTab+"  networks:"
            for ipAddress,area in ospfProcess[process]:
                 variables+= threeTab+"- "+getIPandSubnet(ipAddress,wildcard=True)+" area "+area
        
        #bgp config addition
        with open(BGPPeeringcsvFileName,"r") as bgpCSVFile:
            bgpCSVFileReader = csv.DictReader(bgpCSVFile)
            ASNumber=False
            for bgpRow in bgpCSVFileReader:
                if currentRouter == bgpRow['Hostname']:
                    if ASNumber is False:
                        ASNumber=True
                        variables+= twoTab+"- ASNumber: "+bgpRow['ASNumber']
                        variables+= twoTab+"  neighbors:"
                    
                    variables+= threeTab+"- "+bgpRow['NeighborIP']+" remote-as "+bgpRow['NeighborAS']
                    variables+= threeTab+"- "+bgpRow['NeighborIP']+" update-source loopback 0"
                    if bgpRow['ASNumber'] !=  bgpRow['NeighborAS']:
                        #ebgp
                        variables+= threeTab+"- "+bgpRow['NeighborIP']+" ebgp-multihop "+bgpRow['TTL'] 
          
          
        with open(BGPAdvcsvFileName,"r") as bgpCSVFile:
            bgpCSVFileReader = csv.DictReader(bgpCSVFile)
            networks = False
            for bgpRow in bgpCSVFileReader:
                if currentRouter == bgpRow['Hostname']:
                    if networks is False:
                        networks= True
                        variables+= twoTab+"  networks:"
                    generatedIPandSubnet = getIPandSubnet(bgpRow['NetworkToAdvertise']).split()
                    variables+= threeTab+"- "+generatedIPandSubnet[0]+" mask "+generatedIPandSubnet[1]

    with open("isp-backbone/vars/main.yml","w") as vars:
        vars.write(variables)

def generatePlayBook():

    finalPlay  = "\n- name: Generate Configs"
    finalPlay += "\n  hosts: routers"
    finalPlay += "\n  become: yes"
    finalPlay += "\n  become_user: root"
    finalPlay += "\n  roles:"
    finalPlay += "\n  - isp-backbone"

    tasks  = "---"
    tasks += "\n  - name: Generate Router Config"
    tasks += "\n    template: src=backboneRouter.j2 dest={{ item.hostname }}.conf"
    tasks += "\n    with_items: \"{{ routers }}\""    
    with open("isp-backbone/tasks/main.yml","w") as t:
        t.write(tasks)

    with open("isp-backbone/backboneISPTopology.yml","w") as t:
        t.write(finalPlay)

generateVarFile()
generatePlayBook()
