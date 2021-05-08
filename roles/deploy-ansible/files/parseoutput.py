import sys, json
tmpoutput = sys.argv[1]
finaloutput = sys.argv[2] 
f = open(tmpoutput, "r") 
data = json.load(f)
print(data['outputs'])
a={}
for output in data['outputs']:
    outputkey = output['OutputKey']
    outputvalue = output['OutputValue']
    a[outputkey] = outputvalue 
with open(finaloutput, "w+") as file_object:
    file_object.write(json.dumps(a))
    file_object.close()