from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from scraper import process_cino_form
from logger import app_logger
import json
from services.parser import parse_case_html

GATEWAY_SECRET = "secret-123"

# Create FastAPI instance
app = FastAPI()

def verify_gateway_auth(request: Request):
    print("=== Incoming Headers ===")
    for k, v in request.headers.items():
        print(f"{k}: {v}")

    if request.headers.get("x-gateway-auth") != GATEWAY_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized gateway call")

@app.get("/")
def home():
    app_logger.info("Root Executed...")
    return {"message": "Python service running"}

# Request body model
class CinoRequest(BaseModel):
    cino: str

# Route for handling the form submission
@app.post("/submit-form")
async def submit_form(
    cino_request: CinoRequest,
    _ = Depends(verify_gateway_auth)  # Require Gateway header
):
    try:
        app_logger.info("Calling Cino Request...")
        result = process_cino_form(cino_request.cino)

        # Retry on "Invalid Captcha"
        response_data = json.loads(result.get("response", ""))
        while "errormsg" in response_data and "Invalid Captcha" in response_data["errormsg"]:
            app_logger.info("Invalid Captcha... Retrying...")
            result = process_cino_form(cino_request.cino)
            response_data = json.loads(result.get("response", ""))

        # Final valid HTML response
        response_html = result["response"]
        case_details = parse_case_html(response_html)
        app_logger.info(case_details)

        return {
            "status": "success",
            "data": case_details
        }

    except Exception as e:
        app_logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
