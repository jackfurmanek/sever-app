import React, { useState } from 'react';

function QuitObj({ id, name, rate, type, onDelete, onSave }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedName, setEditedName] = useState(name);
  const [editedRate, setEditedRate] = useState(rate);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    onSave(id, editedName, parseFloat(editedRate));
    setIsEditing(false);
  };

  return (
    <div style={{ margin: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}>
      {isEditing ? (
        <>
          <input type="text" value={editedName} onChange={(e) => setEditedName(e.target.value)} />
          <input type="number" step="0.01" value={editedRate} onChange={(e) => setEditedRate(e.target.value)} />
          <button onClick={handleSave}>Save</button>
        </>
      ) : (
        <>
          <h2>{name}</h2>
          <p>Rate: ${rate}/mo</p>
          <p>Type: {type}</p>
          <button onClick={handleEdit}>Edit</button>
          <button onClick={() => onDelete(id)} style={{ color: 'red', cursor: 'pointer' }}>Delete</button>
        </>
      )}
    </div>
  );
}

export default QuitObj;
