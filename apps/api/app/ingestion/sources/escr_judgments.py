from app.ingestion.sources.india_code import IndiaCodeConnector


class ESCRJudgmentsConnector(IndiaCodeConnector):
    source_name = "escr_judgments"
