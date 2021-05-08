import sys, json, yaml, os
import pathlib
templateinput = sys.argv[1]
templateoutput = sys.argv[2]
templatefolder = sys.argv[3]
of = open( templateinput, "r") 
data = yaml.load(of, Loader=yaml.FullLoader)
print(data)
EnvironmentsOut = []
for Environment in data["Environments"]:
  envparameterfile = templatefolder + "/" + Environment["DeployId"] + ".j2"
  pfile = pathlib.Path(envparameterfile)
  if pfile.exists ():
    ef = open( envparameterfile, "r") 
    paramdata = yaml.load(ef, Loader=yaml.FullLoader)
    Environment["Inputs"] = paramdata
  envoutputfile = templatefolder + "/" + Environment["DeployId"] + "-output.j2"
  ofile = pathlib.Path(envoutputfile)
  if ofile.exists ():
    outf = open( envoutputfile, "r") 
    outdata = yaml.load(outf, Loader=yaml.FullLoader)
    Environment["Outputs"] = outdata
  EnvironmentsOut.append(Environment)
data["Environments"] = EnvironmentsOut
tf = open( templateoutput, "w") 
tf.write(json.dumps(data))
tf.close()
    
