import fitz

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            if page_num > 67 and page_num < 69:
                page = doc[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

if __name__ == "__main__":

    pdf_path = 'acm_guidelines.pdf'
    text = extract_text_from_pdf(pdf_path)

    if text:
        print(text)
