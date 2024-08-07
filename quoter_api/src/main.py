import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from models.quotation_models import QuotationInput
from chains.pdf_chain import get_parsing_chain
from utils.async_utils import async_retry

from utils.create_store import create_or_update_vector_store, load_vector_store

# Create a FastAPI app with a title and description
app = FastAPI(
    title="Quoter",
    description="Endpoints for the quoter system",
    version='1.0.0',
    openapi_url='/api/v1/openapi.json',
    docs_url='/api/v1/docs',
    redoc_url='/api/v1/redoc'
)

# Load the Excel file path from the environment variables
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH")
create_or_update_vector_store(Path(EXCEL_FILE_PATH)) # type: ignore
# Load the vector store
vector_store = load_vector_store()
# Get the parsing chain using the loaded vector store
parsing_chain = get_parsing_chain(vector_store)

@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query: str):
    """Retry the agent if a tool fails to run.
    
    This can help when there are intermittent connection issues
    to external APIs.
    """
    pdf_path = await parsing_chain.ainvoke({"text": query})
    return pdf_path

@app.get("/")
async def get_status():
    """Endpoint to check the status of the API"""
    return {"status": "running"}

@app.post("/download-pdf")
async def download_pdf(text: QuotationInput) -> FileResponse:
    """Endpoint to generate and download a PDF based on the input text"""
    try:
        # Invoke the agent with retries to handle intermittent failures
        pdf_path = await invoke_agent_with_retry(text.text)
        
        if not os.path.exists(pdf_path):
            # Raise an HTTP exception if the PDF generation failed
            raise HTTPException(status_code=500, detail="Error generating PDF")
        
        # Return the generated PDF as a file response
        return FileResponse(
            path=pdf_path,
            media_type='application/pdf',
            filename=os.path.basename(pdf_path)
        )
    except Exception as e:
        # Raise an HTTP exception if any error occurs
        raise HTTPException(status_code=500, detail=str(e))
