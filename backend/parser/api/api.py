from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os

app = FastAPI()

UPLOAD_DIRECTORY = "uploads"


@app.get("/health")
async def health_check():
    return JSONResponse(content={"message": "Health Check Successful"}, status_code=200)


@app.post("/upload_files")
async def upload_files(files: list[UploadFile] = File(...)):
    files_to_handle = []
    try:
        # Create the upload directory if it doesn't exist
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)

        # Process each uploaded file
        for uploaded_file in files:
            contents = await uploaded_file.read()
            file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.filename)

            # Save the file to disk
            with open(file_path, "wb") as file_object:
                file_object.write(contents)

            print(f"Uploaded file saved as: {file_path}")

        return JSONResponse(
            content={"message": "Files uploaded successfully"}, status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error uploading files: {str(e)}"}, status_code=500
        )
