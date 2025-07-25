import { useState } from 'react'
import Register  from './register/Register';
import { CanteenHeader, CanteenMenu } from './container';
import { Navbar } from './components';
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <Navbar/>
    <CanteenHeader/>
    <CanteenMenu/>
    <Register/>
    </>
  ) 
}

export default App
