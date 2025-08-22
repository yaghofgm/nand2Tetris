def parse_lines(raw_lines:list[str])->list[str]:
    cleaned_lines=[]
    for line in raw_lines:
        cleaned = clean_line(line)
        if cleaned:
            cleaned_lines.append(cleaned)
    return cleaned_lines

def clean_line(line: str) -> str:
    # Remove comments
    if '//' in line:
        line = line[:line.index('//')]
    
    # Remove surrounding whitespace
    return line.strip()