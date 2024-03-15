import React, { useState } from "react";

export default function FileUpload() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [response, setResponse] = useState("");
  const [dragging, setDragging] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFiles(e.target.files);
  };

  const handleUpload = async () => {
    try {
      const formData = new FormData();
      for (let i = 0; i < selectedFiles.length; i++) {
        formData.append("files", selectedFiles[i]);
      }

      const res = await fetch("http://localhost:8000/upload_files", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log(data);
      setResponse(data.message);
    } catch (error) {
      console.error("Error uploading files:", error);
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    setSelectedFiles([...selectedFiles, ...droppedFiles]);
  };

  return (
    <div
      onDragEnter={handleDragEnter}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {response && <p>Response from backend: {response}</p>}
      {selectedFiles.length > 0 && (
        <div>
          <h4>Selected Files:</h4>
          <ul>
            {selectedFiles.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}
      <div
        style={{
          border: `2px dashed ${dragging ? "blue" : "black"}`,
          padding: "20px",
          textAlign: "center",
          cursor: "pointer",
        }}
      >
        <h3>Drag & Drop Files Here</h3>
      </div>
    </div>
  );
}
