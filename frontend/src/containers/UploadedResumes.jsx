import React, { useState, useEffect } from "react";
import FileTile from "./components/FileTile";

const UploadedResumes = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    // Function to fetch data from API
    const getResumes = async () => {
      try {
        const res = await fetch("http://localhost:8000/get_resumes", {
          method: "GET",
        });
        const data = await res.json();
        console.log(data);
        setItems(data);
      } catch (error) {
        console.error("Error getting files:", error);
      }
    };

    getResumes(); // Call the fetch data function when component mounts
  }, []);

  return (
    <div className="grid grid-cols-4 gap-x-16 gap-y-8">
      {items.length === 0 ? (
        <h2 className="text-2xl">No resumes uploaded.</h2>
      ) : (
        items.map((item, index) => (
          <div
            key={index}
            className="flex justify-center p-4 border-2 rounded-xl"
          >
            <FileTile item={item} />
          </div>
        ))
      )}
    </div>
  );
};

export default UploadedResumes;
