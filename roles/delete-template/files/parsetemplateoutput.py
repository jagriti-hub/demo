import sys, json
outputkey = sys.argv[1]
getEnvironment = sys.argv[2]
getoutputKey = sys.argv[3]
deployid = sys.argv[4]
templateworkfolder = sys.argv[5]
f = open(templateworkfolder + "/ENVIRONMENTS/" + deployid + "/output.json", "r") 
data = json.load(f)
toutputkey = getoutputKey + deployid
foutput={}
foutput[outputkey] =  data[toutputkey]
of = open(templateworkfolder + "/output.json", "w") 
odata = json.load(of)
odata.update(foutput)
of.write(json.dumps(odata))
of.close()
