import os

from services.pdf_service import extract_text
from rag.chunker import chunk_text
from rag.vector_store import store_chunks

UPLOAD_FOLDER = "uploads"

# Get all PDF files
pdf_files = [file for file in os.listdir(UPLOAD_FOLDER) if file.lower().endswith(".pdf")]

if len(pdf_files) < 2:
    print("❌ Please upload both Resume and Job Description PDFs.")
    exit()

print("PDF Files Found:")
for file in pdf_files:
    print("-", file)

# Assume first PDF = Resume, second PDF = Job Description
resume_path = os.path.join(UPLOAD_FOLDER, pdf_files[0])
jd_path = os.path.join(UPLOAD_FOLDER, pdf_files[1])

print("\nReading Resume...")
resume_text = extract_text(resume_path)
print(f"Resume Characters: {len(resume_text)}")

print("Reading Job Description...")
jd_text = extract_text(jd_path)

print("Creating Chunks...")
resume_chunks = chunk_text(resume_text)
jd_chunks = chunk_text(jd_text)
print(f"JD Characters: {len(jd_text)}")

print(f"Resume Chunks: {len(resume_chunks)}")
print(f"Job Description Chunks: {len(jd_chunks)}")

print("Storing Resume...")
store_chunks(resume_chunks, "resume")

print("Storing Job Description...")
store_chunks(jd_chunks, "job_description")

print("\n✅ ChromaDB Index Created Successfully!")