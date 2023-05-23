


export const requestBackend=async(subDomain,type,content)=>{
       let body= JSON.stringify(content) 
        const domain="http://127.0.0.1:8000/"
        const url= domain+subDomain
        console.log(url , body )
       
       const rawData= await fetch(url,{
            method:type,
            headers:{
                'Content-Type': 'application/json',
            },
  
            body

        })
  if (type==="GET") { 
       const data = await rawData.json()
         
       return data
  }
  if (type==="POST") { 
     
     return rawData
    
}
}