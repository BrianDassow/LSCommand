import os, glob, stat, sys, datetime

recursive = False
myPath = os.getcwd()
linkCount = 0
regCount = 0
directoryCount = 0
otherCount = 0

def mode_type(mode):
    global linkCount
    global regCount
    global directoryCount
    global otherCount

    if stat.S_ISLNK(mode):
        linkCount += 1
    elif stat.S_ISREG(mode):
        regCount += 1
    elif stat.S_ISDIR(mode):
        directoryCount += 1
    else:
        otherCount += 1

if len(sys.argv) > 1:
    if sys.argv[1] == "-R":
        recursive = True
    else:
        myPath = sys.argv[1]
        if len(sys.argv) > 2:
            if sys.argv[2] == "-R":
                print("recursive")
                recursive = True
            else:
                print("Malformed command.")

print("Name\t\t\t", "Owner\t\t", "Size\t\t", "Created\t\t", "Modified")

if stat.S_ISDIR(os.stat(myPath).st_mode):
    length = 0
    if recursive:
        myPath += "\\**\\*"
        length = 4
    else:
        myPath += "\\*"
        length = 1

    for filename in glob.iglob(myPath, recursive=recursive):
        stats = os.stat(filename)
        mode_type(stats.st_mode)
        print(filename[(len(myPath) - length):] + "\t", str(stats.st_uid) + "\t\t", str(stats.st_size) + "kb\t\t", str(datetime.datetime.fromtimestamp(stats.st_ctime)) + "\t\t", str(datetime.datetime.fromtimestamp(stats.st_mtime)) + "\t\t")
else:
    stats = os.stat(myPath)
    mode_type(stats.st_mode)
    print(myPath + "\t", str(stats.st_uid) + "\t\t", str(stats.st_size) + "kb\t\t", str(datetime.datetime.fromtimestamp(stats.st_ctime)) + "\t\t", str(datetime.datetime.fromtimestamp(stats.st_mtime)) + "\t\t")

print("\nTotal files: ", regCount)
print("Total directories: ", directoryCount)
print("Total links: ", linkCount)
print("Total other: ", otherCount)
print("Total entries: ", regCount + directoryCount + linkCount + otherCount)
