
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def rename_duplicate_files(folder_path):
    """
    Rename duplicate files in a folder by appending a number at the end.
    """
    files = {}
    for dirpath, _, filenames in os.walk(folder_path):
      try:
        for filename in filenames:
            if filename in files:
                files[filename] += 1
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_{files[filename]}{ext}"
                os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
            else:
                files[filename] = 0
      except Exception as e:
         print(e)


def upload_folder_to_drive(folder_path):
    """
    Upload a folder and its contents to Google Drive.
    """
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    folder_name = os.path.basename(folder_path)
    folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Check if file exists in Google Drive
            file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder['id'])}).GetList()
            for file in file_list:
                if file['title'] == filename:
                    # If file with same name exists, rename it
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_0{ext}"
                    break
            # Upload the file to Google Drive
            gdrive_file = drive.CreateFile({'title': filename, 'parents': [{'id': folder['id']}]})
            gdrive_file.SetContentFile(file_path)
            gdrive_file.Upload()

if __name__ == "__main__":
    #folder_path = "/path/to/your/folder"
    folder_rem ='C:\\Users\\Jeferson\\TeraBox'
   # rename_duplicate_files(folder_rem)
    upload_folder_to_drive(folder_rem)
