from app.ingestion.sources.india_code import IndiaCodeConnector


class ECourtsConnector(IndiaCodeConnector):
    source_name = "ecourts"
