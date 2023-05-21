import React  ,{useEffect} from "react";


export const GetData=async(subDomain,type,func)=>{
    let outList=[] ;

      
        const domain="http://127.0.0.1:8000/"
        const url= domain+subDomain
        console.log(url)
        let outData;
       const rawData= await fetch(url,{
            method:type,
            headers:{
                'Content-Type': 'application/json',
            },
            
            
        })
       const data= await rawData.json()
       console.log(data ,"ASdfdf")
       data.map(ele=>{
           outData={
            name:ele.name
            ,role:ele.role.name,
            reportedTo:ele.reporting_Person,
            pk:ele.pk
         }
        outList.push(outData)
        })
        setTimeout(()=>{
            func(outList)
        },1000) 
        
        // .then(response=>
        //     response.json()
    
       
        // ).then(data=>{
        //     console.log(data)
        
        //     
        //         outList.push(outData)
        //     })
      
        //  console.log(outList)
        // })
        // .catch(err=>console.log(err))
        
        
    
        
    return outList
    
}