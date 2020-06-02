# Cloud_resumable_upload - Upload documents from the cloud to the cloud without time out error
Detailed usage documentation is still in progress
The objective of this package is to allow developpers to upload large files into cloud drives from web applications without any timeout error.
Using cloud web application, backend activities are limited to 20 to 30 seconds of run time before they are close without response.
In order to overcome this limitation, a possibility is to use resumable upload which allows you to send chunks of the file you wish to upload.

As of now, this package only helps developpers uploading resumable files for SharePoint. Our next objective is to develop this functionality for Google as well.

## Installation

This is how you can install it on your machine:

```
pip install cloud_resumable_upload
```

## Use case

You have a 20Mb file that you wish to upload to SharePoint from a web application.
You are using the library o365.

```
#Step 1: Set up

from O365 import Account #we are using this library as a base for our package
from cloud_resumable_upload import prepare_resumable_split, upload_file_resumable #those are the two functions we will need for this use case
drive = get_sp_drive(Account, 'youraccount.sharepoint.com', 'yoursharepointsite') #in this example, we will use the main folder as the location for our upload

#Step 2: split file

file_size, partnum, chunked_files = prepare_resumable_split('yourfile.ext', 'todir', chunksize=4194304) #this function splits the file of you choice in the folder of your choice and returns information regarding the execution

#Step 3: simple loop through the chunked files

chunkrank = 1
current_bytes = 0
for i in chunked_files:
    print('chunkfile: ',i)
    print('chunkrank: ',chunkrank)
    print('current_bytes: ',current_bytes)
    if chunkrank == 1:
        current_bytes, url = upload_file_resumable(drive, i, file_size, current_bytes, 'video_demo.mp4')
    elif chunkrank < len(chunked_files):
        current_bytes, url = upload_file_resumable(drive, i, file_size, current_bytes, 'video_demo.mp4', url)
    else:
    	upload_file_resumable(drive, i, file_size, current_bytes, 'video_demo.mp4', url)
    chunkrank += 1

```

This can very simply be integrated in flask back end API.

## List of the functions available [last update: 6/1/2020]:

### prepare_resumable_split(file, todir, chunksize=4194304)
Split a file into chunks in a directory  
This function is spliting the file into chunks based on the "chunksize" determined in the arguments.  
This function returns:  
     - file_size (int): the overall file size of the file that is needed to appropriately send a resumable file in SharePoint.  
     - partnum (int): the number of the chunks that have been created  
     - chunked_files (list): a list of the file names that have been created  
  
param file: path to the file you want to upload  
param todir: path of the folder where you want the chunks to be temporarorily saved  
param chunksize: size of the chunks (in bytes)  
  
### upload_file_resumable(drive, item, file_size, current_bytes, filename, url_first=None, chunk_size=4194304)
Uploads a resumable file  
This function is an addon to the Library O365 in the sense that it adds the possibility for the user to create a resumable upload of a file. This resumable upload of the file is mandatory when it comes to uploading large files through a web application.  
  
param item: path to the item you want to upload  
param file_size: total size of the file you want to upload  
param current_bytes: size of the chunk that is being uploaded  
param filename: name of the file  
param url: url with ID of the file that is temporarily saved in SharePoint  
param chunksize: size of the chunks (in bytes)  
