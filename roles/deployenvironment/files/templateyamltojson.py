import sys, json, yaml, os
from demjson import decode
yamlfile = sys.argv[1]
jsonfile = sys.argv[2]
f = open(yamlfile, "r") 
data = yaml.load(f, Loader=yaml.FullLoader)
outjson = {}
for key,value in data.items():
    try:
        ovalue = decode(value)
        outjson[key] = ovalue
    except:
        outjson[key] = value
of = open(jsonfile, "w") 
of.write(json.dumps(outjson))
of.close()

    