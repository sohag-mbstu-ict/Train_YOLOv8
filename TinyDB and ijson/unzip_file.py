
# importing the zipfile module 
from zipfile import ZipFile 

# loading the temp.zip and creating a zip object 
with ZipFile("/home/azureuser/data/datadisk/original/images/train/train2017.zip", 'r') as zObject: 

	# Extracting all the members of the zip 
	# into a specific location. 
	zObject.extractall( 
		path="/home/azureuser/data/datadisk/original/images/train/") 

