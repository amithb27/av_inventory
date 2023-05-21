import { createSlice } from "@reduxjs/toolkit";
import { useSelector } from 'react-redux';
const UserSlice=createSlice({
    initialState:{},
    name:"UserSlice",
    reducers:{
        reducer1(state,action){
            state+=action.payload
        }
    }
})
const useSupplier=function(){
    const value=useSelector(state=>state.userReducer)
    return (value)
}
export default UserSlice.reducer
export const {reducer1}=UserSlice.actions
export {useSupplier}