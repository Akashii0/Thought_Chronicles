import { useState, useEffect } from 'react';
import api from './api/axiosConfig';
import './style/AuthForm.css';

const AuthForm = () => {
  const [isLoginForm, setIsLoginForm] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [formStyle, setFormStyle] = useState({
    marginLeft: '0%'
  });
  
  const [titleStyle, setTitleStyle] = useState({
    marginLeft: '0%'
  });

  useEffect(() => {
    if (!isLoginForm) {
      setFormStyle({ marginLeft: '-0%' });
      setTitleStyle({ marginLeft: '-0%' });
    } else {
      setFormStyle({ marginLeft: '0%' });
      setTitleStyle({ marginLeft: '0%' });
    }
  }, [isLoginForm]);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    const endpoint = isLoginForm ? '/login' : '/users';
    
    api.post(endpoint, 
      new URLSearchParams({
        author: formData.username,
        password: formData.password,
      }), 
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )
    .then(response => {
      if (response.data) {
        window.location.href = '/dashboard';
      }
    })
    .catch(error => {
      setError(error.response?.data?.detail || 'An error occurred');
      console.error('Auth error:', error);
    })
    .finally(() => {
      setLoading(false);
    });
  };

  return (
    <div className="wrapper">
      <div className="title-text" style={titleStyle}>
        <div className="title login">Akashi ToDo</div>
        <div className="title signup">Signup Form</div>
      </div>
      <div className="form-container">
        <div className="slide-controls">
          <input 
            type="radio" 
            name="slide" 
            id="login" 
            checked={isLoginForm}
            onChange={() => setIsLoginForm(true)}
          />
          <input 
            type="radio" 
            name="slide" 
            id="signup" 
            checked={!isLoginForm}
            onChange={() => setIsLoginForm(false)}
          />
          <label 
            htmlFor="login" 
            className={`slide login ${isLoginForm ? 'active' : ''}`}
            onClick={() => setIsLoginForm(true)}
          >
            Login
          </label>
          <label 
            htmlFor="signup" 
            className={`slide signup ${!isLoginForm ? 'active' : ''}`}
            onClick={() => setIsLoginForm(false)}
          >
            Signup
          </label>
          <div className="slider-tab"></div>
        </div>
        
        <div className="form-inner">
          <form 
            onSubmit={handleSubmit} 
            className={isLoginForm ? 'login' : 'signup'}
            style={formStyle}
          >
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}
            
            <div className="field">
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleInputChange}
                required
                disabled={loading}
              />
            </div>
            <div className="field">
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
                required
                disabled={loading}
              />
            </div>
            
            {isLoginForm && (
              <div className="pass-link">
                <a href="#" onClick={(e) => e.preventDefault()}>
                  Forgot password?
                </a>
              </div>
            )}
            
            <div className="field btn">
              <div className="btn-layer"></div>
              <input 
                type="submit" 
                value={loading ? 'Please wait...' : (isLoginForm ? 'Login' : 'Signup')}
                disabled={loading}
              />
            </div>
            
            {isLoginForm && (
              <div className="signup-link">
                Not a member?{' '}
                <a 
                  href="#" 
                  onClick={(e) => {
                    e.preventDefault();
                    setIsLoginForm(false);
                  }}
                >
                  Signup now
                </a>
              </div>
            )}
          </form>

          <form 
            onSubmit={handleSubmit} 
            className="signup"
            style={{ ...formStyle, display: isLoginForm ? 'none' : 'block' }}
          >
            <div className="field">
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleInputChange}
                required
                disabled={loading}
              />
            </div>
            <div className="field">
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
                required
                disabled={loading}
              />
            </div>
            <div className="field btn">
              <div className="btn-layer"></div>
              <input 
                type="submit" 
                value={loading ? 'Please wait...' : 'Signup'}
                disabled={loading}
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;