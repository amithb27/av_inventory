import { configureStore } from "@reduxjs/toolkit";
import Reducer1 from "./UserSlice";

const store=configureStore({
    reducer:{
        userReducer:Reducer1
    }

})


export default store