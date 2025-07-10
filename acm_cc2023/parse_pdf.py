from docx import Document
import sys
import json

def is_heading3(paragraph):
    return paragraph.style.name == "Heading 3"

def is_italic_paragraph_with_trigger(paragraph, trigger_text="Illustrative Learning Outcomes"):
    return (
        trigger_text.lower() in paragraph.text.lower() and
        any(run.italic for run in paragraph.runs)
    )

def is_professional_dispositions(paragraph):
    return paragraph.text.strip().lower() == "professional dispositions"

def parse_learning_outcomes(filepath):
    try:
        doc = Document(filepath)
        paragraphs = doc.paragraphs

        knowledge_units = []

        i = 0
        while i < len(paragraphs):
            para = paragraphs[i]

            if is_heading3(para):
                heading_text = para.text.strip()
                found_trigger = False
                outcome_lines = []

                i += 1
                while i < len(paragraphs):
                    next_para = paragraphs[i]

                    # Stop if next Heading 3 or Professional Dispositions is encountered
                    if is_heading3(next_para) or is_professional_dispositions(next_para):
                        break

                    if not found_trigger and is_italic_paragraph_with_trigger(next_para):
                        found_trigger = True
                        i += 1
                        continue

                    if found_trigger:
                        if next_para.text.strip():  # skip empty
                            outcome_lines.append(next_para.text.strip())

                    i += 1

                # Print if we found a valid trigger and outcomes
                if found_trigger and outcome_lines:
                    print(f"\n🔵 {heading_text}")
                    ku = {
                        "name": heading_text,
                        "outcomes": []
                    }
                    for line in outcome_lines:
                        if "CS Core" not in line and "KA Core" not in line and "Non-core" not in line:
                            print(f"   {line}")
                            ku["outcomes"].append(line)
                    
                    knowledge_units.append(ku)
            else:
                i += 1
            
        return knowledge_units

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    kus = parse_learning_outcomes("acm_guidelines.docx")
    print(len(kus))

    with open("acm_kus.json", "w", encoding="utf-8") as f:
        json.dump(kus, f, indent=2, ensure_ascii=False)


