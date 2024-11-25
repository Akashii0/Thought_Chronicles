//Create an axios instance with interceptors:

import axios from 'axios';

const baseURL = 'http://localhost:8000'; // adjust to your FastAPI URL

const api = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle 401 errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;





//Create a signup form component:


import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';

const SignupForm = () => {
    const [author, setAuthor] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        const formData = new FormData();
        formData.append('author', author);
        formData.append('password', password);

        try {
            const response = await api.post('/users', formData);
            const { access_token, user } = response.data;
            login(access_token, user);
            navigate('/dashboard'); // or wherever you want to redirect after signup
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="author">Username:</label>
                <input
                    type="text"
                    id="author"
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="password">Password:</label>
                <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </div>
            {error && <div className="error">{error}</div>}
            <button type="submit">Sign Up</button>
        </form>
    );
};

export default SignupForm;









//Update your main App component to use the AuthProvider:
import { BrowserRouter as Router } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import AppRoutes from './routes'; // You'll need to create this

function App() {
    return (
        <Router>
            <AuthProvider>
                <AppRoutes />
            </AuthProvider>
        </Router>
    );
}

export default App;





//Create a protected route wrapper:
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children }) => {
    const { auth } = useAuth();

    if (!auth?.token) {
        return <Navigate to="/login" />;
    }

    return children;
};

export default ProtectedRoute;








//Example of how to use the API with authentication:
import { useEffect, useState } from 'react';
import api from '../api/axios';

const SomeProtectedComponent = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // The token will be automatically added to the request header
                const response = await api.get('/protected-endpoint');
                setData(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            {/* Render your protected data */}
        </div>
    );
};

export default SomeProtectedComponent;




// to use this setup:
// Wrap your app with the AuthProvider
// Use the useAuth hook to access authentication state and methods
// Use the api instance for making authenticated requests
// Protect routes using the ProtectedRoute component



// You'll also need to install these dependencies:
// Bash
// This setup provides:
// Global authentication state management
// Automatic token handling in requests
// Protected routes
// Automatic handling of 401 errors
// Persistent authentication across page refreshes



// Remember to:
// Handle CORS in your FastAPI backend
// Secure your routes appropriately
// Use HTTPS in production
// Store sensitive information in environment variables
// Implement proper token refresh mechanisms for production use
// Would you like me to explain any part in more detail or show how to implement additional features like token refresh?