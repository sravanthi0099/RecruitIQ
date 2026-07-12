from app.database import engine
from app.models.analysis_result import AnalysisResult

AnalysisResult.__table__.create(
    bind=engine,
    checkfirst=True
)

print("analysis_results table created")