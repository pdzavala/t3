import { Route, Routes } from 'react-router-dom'
import App from "./App"
import Flight from "../views/Flight"
import Charts from "../views/Charts"



export default function Routing() {
    return (
        <Routes>
            <Route path="/" element={<App />} />
            <Route path="/flight/:flightNumber" element={<Flight />} />
            <Route path="/charts" element={<Charts />} />
            
        </Routes>
    )
}
