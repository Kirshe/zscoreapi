import sqlalchemy
import databases
from settings import settings


metadata = sqlalchemy.MetaData()

companies_table = sqlalchemy.Table(
    "companies",
    metadata,
    sqlalchemy.Column(
        "id", sqlalchemy.Integer, 
        sqlalchemy.Sequence("seq_company_id", start=1, increment=1), 
        primary_key=True
    ),
    sqlalchemy.Column("company_code", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("country_iso_code", sqlalchemy.String(length=2), nullable=False),
    sqlalchemy.UniqueConstraint("company_code", "country_iso_code")
)

scores_table = sqlalchemy.Table(
    "scores",
    metadata,
    sqlalchemy.Column(
        "id", sqlalchemy.Integer, 
        sqlalchemy.Sequence("seq_score_id", start=1, increment=1), 
        primary_key=True
    ),
    sqlalchemy.Column("company_id", sqlalchemy.ForeignKey("companies.id"), nullable=False),
    sqlalchemy.Column("year", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("zscore", sqlalchemy.Float)
)

engine = sqlalchemy.create_engine(settings.database_url)
metadata.create_all(engine)

database = databases.Database(settings.database_url)