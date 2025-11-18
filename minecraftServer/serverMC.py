import subprocess

#Server empty for 60 seconds, pausing

def main():
    with open("status.txt", "w") as f:
        f.write("True")
    with subprocess.Popen(["bash start.sh"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            if "Server empty for 60 seconds, pausing" in line:
                print("Python stopping server")
                with open("status.txt", "w") as f:
                    f.write("False")
                p.communicate(input="/stop")
            else:
                print(line, end='')
        

if __name__ == "__main__":
    main()