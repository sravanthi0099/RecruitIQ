from app.services.resume_parser import extract_text_from_pdf

text = extract_text_from_pdf("sample_resume.pdf")

print(text[:1000])