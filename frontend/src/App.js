import React from 'react'
import { BrowserRouter } from 'react-router-dom';
import './App.css';
import Application from './application'

const App = () => (
    <BrowserRouter basename='localhost'>
        <Application/>
    </BrowserRouter>
)

export default App;
