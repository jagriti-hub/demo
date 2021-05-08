import sys, json, yaml
parameterfile = sys.argv[1]
envdeploymentfolder = sys.argv[2]
print(parameterfile)
f = open( parameterfile, "r") 
data = yaml.load(f, Loader=yaml.FullLoader)

parseparameter = open( envdeploymentfolder+"/paramyamltojson.json", "w+" )
parseparameter.write(json.dumps(data))
parseparameter.close()
