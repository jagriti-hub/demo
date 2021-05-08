import sys, json
deploymentid = sys.argv[1]
Environmenthome = sys.argv[2] 
dependentdeploymentid = sys.argv[3]
GetOutputKey = sys.argv[4]
ParameterKey = sys.argv[5]
f = open(Environmenthome + "/workfolder/" + dependentdeploymentid + "/output.json", "r") 
data = json.load(f)
outputkey=GetOutputKey + dependentdeploymentid
outputvalue=data[outputkey]
with open(Environmenthome + "/workfolder/" + deploymentid + "/dependentparameter.yaml", "a+") as file_object:
    file_object.seek(0)
    data = file_object.read(100)
    if len(data) > 0 :
        file_object.write("\n")
    file_object.write(ParameterKey + deploymentid + ': ' + outputvalue)
    file_object.close()
