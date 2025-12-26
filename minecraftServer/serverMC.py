import subprocess
import json

def main():
    with open("status.json", "w") as f:
        f.write(json.dumps(True))
    p = subprocess.Popen(["bash start.sh"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
    for line in p.stdout:
        if ("<" in line) or (">" in line):
            print(line, end='')
        elif "Server empty for 120 seconds, pausing" in line:
            break
        else:
            print(line, end='')
    p.communicate(input="/stop")
    with open("status.json", "w") as f:
        f.write(json.dumps(False))




if __name__ == "__main__":
    main()