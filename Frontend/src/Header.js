import { useState, useEffect } from "react";
import logo from './logo.png'
import {

  MobileNav,
  Typography,
  Button,
  IconButton,

} from "@material-tailwind/react";
 
export default function Header() {
  const [openNav, setOpenNav] = useState(false);
 
  useEffect(() => {
    window.addEventListener("resize", () => window.innerWidth >= 570 && setOpenNav(false));
  }, []);
 
  const navList = (
    <ul className=" mb-4 mt-2 flex flex-col gap-2 lg:mb-0 lg:mt-0 lg:flex-row lg:items-center lg:gap-6">
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal hover:text-light-blue-600"
      >
        <div className="flex items-center">
          Home
        </div>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal hover:text-light-blue-600"
      >
        <div className="flex items-center">
          Services
        </div>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal hover:text-light-blue-600"
      >
        <div className="flex items-center">
          About Us
        </div>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal hover:text-light-blue-600"
      >
        <div className="flex items-center hover:text-light-blue-600">
         Help
        </div>
      </Typography>
    </ul>
  );
 
  return (
    <div className=" mx-auto max-w-screen-2xl py-2 px-6 lg:px-8 lg:py-4">
      <div className=" ml-6 container  flex items-center justify-between text-blue-gray-900">
        <div className="flex flex-row items-center">
        <div className="mt-2 ">
          <img  src={logo} height={80} width={80} alt=""></img>
        </div>
        <Typography
          as="a"
          href="#"
          className="mr-4 cursor-pointer py-1.5 font-medium"
        >
          Analytics Valley
        </Typography>
       

    
        </div>
        <div className="hidden lg:block lg:ml-auto lg:mr-8 ">{navList}</div>
        <Button variant="gradient" size="sm" className="hidden lg:inline-block ">
          <span>More Info</span>
        </Button>
        <IconButton
          variant="text"
          className=" ml-auto h-6 w-6 text-inherit hover:bg-transparent focus:bg-transparent active:bg-transparent lg:hidden"
          ripple={false}
          onClick={() => setOpenNav(!openNav)}
        >
          {openNav ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              className=" h-6 w-6"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            
          )}
        </IconButton>
      </div>
      <MobileNav open={openNav}>
        <div className="container mx-auto">
          {navList}
          <Button variant="gradient" size="sm" fullWidth className="mb-2">
            <span>More Info</span>
          </Button>
        </div>
      </MobileNav>
    </div>
  );
}
