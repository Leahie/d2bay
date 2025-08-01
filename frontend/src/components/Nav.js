"use client"
import { useAuth } from '@/context/AuthContext'
import { useState, useEffect, useRef } from 'react';


export default function Nav(props){
    const { user, logoutUser } = useAuth();
    const { page } = props;
    const [openDropdown, setOpenDropdown] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const dropdownRef = useRef();
    
    useEffect(() => {
    function handleClickOutside(e) {
        if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
            setOpenDropdown(false);
        }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);
    return(
        < >
        <nav className="fixed  top-0 z-50 w-full bg-white border-b border-med/40 dark:bg-gray-800 dark:border-gray-700 ">
        <div className="px-3 py-3 lg:px-5 lg:pl-3">
            <div className="flex items-center justify-between">
                <div className="flex items-center justify-start rtl:justify-end">
                    <button onClick={() => setSidebarOpen(!sidebarOpen)} type="button" className="inline-flex items-center p-2 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600">
                        <span className="sr-only">Open sidebar</span>
                        <svg className="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path clipRule="evenodd" fillRule="evenodd" d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"></path>
                        </svg>
                    </button>
                    <a href="/" className="flex ms-2 md:me-24">
                    <span className="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap dark:text-white">Logo</span>
                    </a>
                </div>
                {/* Beginning of Profile Picture Section */}
                <div className="flex items-center px-4">
                    <div className="flex items-center ms-3">
                        {user ? 
                        <div className="relative" ref={dropdownRef}>
                            <button
                            onClick={() => setOpenDropdown(!openDropdown)}
                            className="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
                            >
                            <img
                                className="w-8 h-8 rounded-full"
                                src={user?.avatar || "https://flowbite.com/docs/images/people/profile-picture-5.jpg"}
                                alt="user avatar"
                            />
                            </button>

                            {openDropdown && (
                            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-50 dark:bg-gray-700">
                                <div className="px-4 py-2 text-sm text-gray-900 dark:text-white">
                                {user?.username || "User"}
                                </div>
                                <ul className="py-1">
                                <li>
                                    <a href={`/${user?.username}`} className="block px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-600">Profile</a>
                                </li>
                                <li>
                                    <button onClick={logoutUser} className="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-600">
                                    Logout
                                    </button>
                                </li>
                                </ul>
                            </div>
                            )}
                        </div> : <a className='' href="/login">Login/Signup</a>}
                    </div>
                </div>
                {/* End of Profile Picture Section */}
            </div>
        </div>
    </nav>

        <aside id="logo-sidebar" className={`fixed  top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform -translate-x-full ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} bg-white border-r border-med/40 sm:translate-x-0 dark:bg-gray-800 dark:border-gray-700 `} aria-label="Sidebar">
        <div className="h-full px-3 pb-4 overflow-y-auto bg-white dark:bg-gray-800">
            <ul className="space-y-2 font-medium">
                <li>
                    <a href="/settings/profile" className={`flex ${Number(page) == 1 ? "  bg-slate-300 text-gray-900 dark:text-white " : ""}items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-med dark:hover:bg-gray-700 group`}>
                    <svg className="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-black dark:group-hover:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 21">
                        <path d="M16.975 11H10V4.025a1 1 0 0 0-1.066-.998 8.5 8.5 0 1 0 9.039 9.039.999.999 0 0 0-1-1.066h.002Z"/>
                        <path d="M12.5 0c-.157 0-.311.01-.565.027A1 1 0 0 0 11 1.02V10h8.975a1 1 0 0 0 1-.935c.013-.188.028-.374.028-.565A8.51 8.51 0 0 0 12.5 0Z"/>
                    </svg>
                    <span className="ms-3">Home</span>
                    </a>
                </li>
                <li>
                    <a href="#" className={`flex ${Number(page) == 2 ? "  bg-slate-300 text-gray-900 dark:text-white " : ""}items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-med dark:hover:bg-gray-700 group`}>
                    <svg className="shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-black dark:group-hover:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 18">
                        <path d="M6.143 0H1.857A1.857 1.857 0 0 0 0 1.857v4.286C0 7.169.831 8 1.857 8h4.286A1.857 1.857 0 0 0 8 6.143V1.857A1.857 1.857 0 0 0 6.143 0Zm10 0h-4.286A1.857 1.857 0 0 0 10 1.857v4.286C10 7.169 10.831 8 11.857 8h4.286A1.857 1.857 0 0 0 18 6.143V1.857A1.857 1.857 0 0 0 16.143 0Zm-10 10H1.857A1.857 1.857 0 0 0 0 11.857v4.286C0 17.169.831 18 1.857 18h4.286A1.857 1.857 0 0 0 8 16.143v-4.286A1.857 1.857 0 0 0 6.143 10Zm10 0h-4.286A1.857 1.857 0 0 0 10 11.857v4.286c0 1.026.831 1.857 1.857 1.857h4.286A1.857 1.857 0 0 0 18 16.143v-4.286A1.857 1.857 0 0 0 16.143 10Z"/>
                    </svg>
                    <span className="flex-1 ms-3 whitespace-nowrap">Feed</span>
                    </a>
                </li>

            </ul>
        </div>
        </aside>

        <div className="p-7 sm:ml-64 ">
        
        </div>

        </>
    )
}