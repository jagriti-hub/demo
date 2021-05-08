import sys, json, yaml, os
tempoutputyaml = sys.argv[1]
envoutjson = sys.argv[2]
filesize = os.path.getsize(tempoutputyaml)
if filesize != 0:
    f = open(tempoutputyaml, "r") 
    data = yaml.load(f, Loader=yaml.FullLoader)
of = open( envoutjson, "r") 
adata = json.load(of)
adata.update(data)
of = open( envoutjson, "w") 
of.write(json.dumps(adata))
of.close()
    
