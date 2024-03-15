from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ..job_description import handle_user_query
from ..config import host, port, reload
from ..ingestion.main import save_and_ingest_file, get_all_resumes, reset_parser_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # This allows all origins, you can specify specific origins instead
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


def start():
    uvicorn.run(
        f"{__name__}:app",
        host=host,
        port=port,
        reload=reload,
    )


@app.post("/")
def main():
    return {"message": "Hello World"}


@app.post("/upload_files")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        files_ingested = []

        for uploaded_file in files:
            contents = await uploaded_file.read()

            success = save_and_ingest_file(contents, uploaded_file.filename)

            if success:
                files_ingested.append(uploaded_file.filename)
            else:
                print(f"Unable to Ingest {uploaded_file.filename}")

        return JSONResponse(
            content={"message": f"Files {files_ingested} ingested successfully"},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error uploading files: {str(e)}"}, status_code=500
        )


@app.get("/get_resumes")
async def get_resume():
    return get_all_resumes()


@app.get("/reset")
async def reset():
    return reset_parser_data()


@app.post("/query_resumes")
async def query_resumes(query: str):
    handle_user_query(query)
    print("query: ", query)
