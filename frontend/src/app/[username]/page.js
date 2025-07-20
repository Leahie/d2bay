"use client"
import { useState, useEffect } from "react"
import { useParams } from 'next/navigation'
import { getUser } from "@/utils/api/profile"
import { useAuth } from '../../context/AuthContext'



export default function UserPage(){
    const params = useParams();
    const { user:account } = useAuth();
    const [user, setUser] = useState({})

    useEffect(() => {
        const fetchUser = async () => {
                const response = await getUser(params.username);
                setUser(response);
            }
        fetchUser();
    }, [])

    const isOwner = user?.username && account?.username && user.username === account.username;

    return (
        <>
        <a href="/">Home</a>
        <h1>{user.username}</h1>
        {isOwner ? <button>Edit</button> : <></> }
        </>
    )
}