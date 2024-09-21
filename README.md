# **Folder Synchronization**

This Python program aims to synchronize two folders – source and copy – ensuring both have the same content. For that, it performs 3 main operations:
-	**Copy file**: If a file is modified or created, it is copied from the source to the copy folder.
-	**Create folder**: When a folder is created in the source folder, a new folder is created in the copy folder as well.
-	**Remove item**: The same happens in the copy folder when a file or a folder is deleted from the source folder.
To check the content of files, the program makes use of the MD5 hashing algorithm, from the library `hashlib`.

## User Usage
To run the program, it is recommended to have *Python 3.12.6* installed. The following arguments must be provided:
- **source_path**: Absolute path of the source folder
- **copy_path**: Absolute path of the copy folder
- **log_path**: Absolute path of the log file
- **sync_time**: Verification cycle time in seconds

If any of the specified folders do not exist, the program notifies the user and exits. During the verification process, log messages are displayed in the console, describing each operation performed. These messages are also saved in the log file.

After **5 minutes** of inactivity, the program exits.
