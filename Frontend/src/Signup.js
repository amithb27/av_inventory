import React from "react";

import logo from './logo.png'
import {
  Card,
  CardHeader,
  CardBody,
  Input,
  Button,
  Typography,
  Tabs,
  TabsHeader,
  TabsBody,
  Tab,
  TabPanel,
  Checkbox
} from "@material-tailwind/react";
  
export default function Example() {

  const [type, setType] = React.useState("in");

 
return (
  <div className="  pt-32 w-10/12 mx-auto  xl:ml-16 max-w-xl   ">
<Card >
<CardHeader
        color={type==="in" ?"blue":"orange"}
        floated={false}
        shadow={false}
        className="m-0 grid place-items-center rounded-b-none py-8 px-4 text-center"
      >
        <div className="mb-2 rounded-[100000px] border border-white/10 bg-white/10 p-2 text-white ">
          <img src={logo} height={60} width={60}></img>
</div>
        <Typography className="italic" variant="h4" color="white">
Analytics Valley
</Typography>
</CardHeader>
<CardBody>
<Tabs value={type}  className=" overflow-visible  ">
<TabsHeader 
  indicatorProps={{
    className: type==="in"?"bg-blue-100 shadow-none ":"bg-deep-orange-100 shadow-none ",
  }}
className="relative z-0 ">
<Tab value="in" onClick={() => setType("in")}>
SignIn
</Tab>
<Tab value="up"  onClick={() => setType("up")}>
SignUp
</Tab>
</TabsHeader>
<TabsBody
className=" !overflow-x-hidden !overflow-y-visible"
animate={{
              initial: {
                x: type === "in" ? 400 : -400,
              },
              mount: {
                x: 0,
              },
              unmount: {
                x: type === "in" ? 400 : -400,
              },
            }} >
<TabPanel value="in" className="p-0">
<form className="mt-12 flex flex-col gap-4">
<div>
<div className="mt-4 ">
<Input   type="email" label="Email Address" icon={
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
  <path d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 5.493a3 3 0 01-3.144 0L1.5 8.67z" />
  <path d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 5.978a1.5 1.5 0 001.572 0L22.5 6.908z" />
</svg>

} />
</div>
</div>
                <div className="my-6">
                  
 
                  <Input
                    label="Password"
                    type="password"
                    
                    onChange={(event) => {}}
                    icon={
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
  <path fillRule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clipRule="evenodd" />
</svg>

                    }
                  />
                </div>
                <Button size="lg">Log In</Button>
                <Typography
                  variant="small"
                  color="gray"
                  className="mt-2 flex items-center justify-center gap-2 font-normal opacity-60"
                >
                     <Checkbox id="ripple-on" label="Remember Me" ripple={true} />
                  
                </Typography>
              </form>
            </TabPanel>
            <TabPanel value="up" className="p-0">
              <form className="mt-12 flex flex-col gap-4">
                <div className="mt-2">
                  
                  <Input type="text" label="Full Name" />
                </div>
 
                <div className="">
                 
 
                
                  <Input
                    label="Email"
                    containerProps={{ className: "mt-2" }}
                  />
                </div>
                <div className="">
                 
 
                
                 <Input
                   label="Password"
                   type="password"
                   
                 />
               </div>
               <div >
                
                 <Input
                 type="password"
                   label="Re-enter Password"
                   containerProps={{ className: "mt-2" }}
                 />
               </div>
             
                <Button size="lg" color="orange" className="h-12 ">
                    Sign Up
                </Button>
               
              </form>
            </TabPanel>
          </TabsBody>
        </Tabs>
      </CardBody>
    </Card>
    </div>
);
}