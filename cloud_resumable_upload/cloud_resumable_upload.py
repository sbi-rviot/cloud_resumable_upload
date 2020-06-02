from pathlib import Path
import os


def prepare_resumable_split(file, todir, chunksize=4194304): 
    """ Split a file into chunks in a directory
    This function is spliting the file into chunks based on the "chunksize" determined in the arguments.
    This function returns:
     - file_size (int): the overall file size of the file that is needed to appropriately send a resumable file in SharePoint.
     - partnum (int): the number of the chunks that have been created
     - chunked_files (list): a list of the file names that have been created

    :param file: path to the file you want to upload
    :param todir: path of the folder where you want the chunks to be temporarorily saved
    :param chunksize: size of the chunks (in bytes)
    """

    file_size = os.path.getsize(file)

    index = file.rfind(".")
    file_name = file[:index]

    index = file.rfind(".")
    extention = file[index:]

    if not os.path.exists(todir):
        os.mkdir(todir)
    else:
        for fname in os.listdir(todir):
            os.remove(os.path.join(todir, fname)) 
    partnum = 0
    chunked_files = []
    input = open(file_name + extention, 'rb')
    while 1:
        chunk = input.read(chunksize)
        if not chunk: break
        partnum  = partnum + 1
        filename = os.path.join(todir, file_name + str(partnum) + extention)
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()
        chunked_files.append(filename)

    input.close()
    return file_size, partnum, chunked_files


def upload_file_resumable(drive, item, file_size, current_bytes, filename, url_first=None, chunk_size=4194304):
    """ Uploads a resumable file
    This function is an addon to the Library O365 in the sense that it adds the possibility for the user to create a resumable upload of a file. This resumable upload of the file is mandatory when it comes to uploading large files through a web application.

    :param item: path to the item you want to upload
    :param file_size: total size of the file you want to upload
    :param current_bytes: size of the chunk that is being uploaded
    :param filename: name of the file
    :param url: url with ID of the file that is temporarily saved in SharePoint
    :param chunksize: size of the chunks (in bytes)
    """
    if item is None:
        raise ValueError('Item must be a valid path to file')
    item = Path(item) if not isinstance(item, Path) else item

    if not item.exists():
        raise ValueError('Item must exist')
    if not item.is_file():
        raise ValueError('Item must be a file')

    if url_first:
        upload_url = url_first
    else:
        url = drive.build_url(
            drive._endpoints.get('create_upload_session').format(
                id=drive.object_id, filename=filename))
        response = drive.con.post(url)
        if not response:
            return None

        data = response.json()
        upload_url = data.get(drive._cc('uploadUrl'), None)

    if upload_url is None:
        log.error('Create upload session response without '
                  'upload_url for file {}'.format(item.name))
        return None

    data = item.open(mode='rb').read()
    transfer_bytes = len(data)
    headers = {
        'Content-type': 'application/octet-stream',
        'Content-Length': str(len(data)),
        'Content-Range': 'bytes {}-{}/{}'
                         ''.format(current_bytes,
                                   current_bytes +
                                   transfer_bytes - 1,
                                   file_size)
    }
    current_bytes += transfer_bytes
    response = drive.con.naive_request(upload_url, 'PUT',
                                      data=data,
                                      headers=headers)

    if not response:
        return None

    if response.status_code != 202:
        # file is completed
        data = response.json()
        return drive._classifier(data)(parent=drive, **{
            drive._cloud_data_key: data})
    else:
        print("transfer_bytes: ", transfer_bytes)
        return current_bytes, upload_url