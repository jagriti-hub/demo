import sys, json, yaml
parameterfile = sys.argv[1]
dependentoutputfile = sys.argv[2]
dependenttemplateid = sys.argv[3]
f = open( parameterfile, "r") 
data = yaml.load(f, Loader=yaml.FullLoader)
tf = open( dependentoutputfile, "r")
odata = yaml.load(tf, Loader=yaml.FullLoader)
data[dependenttemplateid] = odata
ofw = open(parameterfile, "w") 
ofw.write(yaml.dump(data))
ofw.close()
