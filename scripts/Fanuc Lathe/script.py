# ------------------------------------------------
converts = {}
GCODE_FILE = 'swapped_gcodes.txt'

def getConverts(prepend_path):
    with open(prepend_path+'/'+GCODE_FILE, 'r') as f:
        for line in f.readlines():
            converts[line.split('->')[0].strip()] = line.split('->')[1].strip()
    return converts

def convertGCodes(content, prepend_path):
    converts = getConverts(prepend_path)
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
'''
def changeToolNumFormat(content):
    for toolNum in range(100):
        content = content.replace(f"T{toolNum}M6", f"M6T{toolNum}").replace(f"T{toolNum}\nM6", f"M6T{toolNum}")
    return content
'''
def main(content, prepend_path):
    newContent = convertGCodes(content, prepend_path)
    #newContent = changeToolNumFormat(newContent)
    return newContent