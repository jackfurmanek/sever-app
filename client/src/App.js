import React, { useState, useEffect } from 'react';
import QuitObj from './components/QuitObj'; // Adjust the path as necessary

export default function App() {
  // State for the name and rate inputs
  const [name, setName] = useState('');
  const [rate, setRate] = useState('');
  const [quits, setQuits] = useState([]);

  // Function to handle submitting the form
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents the default form submit action

    // Creating the object to send
    const quitEntry = {
      name: name,
      rate: parseFloat(rate), // Ensure rate is sent as a float
    };

    // Sending the POST request to the Flask backend
    fetch('http://localhost:5000/add_quit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(quitEntry),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        // Optionally reset form or give user feedback
        setName('');
        setRate('');
        window.location.reload();
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  useEffect(() => {
    fetch('http://localhost:5000/get_quits')
      .then(response => response.json())
      .then(data => setQuits(data))
      .catch(error => console.error('Error fetching quits data:', error));
  }, []);

  const handleDelete = (id) => {
    fetch(`http://localhost:5000/delete_quit/${id}`, {
      method: 'DELETE',
      // Additional headers and body as needed
    })
    .then(response => response.json())
    .then(() => {
      // After deletion, you might want to remove the item from the state
      // This will trigger a re-render and remove the item from the UI
      setQuits(quits.filter(quit => quit.id !== id));
    })
    .catch(error => console.error('Error:', error));
  };

  return (
    <div>
      <h2>Add New Quit Entry</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Name:
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </label>
        </div>
        <div>
          <label>
            Rate ($):
            <input
              type="number"
              step="0.01" // Allows decimal values
              value={rate}
              onChange={(e) => setRate(e.target.value)}
            />
          </label>
        </div>
        <button type="submit">Add Quit Entry</button>
      </form>
      <div>
        <h1>Quits</h1>
        {quits.map(quit => (
          <QuitObj key={quit.id} id={quit.id} name={quit.name} rate={quit.rate} timeAdded={quit.time_added} onDelete={handleDelete} />
        ))}
      </div>
    </div>

  );
}
