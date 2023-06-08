from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from calculations import calculate_z_score
from models import FinancialData, ScoreData, Score
from dbschema import database, scores_table, companies_table
import sqlite3

load_dotenv()
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/company/{country_iso_code}/{company_code}", response_model=ScoreData)
async def z_score_calculator(country_iso_code: str, company_code: int, financial_data: FinancialData):
    scores = [
        Score(year=financial.year, zscore=calculate_z_score(financial)) 
        for financial in financial_data.financials
    ]
    query = companies_table.select().where(
        companies_table.c.country_iso_code == country_iso_code,
        companies_table.c.company_code == company_code,
    )
    company_id = await database.fetch_val(query, column="id")
    if not company_id:
        query = companies_table.insert().values(company_code=company_code, country_iso_code=country_iso_code)
        company_id = await database.execute(query)
    query = scores_table.insert().values([
        dict(zscore=score.zscore, year=score.year, company_id=company_id)
        for score in scores
    ])
    await database.execute(query)
    return ScoreData(scores=scores)


@app.get("/company/{iso_code}/{id}/{year}", response_model=Score)
async def stored_z_score(country_iso_code: str, company_code: int, year: int):
    query = companies_table.select().where(
        companies_table.c.company_code == company_code, 
        companies_table.c.country_iso_code == country_iso_code
    )
    company_id = await database.fetch_val(query, column="id")
    if not company_id:
        raise HTTPException(status_code=404, detail="Company not found")
    query = scores_table.select().where(
        scores_table.c.company_id == company_id,
        scores_table.c.year == year
    )
    record = await database.fetch_one(query)
    if not record:
        raise HTTPException(status_code=404, detail="Score not found")
    score = Score(**record)
    return score