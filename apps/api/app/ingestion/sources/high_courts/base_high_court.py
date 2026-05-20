from app.ingestion.sources.india_code import IndiaCodeConnector


class BaseHighCourtConnector(IndiaCodeConnector):
    source_name = "high_court_base"
