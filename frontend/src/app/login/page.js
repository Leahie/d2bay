'use client'
import { useState, useEffect } from 'react'
import { useAuth } from '@/context/AuthContext'
import Link from 'next/link'

export default function Login() {
  const [credentials, setCredentials] = useState({ username: '', password: '' })
  const [previousUrl, setPreviousUrl] = useState('/')
  const [error, setError] = useState(null);

  const { loginUser } = useAuth()

  const handleSubmit = async(e) => {
    setError(null);
    e.preventDefault()
    try {
      const response = await loginUser(credentials, previousUrl);
      if (response.errors != null){
        throw new Error('Failed to sign in, please check your credentials')
      }
    } catch (error) {
      setError(error.message);
    }
  }

  useEffect(() => {
    const temp = document.referrer;
    if (temp && temp !== window.location.href && temp !== '/register') {
      setPreviousUrl(temp)
    } else {
      setPreviousUrl('/')
    }
  }, [])

  return (
    <div className="h-screen flex items-stretch justify-center py-5 px-3 flex-col sm:flex-row">
      {/* Left vertical title section */}
      <div className="sm:w-96 space-y-8 bg-light/70 flex items-center justify-center content-center">
        <h1 className="text-body sm:text-[84px] text-[24px] font-bold tracking-[1em] sm:tracking-widest sm:[writing-mode:vertical-rl] sm:[text-orientation:upright]">
          Login
        </h1>
      </div>

      {/* Right form section */}
      <div className="flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 ">
        <div className="max-w-md w-full space-y-5">
          <div>
            <h2 className="text-3xl font-bold text-black">
              Signin.
            </h2>
          </div>
          <form className="mt-3 space-y-6" onSubmit={handleSubmit}>
            <div className="rounded-md flex flex-col gap-4">
              <div>
                <label htmlFor="username" className="sr-only">Username</label>
                <input
                  id="username"
                  name="username"
                  type="username"
                  autoComplete="username"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:bg-white focus:ring-light focus:border-light focus:z-10 sm:text-sm"
                  placeholder="Username"
                  value={credentials.username}
                  onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">Password</label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:bg-white focus:ring-light focus:border-light focus:z-10 sm:text-sm"
                  placeholder="Password"
                  value={credentials.password}
                  onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                />
              </div>
            </div>

            {error && (
              <div className="text-red-500 text-sm mt-2">
                {error}
              </div>
            )}

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-dark/80 hover:bg-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-light"
              >
                Login
              </button>
            </div>
          </form>
          <div className="text-sm text-center">
            <Link href="/register" className="font-medium text-dark hover:text-highlight">
              Don&apos;t have an account yet? Sign up
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
