'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '../../context/AuthContext'

export default function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: ''
  })
  const [error, setError] = useState('')

  const { registerUser } = useAuth()
  const router = useRouter()

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const result = await registerUser(formData)

    if (result.success) {
      router.push('/login')
    } else {
      setError(result.errors.email || result.errors.password || 'Registration failed')
    }
  }

  
  return (
    <div className="h-screen flex items-stretch justify-center py-5 px-3 flex-col sm:flex-row ">
      <div className="sm:w-96  space-y-8 bg-light/70 flex items-center justify-center content-center ">
        <h1 className="text-body sm:text-[84px] text-[24px] font-bold tracking-[1em]  sm:tracking-widest sm:[writing-mode:vertical-rl] sm:[text-orientation:upright]">
          Trade 
        </h1>
      </div>
      <div className=" flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 ">
        <div className="max-w-md w-full space-y-5">
          <div>
            <h2 className="  text-3xl font-bold text-black">
              Signup.
            </h2>
          </div>
          <form className="mt-3 space-y-6" onSubmit={handleSubmit}>
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="rounded-md  flex flex-col gap-4">
              <div>
                <label htmlFor="username" className="sr-only">
                  Username
                </label>
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:bg-white focus:ring-light focus:border-light focus:z-10 sm:text-sm"
                  placeholder="Username"
                  value={formData.username}
                  onChange={handleChange}
                  autoComplete="off"
                />
              </div>
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Email address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-light focus:bg-white focus:border-light focus:z-10 sm:text-sm"
                  placeholder="Email address"
                  value={formData.email}
                  onChange={handleChange}
                  autoComplete="off"
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="off"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-light focus:bg-white focus:border-light focus:z-10 sm:text-sm"
                  placeholder="Password"
                  value={formData.password}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="password2" className="sr-only">
                  Confirm Password
                </label>
                <input
                  id="password2"
                  name="password2"
                  type="password"
                  autoComplete="new-password"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:bg-white focus:ring-light focus:border-light focus:z-10 sm:text-sm"
                  placeholder="Confirm Password"
                  value={formData.password2}
                  onChange={handleChange}
                  
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
                Register
              </button>
            </div>
          </form>
          <div className="text-sm text-center">
            <Link href="/login" className="font-medium text-dark hover:text-highlight">
              Already have an account? Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}