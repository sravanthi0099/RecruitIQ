from app.database import SessionLocal
from app.models.analysis_result import AnalysisResult

db = SessionLocal()

rows = db.query(AnalysisResult).all()

print(f"Total Records: {len(rows)}")

for row in rows:
    print("-" * 50)
    print("ID:", row.id)
    print("Candidate:", row.candidate_id)
    print("Job:", row.job_id)
    print("Decision:", row.final_decision)