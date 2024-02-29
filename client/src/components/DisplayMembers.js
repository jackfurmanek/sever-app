import React from 'react' // thing

export default function DisplayMembers({ members }) {
    return (
        <div>
            <h2>Members List</h2>
            <ul>
                {members.map((member, index) => (
                    <li key={index}>{member}</li>
                ))}
            </ul>
        </div>
    );
}
