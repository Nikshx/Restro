import { useState } from 'react'

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
    </>
  ) 
}

export default App
