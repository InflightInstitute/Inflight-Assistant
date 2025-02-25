import re

def clean_manual_text(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        # Skip lines that look like page numbers (e.g., "16 / 845")
        if re.match(r'^\s*\d+\s*/\s*\d+\s*$', line):
            continue
        # Skip lines that appear to be headers or footers (adjust regex if needed)
        if "Table of Contents" in line or "©" in line:
            continue
        # Skip lines that are just punctuation or repeated characters
        if re.match(r'^\s*[-*]+\s*$', line):
            continue
        cleaned_lines.append(line.strip())

    cleaned_text = "\n".join(cleaned_lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Cleaned text saved to {output_path}")

if __name__ == "__main__":
    input_path = "manual.txt"         # Make sure your manual file is named manual.txt and is in the repository root
    output_path = "manual_cleaned.txt"
    clean_manual_text(input_path, output_path)
