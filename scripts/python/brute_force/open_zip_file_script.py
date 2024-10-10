import zipfile
import sys

zip_file_path = sys.argv[1]
passwords_file_path = sys.argv[2]
file = zipfile.ZipFile(zip_file_path) 

def crack_zip(zip_file, passwords_file):
    with zipfile.ZipFile(zip_file) as zf:
        with open(passwords_file, "r") as pf:
            for line in pf:
                password = line.strip()  # Get rid of any newline characters
                try:
                    file.extractall(pwd=password.encode())
                    print(password)

                except (RuntimeError, zipfile.BadZipFile):
                    continue
                print("Password not found!")
    return None


# TODO 5: Call the crack_zip function
crack_zip(zip_file_path,passwords_file_path)
