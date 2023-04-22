
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

def generateVarFile(csvFileName="data.csv"):
    oneTab = "\n  "
    twoTab = "\n    "
    threeTab = "\n      "

    variables = """routers:"""

    with open(csvFileName,"r") as csvFile:
        csvFileReader = csv.DictReader(csvFile)
        #next(csvFileReader)
        interfaces=""
        loopbacks=""
        ospfProcess={}

        uniqueRouters = {}
        #iteration=0
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

    variables+=interfaces
    variables+=loopbacks
    if ospfProcess:
        variables+= oneTab+"  ospf:"
        for process in ospfProcess.keys():
            variables+= twoTab+"- processID: "+process
            variables+= twoTab+"  networks:"
            for ipAddress,area in ospfProcess[process]:
                 variables+= threeTab+"- "+getIPandSubnet(ipAddress,wildcard=True)+" area "+area

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
    tasks += "\n    become: true"
    tasks += "\n    template: src=backboneRouter.j2 dest=/home/mandharek/finalProject/Nexus-Repo/{{ item.hostname }}.conf"
    tasks += "\n    with_items: \"{{ routers }}\""
    with open("isp-backbone/tasks/main.yml","w") as t:
        t.write(tasks)

    with open("isp-backbone/backboneISPTopology.yml","w") as t:
        t.write(finalPlay)

generateVarFile()
generatePlayBook()
