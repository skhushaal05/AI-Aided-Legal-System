import re
import fitz
import json


PDF_PATH = "a1988-59.pdf"

doc = fitz.open(PDF_PATH)

text = ""

for page in doc:
    text += page.get_text()

# normalize spaces
text = re.sub(r'\s+', ' ', text)

# find sections
pattern = r'(\d+[A-Z]?)\.\s+([A-Za-z ,\-\(\)]+?)\.—'

matches = list(re.finditer(pattern, text))

sections = []

for i, match in enumerate(matches):

    section_no = match.group(1)
    heading = match.group(2).strip()

    start = match.end()

    if i + 1 < len(matches):
        end = matches[i + 1].start()
    else:
        end = len(text)

    body = text[start:end].strip()

    sections.append({
        "section": section_no,
        "heading": heading,
        "text": body
    })

with open("sections.json", "w", encoding="utf8") as f:
    json.dump(sections, f, indent=2)

print("Sections extracted:", len(sections))

# definitions.py

import json
import re

with open("sections.json", encoding="utf8") as f:
    sections = json.load(f)

definitions = []

for sec in sections:

    if sec["section"] == "2":

        text = sec["text"]

        pattern = r'\((\d+)\)\s*["“](.*?)["”]\s*means\s*(.*?)(?=\(\d+\)|$)'

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        for num, term, definition in matches:

            definitions.append({
                "term": term.strip(),
                "definition": definition.strip()
            })

with open("definitions.json", "w") as f:
    json.dump(definitions, f, indent=2)

print(len(definitions))

# chunk.py

import re
import json

with open("sections.json", encoding="utf8") as f:
    sections = json.load(f)

chunks = []

for section in sections:

    section_no = section["section"]
    heading = section["heading"]

    text = section["text"]

    subs = re.split(
        r'(\(\d+\))',
        text
    )

    if len(subs) < 3:

        chunks.append({
            "section": section_no,
            "heading": heading,
            "chunk": text
        })

        continue

    current_sub = None

    for part in subs:

        if re.match(r'\(\d+\)', part):

            current_sub = part

        else:

            if current_sub:

                chunks.append({
                    "section": section_no,
                    "heading": heading,
                    "subsection": current_sub,
                    "chunk": part.strip()
                })

with open("chunks.json", "w") as f:
    json.dump(chunks, f, indent=2)

print("chunks:", len(chunks))