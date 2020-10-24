import boto3
import os
import getpass
import regions

# Checking is the AWS Credential files are present

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

# Selecting regions for VPN


conf_path = '/home/'+str(user)+'/.aws/config' 
def select_region():
    print("Select a region for VPN from list below.\n")

    for i in regions.region:
        print(str(i)+" ||||-------------->>>>> "+str(regions.region[i])+"\n")

    select_region.reg_num = int(input("Enter Region Number: "))           # to use reg_num outside function
    reg = regions.region[select_region.reg_num]
    print("***********************************************")
    print("You Selected "+reg+"\n")

# Writing selected region to ~/.aws/config file
    
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

# Creating instance 
ec2 = boto3.resource('ec2',region_name=regions.region_code[select_region.reg_num])

ec2.create_instances(ImageId=regions.AMI[select_region.reg_num], MinCount=1, MaxCount=1,InstanceType='t2.micro')
print("Your Ec2 instance has been created")
