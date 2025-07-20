'use client'

import { useEffect, useState } from "react";
import { getUserList } from "@/utils/api/profile";
import { useAuth } from "@/context/AuthContext";

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
      <h1>Users</h1>
      <div className="m-4 font-[family-name:var(--font-geist-sans)]">
          {users.map((item, index)=>(
            <a className="block" href={`/${item.username}`} key={index}>{item.username}</a>
          ))}
      </div>

      {!!user ? <button onClick={logoutUser} >logout</button> : <></>}
    </>
  );
}
