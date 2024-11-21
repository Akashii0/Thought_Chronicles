from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Cookie, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = 30

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  
    return encode_jwt


def create_access_token(data: dict) -> str:
    return create_token(
        data=data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

def create_refresh_token(data: dict) -> str:
    return create_token(
        data=data,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

def verify_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        token_type: str = payload.get("token_type")
        if id is None:
            raise credentials_exception
        return schemas.TokenData(id=str(id), token_type=token_type) 
    except JWTError:
        raise credentials_exception
    

def get_current_user(access_token: Optional[str] = Cookie(None),
                     refresh_token: Optional[str] = Cookie(None), 
                     db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail= "Could not validate credentials", 
                                          headers= {"WWW-Authenticate": "Bearer"})
    
    if not access_token and not refresh_token:
        raise credentials_exception
    
    if access_token:
        try:
            token_data = verify_token(access_token, credentials_exception)
            if token_data.token_type != "access":
                raise credentials_exception
            user = db.query(models.User).filter(models.User.id == token_data.id).first()
            if user:
                return user
        except JWTError:
            pass
        
    # If access token fails and refresh token exists, redirect to refresh endpoint
    if refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
            headers={"X-Refresh-Required": "true"}
        )

    raise credentials_exception



# On the frontend, you'll need to handle the refresh flow:
# // api/axiosConfig.js
# import axios from 'axios';

# // Create axios instance
# const api = axios.create({
#   baseURL: 'http://your-api-url',
#   withCredentials: true, // Important for cookies
# });

# // Add a response interceptor
# api.interceptors.response.use(
#   (response) => response,
#   async (error) => {
#     const originalRequest = error.config;

#     // If error is 401 and has X-Refresh-Required header and we haven't tried refreshing yet
#     if (
#       error.response?.status === 401 && 
#       error.response?.headers['x-refresh-required'] === 'true' &&
#       !originalRequest._retry
#     ) {
#       originalRequest._retry = true;

#       try {
#         // Call refresh endpoint
#         await api.post('/refresh');
        
#         // Retry the original request
#         return api(originalRequest);
#       } catch (refreshError) {
#         // If refresh fails, redirect to login
#         window.location.href = '/login';
#         return Promise.reject(refreshError);
#       }
#     }

#     return Promise.reject(error);
#   }
# );

# export default api;

# Then use it in your components:

# // Example usage
# import api from './api/axiosConfig';

# // Making API calls
# try {
#   const response = await api.get('/protected-route');
#   // Handle response
# } catch (error) {
#   // Handle error
# }