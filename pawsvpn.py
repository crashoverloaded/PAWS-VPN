import boto3
import time
import os
import getpass
import regions

## Checking is the AWS Credential files are present

user = getpass.getuser()
cred_path = '/home/'+str(user)+'/.aws/credentials'
if os.path.isfile(cred_path):
    perm = input("Would you like to change your AWS secret Key and Access Key (y/n): ")
    if perm == "y" or perm =="Y":
    
        print("Please Go to "+cred_path+".\n")
        print("Here , just update your new credentials.")
        print("And run the program again.....")
        exit()
         
    else:
        print("Proceeding with same credentials.....\n")


# if not..
else:
    # Writing to the ~/.aws/credentials file

    os.system("mkdir "+cred_path[:-12])
    f = open(cred_path, "w+")
    f.write("[default]\n")
    f.write("AWSAccessKeyId = " + input("Enter your Access Key: ")+"\n")
    f.write("AWSSecretKey = " +input("Enter your Secret key: ")+"\n")
    print("Succesfully saved your credentials at "+cred_path+" !!")
    f.close()

## Selecting regions for VPN


conf_path = '/home/'+str(user)+'/.aws/config' 
def select_region():
    print("Select a region for VPN from list below.\n")

    for i in regions.region:
        print(str(i)+" ||||-------------->>>>> "+str(regions.region[i])+"\n")

    select_region.reg_num = int(input("Enter Region Number: "))           # to use reg_num outside function
    reg = regions.region[select_region.reg_num]
    print("***********************************************")
    print("You Selected "+reg+"\n")

## Writing selected region to ~/.aws/config file
    
    os.system("sed -i '2s/^/region="+regions.region_code[select_region.reg_num]+"\\n/' "+conf_path)
    os.system("sed -i '3d' "+conf_path)
    
if os.path.isfile(conf_path):                  # Checking is file is present
    select_region()

else:
    f = open(conf_path, "w+")
    f.write("[default]\n")
    f.write("region=us-east-1")
    f.close()
    select_region()

## Creating instance 
ec2 = boto3.resource('ec2',region_name=regions.region_code[select_region.reg_num])

ec2.create_instances(ImageId=regions.AMI[select_region.reg_num], MinCount=1, MaxCount=1,InstanceType='t2.micro')
print("Your Ec2 instance has been created")


# Using Instance

# Fetching the created instance ID
Instance_ID = []
for instance in ec2.instances.all():
    if instance.state['Name'] == "pending":
        Instance_ID.append(instance.id)

# Now using that instance id to fetch Instance Public IP address
instance = ec2.Instance(id=Instance_ID[0])
instance.wait_until_running()
current_instance = list(ec2.instances.filter(InstanceIds=Instance_ID))

# IP
ip_address = current_instance[0].public_ip_address


# creating AWS Key-Pair to a file
keypair_name = "AWSVPN_KEY"
new_pair  = ec2.create_key_pair(KeyName = keypair_name)

with open('./AWSVPN_KEY.pem', 'w') as file:
    file.write(new_pair.key_material)

# changing AWS File permission
os.system("chmod 400 AWSVPN_KEY.pem")

#response = ec2.describe_key_pairs()
#print(response)
## After Getting IP , making an SSH connection to instance
#os.system("ssh  )
