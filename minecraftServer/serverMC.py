import subprocess

def main():
    with open("status.txt", "w") as f:
        f.write("True")
    p = subprocess.Popen(["bash start.sh"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
    for line in p.stdout:
        if "<" or ">" in line:
            print(line, end='')
        elif "Server empty for 60 seconds, pausing" in line:
            break
        else:
            print(line, end='')
    p.communicate(input="/stop")
    with open("status.txt", "w") as f:
        f.write("False")




if __name__ == "__main__":
    main()