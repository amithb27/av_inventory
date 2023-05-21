import React from 'react'
import Footer from './Footer'
import Sidebar from './SideBar'
import Header from './Header'
import Directory from './Breadcrumbs'
import HomeTabs from './Tabs'
function Home() {
  return (
    <div>
      <Header />
      <div className='hidden lg:block ml-8 '><Directory/></div>
      <div className='flex flex-row'>
      
      <div className='w-4/12'><Sidebar/></div>
      <div className='w-7/12'><HomeTabs/></div>
      </div>
      
    
    <div className='mt-[400px]'>
        <Footer/>
    </div>
    </div>
  )
}

export default Home