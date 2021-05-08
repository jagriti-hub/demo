import os,sys,time,json
templatepath=sys.argv[1]
filepath=templatepath+"/eksctl.yaml"
inputpath=templatepath+"/input.json"
ekspath=templatepath+"/eksconfig.yaml"

with open(filepath, "r+") as f:
    eksyaml = f.read()

with open(inputpath, "r+") as f:
    input_options = json.loads(f.read())

PrivateSubnetId1=os.getenv("PrivateSubnet1ID")
PrivateSubnetId2=os.getenv("PrivateSubnet2ID")
PublicSubnetId1=os.getenv("PublicSubnet1ID")
PublicSubnetId2=os.getenv("PublicSubnet2ID")
Region=os.getenv("VPCRegion")
PrivateAvailabilityZone1=os.getenv("PrivateAvailabilityZone1")
PrivateAvailabilityZone2=os.getenv("PrivateAvailabilityZone2")
PublicAvailabilityZone1=os.getenv("PublicAvailabilityZone1")
PublicAvailabilityZone2=os.getenv("PublicAvailabilityZone2")

eksyaml=eksyaml.replace("PVTSUBNETID1",PrivateSubnetId1)
eksyaml=eksyaml.replace("PVTSUBNETID2",PrivateSubnetId2)
eksyaml=eksyaml.replace("PUBSUBNETID1",PublicSubnetId1)
eksyaml=eksyaml.replace("PUBSUBNETID2",PublicSubnetId2)
eksyaml=eksyaml.replace("PVTAZ1",PrivateAvailabilityZone1)
eksyaml=eksyaml.replace("PVTAZ2",PrivateAvailabilityZone2)
eksyaml=eksyaml.replace("PUBAZ1",PublicAvailabilityZone1)
eksyaml=eksyaml.replace("PUBAZ2",PublicAvailabilityZone2)
eksyaml=eksyaml.replace("AWSREGION",Region)
eksyaml=eksyaml.replace("CLUSTERNAME",input_options["Clustername"])
eksyaml=eksyaml.replace("DESIREDCAPACITY",input_options["DesiredCapacity"])
eksyaml=eksyaml.replace("INSTANCETYPE",input_options["InstanceType"])
eksyaml=eksyaml.replace("MAXSIZE",input_options["MaxSize"])
eksyaml=eksyaml.replace("MINSIZE",input_options["MinSize"])
eksyaml=eksyaml.replace("NGNAME",input_options["NodeGrpName"])
eksyaml=eksyaml.replace("VOLUME",input_options["Volume"])
eksyaml=eksyaml.replace("KEYPAIRNAME",input_options["KeyName"])

data_folder=open(ekspath,"w+")
data_folder.write(eksyaml)