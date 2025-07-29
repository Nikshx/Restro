// src/components/BookTable/BookTable.js

import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './BookTable.css';

const BookTable = () => {
    const [tables, setTables] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [bookingCounts, setBookingCounts] = useState({});

    const { user, authTokens } = useContext(AuthContext); 
    const navigate = useNavigate();

    const fetchTablesData = async () => {
        try {
            const response = await fetch('/api/tables/', {
                headers: { 'Authorization': `Bearer ${authTokens.access}` }
            });
            if (!response.ok) throw new Error('Failed to fetch tables.');
            const data = await response.json();
            setTables(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (authTokens) {
            fetchTablesData();
        } else {
            navigate('/auth');
        }
    }, [authTokens, navigate]);

    const handleCountChange = (tableId, value, maxSeats) => {
        const count = Math.max(1, Math.min(parseInt(value) || 1, maxSeats));
        setBookingCounts(prev => ({ ...prev, [tableId]: count }));
    };

    const handleBookTable = async (tableId) => {
        const numPeople = bookingCounts[tableId] || 1;

        try {
            const response = await fetch('http://127.0.0.1:8000/api/bookings/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authTokens.access}`
                },
                body: JSON.stringify({ 
                    user: user.user_id, 
                    table: tableId, 
                    number_of_people: numPeople 
                }) 
            });

            const responseData = await response.json();

            if (response.ok) {
                alert('Table booked successfully!');
                fetchTablesData(); // Re-fetch data to update UI
            } else {
                // Display the specific validation error from the backend
                const errorMessage = Object.values(responseData).join('\n');
                alert(`Failed to book table: ${errorMessage}`);
            }
        } catch (error) {
            console.error('Booking error:', error);
            alert('An error occurred during booking.');
        }
    };

    if (isLoading) return <p style={{ color: 'white', textAlign: 'center', minHeight: '100vh' }}>Loading tables...</p>;
    if (error) return <p style={{ color: 'red', textAlign: 'center', minHeight: '100vh' }}>{error}</p>;

    return (
        <div className="app__book-table section__padding">
            <h1 className="headtext__cormorant">Book Your Table</h1>
            <div className="app__book-table_tables-container">
                {tables.map(table => (
                    <div 
                        key={table.id} 
                        className={`app__book-table_table-card ${table.seats_remaining === 0 ? 'app__book-table_table-card--booked' : ''}`}
                    >
                        <h2 className="p__cormorant">Table {table.table_number}</h2>
                        <p className="p__opensans">
                            {table.seats_remaining > 0 
                                ? `${table.seats_remaining} of ${table.capacity} seats remaining`
                                : `Table Full`
                            }
                        </p>

                        {table.seats_remaining > 0 && (
                            <div className="book-controls">
                                <input 
                                    type="number"
                                    min="1"
                                    max={table.seats_remaining}
                                    value={bookingCounts[table.id] || 1}
                                    onChange={(e) => handleCountChange(table.id, e.target.value, table.seats_remaining)}
                                    className="seats-input"
                                />
                                <label className="p__opensans">Seats</label>
                            </div>
                        )}

                        <button 
                            type="button" 
                            className="custom__button" 
                            onClick={() => handleBookTable(table.id)}
                            disabled={table.seats_remaining === 0}
                        >
                            {table.seats_remaining === 0 ? 'Full' : 'Book Now'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BookTable;