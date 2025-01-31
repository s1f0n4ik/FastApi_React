import React, { useState } from 'react';
import { fetchDashboardData } from '../services/api';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [token, setToken] = useState('');

    const loadDashboard = async () => {
        try {
            const result = await fetchDashboardData(token);
            setData(result);
        } catch (err) {
            alert('Failed to load dashboard data!');
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Dashboard</h2>
            <input
                type="text"
                placeholder="Enter token"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                style={{ marginBottom: '10px' }}
            />
            <button onClick={loadDashboard}>Load Data</button>
            {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
        </div>
    );
};

export default Dashboard;