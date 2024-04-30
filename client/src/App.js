import React, { useState, useEffect } from 'react';
import QuitObj from './components/QuitObj'; // Adjust the path as necessary

export default function App() {
  // State for the name and rate inputs
  const [name, setName] = useState('');
  const [rate, setRate] = useState('');
  const [types, setTypes] = useState([]);
  const [typeId, setTypeId] = useState('');
  const [timeAdded, setTimeAdded] = useState('');
  const [quits, setQuits] = useState([]);
  const [totalSaved, setTotalSaved] = useState(0);
  const [selectedTypeFilter, setSelectedTypeFilter] = useState('All');

  const [highestValuedQuit, setHighestValuedQuit] = useState(null);

  const fetchHighestValuedQuit = (typeId) => {
    fetch(`http://localhost:5000/highest_valued_quit/${typeId}`)
      .then(response => response.json())
      .then(data => setHighestValuedQuit(data))
      .catch(error => console.error('Error fetching highest valued quit:', error));
  };

  useEffect(() => {
    if (types.length > 0) {
      fetchHighestValuedQuit(types[0].id);  // Automatically fetch for the first type initially
    }
  }, [types]);  // Refetch when types change

  useEffect(() => {
    fetch('http://localhost:5000/get_types')
      .then(response => response.json())
      .then(data => setTypes(data))
      .catch(error => console.error('Error fetching types:', error));
  }, []);

  // Function to handle submitting the form
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents the default form submit action

    const timestamp = timeAdded || new Date().toISOString();

    // Creating the object to send, now including type_id
    const quitEntry = {
      name: name,
      rate: parseFloat(rate), // Ensure rate is sent as a float
      time_added: timestamp,
      type_id: parseInt(typeId, 10) // Ensure type_id is sent as an integer
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
        setName('');
        setRate('');
        setTimeAdded('');
        setTypeId(''); // Resetting the type ID selection
        window.location.reload(); // Consider fetching data instead of reloading for better UX
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

  const handleSave = (id, newName, newRate) => {
    const quitToUpdate = { name: newName, rate: newRate };
    fetch(`http://localhost:5000/update_quit/${id}`, {
      method: 'PUT', // or 'PATCH'
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(quitToUpdate),
    })
      .then(response => response.json())
      .then(() => {
        const updatedQuits = quits.map(quit => {
          if (quit.id === id) {
            return { ...quit, name: newName, rate: newRate };
          }
          return quit;
        });
        setQuits(updatedQuits);
      })
      .catch(error => console.error('Error:', error));
  };
  

  return (
    <div style={{ margin: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}>
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
        <div>
          <label>
            Type:
            <select value={typeId} onChange={(e) => setTypeId(e.target.value)}>
              {types.map(type => (
                <option key={type.id} value={type.id}>{type.name}</option>
              ))}
            </select>
          </label>
        </div>
        <button type="submit">Add Quit Entry</button>
      </form>

      <div>
      <label>
        Filter by Type:
        <select value={selectedTypeFilter} onChange={(e) => setSelectedTypeFilter(e.target.value)}>
          <option value="All">All</option>
          {types.map((type) => (
            <option key={type.id} value={type.name}>{type.name}</option>
          ))}
        </select>
      </label>
    </div>

    {/* List of quits */}
    <div>
      <h1>Quits</h1>
      {quits
        .filter(quit => selectedTypeFilter === 'All' || quit.type_name === selectedTypeFilter)
        .map(quit => (
          <QuitObj key={quit.id} id={quit.id} name={quit.name} rate={quit.rate} timeAdded={quit.time_added} type={quit.type_name} onDelete={handleDelete} onSave={handleSave} />
      ))}
    </div>
    <div>
      <label>
        Highest Valued Quit for:
        <select onChange={(e) => fetchHighestValuedQuit(e.target.value)}>
          {types.map(type => (
            <option key={type.id} value={type.id}>{type.name}</option>
          ))}
        </select>
      </label>
    </div>
    {highestValuedQuit && (
      <div>
        <h3>{highestValuedQuit.name}</h3>
        <p>Rate: ${highestValuedQuit.rate}/mo</p>
        <p>Type: {highestValuedQuit.type_name}</p>
        <p>Added On: {highestValuedQuit.time_added}</p>
      </div>
    )}
  </div>

  );
}
