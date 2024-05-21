import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import './App.css';

function App() {
    const [formType, setFormType] = useState('login');

    return (
        <div className="container">
            <div className="button-container">
                <button 
                    onClick={() => setFormType('login')}
                    className={formType === 'login' ? 'active' : ''}
                >
                    Login
                </button>
                <button 
                    onClick={() => setFormType('register')}
                    className={formType === 'register' ? 'active' : ''}
                >
                    Register
                </button>
            </div>
            <div className="form-container">
                {formType === 'login' ? (
                    <>
                        <h1>Login</h1>
                        <LoginForm />
                    </>
                ) : (
                    <>
                        <h1>Register</h1>
                        <RegisterForm />
                    </>
                )}
            </div>
        </div>
    );
}

export default App;
