# DirectoryAnalysis
Functionalities and Benefits
----------------------------

The Directory Analysis script is a powerful tool for analyzing the contents of a directory, including its subdirectories. It can be used to:

1. Find large files: The script can scan a directory and identify all files that are larger than a specified size (default is 400 MB). This can be useful for identifying files that are taking up a lot of space on a drive and may be candidates for deletion.
2. Identify duplicate files: The script can also identify duplicate files, which can be useful for cleaning up a directory and removing unnecessary copies.
3. Generate a file hashes file: The script generates a file hashes file that contains the MD5 hash, path, size, and modified time for each file in the directory. This can be useful for tracking changes to files over time.
4. Generate a pending progress file: If the script is cancelled before it completes, it generates a pending progress file that can be used to resume the scan at a later time.
5. Generate a large files list file: The script generates a large files list file that contains the path, size, and modified time for each large file in the directory.
6. Exclude certain files and directories: The script allows the user to exclude certain files and directories from the scan, which can be useful for excluding system files or other files that should not be scanned.

Quick-Start Guide
-----------------

1. Install the required packages: The script requires the `os`, `hashlib`, `collections`, `concurrent.futures`, `time`, `signal`, and `sys` packages. These packages are included with Python 3.x and do not need to be installed separately.
2. Run the script: Run the script by executing the following command in a terminal or command prompt:
```
python directory_analysis.py
```
3. Select the directory to scan: The script will prompt the user to enter the path to the directory to scan. The user can either enter the path manually or select a folder using the system's file selection dialog.
4. Wait for the scan to complete: The script will scan the directory and identify all files that are larger than the specified size. This may take some time, depending on the size of the directory and the number of files in it.
5. View the results: After the scan is complete, the script will display the results in the terminal or command prompt. The results will include a list of large files, a list of duplicate files, and a file hashes file.
6. Save the results: The script will save the results to a file in the specified output directory. The user can view the results at any time by opening the file in a text editor.
7. Exclude certain files and directories: The user can exclude certain files and directories from the scan by adding them to the `exclude_files` and `exclude_dirs` lists in the script.
8. Cancel the scan: The user can cancel the scan at any time by pressing Ctrl+C. If the scan is cancelled, the script will generate a pending progress file that can be used to resume the scan at a later time.
9. Resume a cancelled scan: To resume a cancelled scan, the user can run the script again and specify the same output directory as before. The script will detect the pending progress file and resume the scan from where it left off.

I hope this quick-start guide is helpful! Let me know if you have any questions or issues.

Disclaimer Notice

The Directory Analysis script is provided "as is" without warranty of any kind, either expressed or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the script is with you. Should the script prove defective, you assume the cost of all necessary servicing, repair, or correction.
In no event shall the author or copyright holder be liable for any claim, damages, or other liability arising from the use of the script, including but not limited to any direct, indirect, special, incidental, or consequential damages, even if the author or copyright holder has been advised of the possibility of such damages.
The script is intended for use on systems with a compatible operating system and configuration. The author cannot be held responsible for any damage or loss of data that may occur as a result of using the script. It is recommended that you back up your data before using the script.
The script may include code that is covered by third-party licenses. The author has made every effort to comply with the terms of these licenses and to provide proper attribution. However, the author cannot be held responsible for any errors or omissions in this regard.
The script is intended for use by experienced users and system administrators. It should not be used by inexperienced users or users who are not familiar with the command line or with the concepts of file systems and directories.
The author reserves the right to modify or discontinue the script at any time. The author may also make changes to the script without prior notice.
By using the Directory Analysis script, you agree to the terms of this disclaimer notice. If you do not agree to the terms of this disclaimer notice, do not use the script.
If you have any questions or concerns about this disclaimer notice, please rise an issue in github.

Thank you for using the Directory Analysis script!

If you'd like to contribute to this project, simply fork the repository and submit a pull request. Your code will be reviewed and merged as soon as possible.

Thank you for your interest in contributing! I'd appreciate your help in making this project even better.

