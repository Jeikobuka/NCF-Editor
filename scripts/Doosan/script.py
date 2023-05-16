# ------------------------------------------------

def changeToolNumFormat(content):
    for toolNum in range(100):
        content = content.replace(f"T{toolNum}M6", f"M6T{toolNum}").replace(f"T{toolNum}\nM6", f"M6T{toolNum}")
    return content

def main(content):
    content = changeToolNumFormat(content)
    return content
