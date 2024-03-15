import React from "react";
import FileUpload from "./containers/filetest";
import UploadedResumes from "./containers/UploadedResumes";

export default function App() {
  return (
    <main className="h-screen relative border-2 border-red-500 px-64 py-32">
      <div>
        <h1 className=" font-bold text-4xl border-2">AI Resume Parser</h1>
      </div>
      <div className="py-10">
        <UploadedResumes />
      </div>
      <div>
        <FileUpload />
      </div>
    </main>
  );
}
