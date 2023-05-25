import React,{useState,useEffect } from "react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import {
  
    Card,
    Input,
    Button,
  Dialog,
  DialogHeader,
  DialogBody,
  IconButton,
  Typography,

  } from "@material-tailwind/react";
  import DeleteIcon from '@mui/icons-material/Delete';

import {requestBackend} from './Fetching'
  const TABLE_HEAD = ["Name", "Role", "reportedTo",""];
  export default function Form() {
    const [TABLE_ROWS,setTABLE_ROWS] = useState([])
    const [changedData, setChangedData] = useState(1) 
    
    const [data,setData]=useState({Adress:{},role:{},created_By:"mani"})
     
    const [open, setOpen] = React.useState(false);
    const handleOpen = () => setOpen((cur) => !cur);
   
     useEffect(()=>{
      let outList=[]
      let outData
         const data = requestBackend("employee/","GET")
         console.log(data ,"ASdfsdfdfd")
         data.then(res=>{
          res.map(ele=>{
            outData={
             name:ele.name
             ,role:ele.role.name,
             reportedTo:ele.reporting_Person,
             pk:ele.pk
          }
          outList.push(outData)
          return null
         } ) 
         setTABLE_ROWS(outList)
         })
        
         
     },[changedData])
        
    return (
        <div>
            <Button onClick={handleOpen} className="w-4/12 ml-[650px] mb-10  ">Register an employee </Button>

          <Dialog  className="bg-transparent" size="lg" open={open} handler={handleOpen} > 
      
      <DialogHeader>
      <IconButton
        color="blue"
        size="sm"
        variant="text"
        className="ml-auto"
        onClick={handleOpen}
      >
        <XMarkIcon strokeWidth={4}  className="h-5 w-5 mr-auto" />
      </IconButton>
      </DialogHeader>
     <DialogBody>
      <Card className="mx-auto px-52" color="transparent" shadow={false}>
     <Typography variant="h4" color="blue">
       Register Form 
  </Typography>
    <Typography color="gray" className="mt-1 font-normal">
      Enter Emplooyee details to register.
   </Typography>
       <form onSubmit={(e)=>{

        e.preventDefault()
        console.log("submited")
         const BackendPromsie= requestBackend("employee/","POST",data)
         console.log(BackendPromsie,"BackendPromsie")
          BackendPromsie.then(()=>{
            setChangedData(pre=>pre+1)
            handleOpen()
           
          }).catch(err=>console.log(err))
  
       
     }} className="mt-8 mb-2 w-80 max-w-screen-lg sm:w-96">
      <div className=" flex flex-row">
      <div className="mb-4 flex flex-col gap-6">
        <Input onChange={(e)=>{
            setData({...data,name:e.target.value})
        }} size="md" label="Name" color="white" />
        <Input onChange={(e)=>{
            setData({...data,email:e.target.value})
        }} size="md" label="Email"color="white" />
        
        <Input onChange={(e)=>{
            setData({...data,phone:e.target.value})
        }}size="md" label="phone" color="white"/>
        <Input onChange={(e)=>{
            setData({...data,role:{name:e.target.value}})
        }} size="md" label="Role" color="white" />
        <Input onChange={(e)=>{
            setData({...data,reporting_Person:e.target.value})
        }} size="md" label="Reporting Person" color="white" />
      </div>

      <div className="mx-10 mb-4 flex flex-col gap-6">
      <Input onChange={(e)=>{
            setData({...data,Adress:{...data.Adress,country:e.target.value}})
        }} size="md" label="country" color="white"/>
       <Input onChange={(e)=>{
            setData({...data,Adress:{...data.Adress,state:e.target.value}})
        }} size="md" label="state" color="white"/>
        <Input onChange={(e)=>{
            setData({...data,Adress:{...data.Adress,city:e.target.value}})
        }} size="md" label="city" color="white"/>
        <Input onChange={(e)=>{
            setData({...data,Adress:{...data.Adress,zip_code:e.target.value}})
        }} size="md" label="pin code" color="white" />
        <Input onChange={(e)=>{
            setData({...data,Adress:{...data.Adress,zone:e.target.value}})
        }} size="md" label="zone" color="white"/>
      </div>
      </div>

      <Button type="submit"  className="mt-6" fullWidth>
     Register
      </Button>
     
    </form>
  </Card>
  </DialogBody>    
          
           
   
    
     </Dialog>
      
      <div className=' ml-[260px] w-6/12'> <Typography variant="h4" color="blue-gray">
          Emplooyee List
        </Typography></div>
      <Card className=" overflow-scroll h-full  w-[1000px]">
      <table className="w-full min-w-max table-auto text-left">
        <thead>
          <tr>
            {TABLE_HEAD.map((head) => (
              <th key={head} className="border-b  border-blue-gray-100 bg-blue-gray-50 p-4">
                <Typography
                  variant="small"
                  color="blue-gray"
                  className="font-normal leading-none opacity-70"
                >
                  {head}
                </Typography>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {TABLE_ROWS.map(({ name, role, reportedTo ,pk}, index) => {
            const isLast = index === TABLE_ROWS.length - 1;
            const classes = isLast ? "p-4" : "p-4 border-b border-blue-gray-50";
 
            return (
              <tr  key={pk}>
                <td className={classes}>
                  <Typography variant="small" color="blue-gray" className="font-normal">
                    {name}
                  </Typography>
                </td>
                <td className={classes}>
                  <Typography variant="small" color="blue-gray" className="font-normal">
                    {role}
                  </Typography>
                </td>
                <td className={classes}>
                  <Typography variant="small" color="blue-gray" className="font-normal">
                    {reportedTo}
                  </Typography>
                </td>
                <td className={classes}>
                  <Typography  variant="small" color="red" className="cursor-pointer font-medium">
                    <div onClick={()=>{
                        const Promsie=requestBackend("employee/"+pk , "DELETE" )
                        Promsie.then(()=>{
                          setChangedData(data=>data-1)
                        })
                      

                    }} >
                      <DeleteIcon /></div>
                  </Typography>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </Card>
      </div>
    


    );
  }
  