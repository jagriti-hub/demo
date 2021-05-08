import yaml, sys, json
from cfn_flip import flip, to_yaml, to_json
from jinja2 import Environment, FileSystemLoader, Template 
deploymentid=sys.argv[1]
Environmentname=sys.argv[2]
Environmenthome=sys.argv[3]
outputpath = Environmenthome+"/workfolder"


#Opening basecode file
with open(Environmenthome+"/"+Environmentname+"/code.yaml", "r") as f:
  file1=f.read()
flipfile=flip(file1)

#writing flipped file to parsecode.json
with open(outputpath+"/"+deploymentid+"/parsecode.json", "w") as parsecode:
    file2=parsecode.write(flipfile)

#Templating
env = Environment(loader=FileSystemLoader(outputpath+"/"+deploymentid))

template = env.get_template("parsecode.json")
output_from_parsed_template = template.render(deploymentid=deploymentid)


#Writing templated file in json
with open(outputpath+"/"+deploymentid+"/"+"/codeparsed1.json", "w") as fh:
    fh.write(output_from_parsed_template)

#Opening json rendered from template
with open(outputpath+"/"+deploymentid+"/"+"/codeparsed1.json", "r") as fjson:
    dummy=fjson.read()
yamltemp=flip(dummy)


#Writing YAML file back from rendered template json
with open(outputpath+"/"+deploymentid+"/code.yaml", "w") as fparseyaml:
    code=fparseyaml.write(yamltemp)



