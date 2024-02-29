// QuitObj.js
import React from 'react';

function QuitObj({ id, name, rate, timeAdded, onDelete }) {
  // Function to handle the delete action
  const handleDelete = () => {
    // Call the onDelete function passed from the parent, using the quit's ID
    onDelete(id);
  };

  return (
    <div style={{ margin: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}>
      <h2>{name}</h2>
      <p>Rate: ${rate}</p>
      <p>Added: {timeAdded}</p>
      <p>id: {id}</p>
      {/* Adding a clickable delete text */}
      <div style={{ color: 'red', cursor: 'pointer' }} onClick={handleDelete}>
        Delete
      </div>
    </div>
  );
}

export default QuitObj;
