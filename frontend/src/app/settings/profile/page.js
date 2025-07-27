"use client"
import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { getUser } from '@/utils/api/profile';

export default function EditProfile() {
  const { user, authTokens, loading } = useAuth();
  const [profile, setProfile] = useState({
    username: '', 
    first_name: '',
    last_name: '',
    bio: '',
    location: '',
    birthday: ''
  });

    useEffect(() => {
        if (!loading){
            const fetchUser = async () => {
                    const response = await getUser(user?.username);
                    setProfile(response);
                }
            fetchUser();
        }
    }, [loading])

  const handleChange = e => {
    setProfile(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/user/update/', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authTokens.access}`
        },
        body: JSON.stringify(profile)
      });
      if (!response.ok) throw new Error('Failed to update profile');
      alert('Profile updated!');
    } catch (error) {
      console.error(error);
      alert('Error updating profile');
    }
  };

  if (!user) return <div>Loading...</div>;

  return (
    <form className="w-full max-w-lg mx-auto" onSubmit={handleSubmit}>
      {/* Username (disabled) */}
      <div className="flex flex-wrap -mx-3 mb-6">
        <div className="w-full px-3">
          <label
            className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
            htmlFor="username"
          >
            Username
          </label>
          <input
            disabled
            id="username"
            name="username"
            value={profile.username}
            className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white"
          />
        </div>
      </div>

      {/* First and Last Name */}
      <div className="flex flex-wrap -mx-3 mb-6">
        <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label
            className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
            htmlFor="first_name"
          >
            First Name
          </label>
          <input
            id="first_name"
            name="first_name"
            type="text"
            value={profile.first_name}
            onChange={handleChange}
            placeholder="Jane"
            className="appearance-none block w-full bg-white text-gray-700 border border-slate-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:border-gray-700"
          />
          {/* Add validation message here if needed */}
        </div>

        <div className="w-full md:w-1/2 px-3">
          <label
            className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
            htmlFor="last_name"
          >
            Last Name
          </label>
          <input
            id="last_name"
            name="last_name"
            type="text"
            value={profile.last_name}
            onChange={handleChange}
            placeholder="Doe"
            className="appearance-none block w-full bg-white text-gray-700 border border-slate-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:border-gray-700"
          />
        </div>
      </div>

      {/* Bio */}
      <div className="flex flex-wrap -mx-3 mb-6">
        <div className="w-full px-3">
          <label
            className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
            htmlFor="bio"
          >
            Bio
          </label>
          <textarea
            id="bio"
            name="bio"
            value={profile.bio}
            onChange={handleChange}
            className="appearance-none block w-full bg-white text-gray-700 border border-slate-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:border-gray-700"
            rows={4}
            placeholder="Tell us about yourself"
          />
        </div>
      </div>

      {/* Location and Birthday */}
      <div className="flex flex-wrap -mx-3 mb-6">
        <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label
            className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
            htmlFor="location"
          >
            Location
          </label>
          <input
            id="location"
            name="location"
            type="text"
            value={profile.location}
            onChange={handleChange}
            placeholder="City, State"
            className="appearance-none block w-full bg-white text-gray-700 border border-slate-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:border-gray-700"
          />
        </div>

        <div className="w-full md:w-1/2 px-3">
          <label
            className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
            htmlFor="birthday"
          >
            Birthday
          </label>
          <input
            id="birthday"
            name="birthday"
            type="date"
            value={profile.birthday}
            onChange={handleChange}
            className="appearance-none block w-full bg-white text-gray-700 border border-slate-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:border-gray-700"
          />
        </div>
      </div>

      {/* Submit */}
      <div className="flex flex-wrap -mx-3 mb-6">
        <div className="w-full px-3 text-right">
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Save Changes
          </button>
        </div>
      </div>
    </form>
  );
}
