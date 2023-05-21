import React from 'react';
import Signup from './Signup';
import bg from './LoginBg.jpg'
import Home from './Home';
import { useSupplier } from './UserSlice';
import UserDemo from './UserDemo';
function App() {
  console.log(useSupplier())
  return (
  //  <div style={{ backgroundImage: `url(${bg})` }}  className='bg-cover w-full h-screen '>

  //         <Signup/>
      
  //   </div>
  // <div>
  //   <Home/>
  // </div>
  <div >
    <UserDemo/>
  </div>
  

  );
}

export default App;
