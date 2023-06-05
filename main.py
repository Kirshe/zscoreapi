from fastapi import FastAPI
from calculations import calculate_z_score

from models import FinancialData, ScoreData, Score

app = FastAPI()


@app.post("/company/{iso_code}/{id}", response_model=ScoreData)
async def z_score_calculator(iso_code: str, id: int, financial_data: FinancialData):
    scores = [
        Score(year=financial.year, zscore=calculate_z_score(financial)) 
        for financial in financial_data.financials
    ]
    return ScoreData(scores=scores)