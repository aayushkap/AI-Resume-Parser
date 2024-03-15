import React from "react";

const FileTile = ({ item }) => {
  return (
    <main className="w-full flex justify-between items-center p-2">
      <div>{item}</div>
      <button className="hover:text-red-500">Delete</button>
    </main>
  );
};

export default FileTile;
