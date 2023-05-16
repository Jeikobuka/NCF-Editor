# ------------------------------------------------

def changeToolNumFormat(content):
    for toolNum in range(100):
        content = content.replace(f"T{toolNum}M6", f"T{toolNum}\nM6").replace(f"M6T{toolNum}", f"T{toolNum}\nM6")
    return content

def main(content):
    content = changeToolNumFormat(content)
    return content
