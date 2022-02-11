#! python3
import os
import sys

def main(envvar, filename):
    secret_var = os.environ[envvar]
    try:
        with open(filename, "x") as write_file:
            write_file.write(secret_var)
    except FileExistsError as e:
        print("Error file already exists")
        exit(1)

if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except KeyError as e:
        print("Error no environment var or no file path provided")
        exit(1)