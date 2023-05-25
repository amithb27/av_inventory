import React from 'react'
import Footer from './Footer'
import Sidebar from './SideBar'
import Header from './Header'
import Directory from './Breadcrumbs'
import HomeTabs from './Tabs'
import UserDemo from './UserDemo'
function Home() {
  return (
    <div>
      <Header />
      <div className='hidden lg:block ml-8 '><Directory/></div>
      <div className='flex flex-row'>
      
      <div className='w-4/12 min-w-[350px] '><Sidebar/></div>
      
      <div className='w-7/12'><HomeTabs/>
      <UserDemo/> </div>
      </div>
      
    
    <div className='mt-[400px]'>
        <Footer/>
    </div>
    </div>
  )
}

export default Home