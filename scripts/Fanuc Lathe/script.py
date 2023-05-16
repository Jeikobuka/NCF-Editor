import os
# ------------------------------------------------
converts = {}
GCODE_FILE = 'swapped_gcodes.txt'

def getConverts(prepend_path):
    with open(prepend_path+'\\'+GCODE_FILE, 'r') as f:
        for line in f.readlines():
            converts[line.split('->')[0].strip()] = line.split('->')[1].strip()
    return converts

def convertGCodes(content, scriptPath):
    converts = getConverts(scriptPath)
    newConvContent = []
    for line in content.split('\n'):
        for convert in converts:
            if convert in line:
                line = line.replace(convert, converts[convert].split('...')[0])
                if "..." in converts[convert]:
                    line += '\n'+converts[convert].split('...')[1]
                break
        newConvContent.append(line)
    return '\n'.join(newConvContent)

def main(content):
    newContent = convertGCodes(content, os.path.dirname(__file__))
    #newContent = changeToolNumFormat(newContent)
    return newContent
