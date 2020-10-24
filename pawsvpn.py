import boto3
import os
import getpass
import regions

# Checking is the AWS Credential files are present

user = getpass.getuser()
path = '/home/'+str(user)+'/.aws/credentials'
if os.path.isfile(path):
    perm = input("Would you like to change your AWS secret Key and Access Key (y/n): ")
    if perm == "y" or perm =="Y":
    
        print("Please Go to "+path+".\n")
        print("Here , just update your new credentials.")
         
    else:
        print("Proceeding with same credentials.....\n")


# if not..
else:
    # Writing to the ~/.aws/credentials file

    os.system("mkdir "+path[:-12])
    f = open(path, "w+")
    f.write("[default]\n")
    f.write("AWSAccessKeyId = " + input("Enter your Access Key: ")+"\n")
    f.write("AWSSecretKey = " +input("Enter your Secret key: ")+"\n")
    print("Succesfully saved your credentials at "+path+" !!")
    f.close()

# Selecting regions for VPN

print("Select a region for VPN from list below.\n")

for i in regions.region:
    print(str(i)+" ||||-------------->>>>> "+str(regions.region[i])+"\n")

reg_num = int(input("Enter Region Number: "))
reg = regions.region[reg_num]
print("***************************************")
print("You Selected "+reg+"\n")

# Writing selected region to ~/.aws/config file

print(repr("sed '2s/^/region="+str(regions.region_code[reg_num])+"\n/' ~/.aws/config"))

'''
ec2 = boto3.client('ec2')
response = ec2.describe_regions()
print('Regions:', response['Regions'])
print("""""""""""""""""""""""""""""""""""""""""""""""")
response = ec2.describe_availability_zones()
print('Availability Zones:', response['AvailabilityZones'])
'''
