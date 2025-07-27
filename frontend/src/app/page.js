'use client'

import { useEffect, useState } from "react";
import { getUserList } from "@/utils/api/profile";
import { useAuth } from "@/context/AuthContext";
import Nav from '@/components/Nav';

export default function Home() {
  const [users, setUsers] = useState([]);
  const {user, logoutUser} = useAuth();

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await getUserList();
      setUsers(response);
    };

    fetchUsers();
  }, []);


  return (<>
      <Nav />
      <div className="ml-[15%]">
        <h1>Users</h1>
        <div className="m-4 font-[family-name:var(--font-geist-sans)]">
            {users.map((item, index)=>(
              <a className="block" href={`/${item.username}`} key={index}>{item.username}</a>
            ))}
        </div>

        {!!user ? <button onClick={logoutUser} >logout</button> : <a href="/login">login</a>}
      </div>    
    </>
  );
}
