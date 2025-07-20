export async function getUserList(){
    const res = await fetch(`http://127.0.0.1:8000/api/user/`, {
        method: "GET", 
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error("Failed to fetch users");
    }

    return res.ok ? await res.json() : null;
}

export async function getUser(username){
    const res = await fetch(`http://127.0.0.1:8000/api/user/${username}`, {
        method: "GET", 
        headers: {
            "Content-Type": "application/json",
        }, 
    });

    if (!res.ok) {
        throw new Error("Failed to fetch user")
    }

    return res.ok ? await res.json() : null;
}