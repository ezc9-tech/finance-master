import { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router';

function RegistrationPage() {

  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    if (data.password !== data.confirm_password) {
        toast.error('Passwords do not match');
        setIsLoading(false);
        return;
    }

    delete data.confirm_password;

    try {
        const response = await axios.post("http://localhost:8000/auth/register", data);
        console.log("Registration successful", response.data)
        toast.success('Registration successful');
        navigate('/dashboard');
    } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Registration failed';
        toast.error(errorMessage);
    } finally {
        setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-md p-8 text-gray-800">
        <h2 className="text-2xl font-bold text-center mb-6">
          Create an Account
        </h2>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-5">
          <div className="flex flex-col space-y-1">
            <label
              className="text-sm font-medium text-gray-700"
              htmlFor="email"
            >
              Email
            </label>
            <input
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              type="email"
              name="email"
              id="email"
              placeholder="you@example.com"
            />
          </div>

          <div className="flex flex-col space-y-1">
            <label
              className="text-sm font-medium text-gray-700"
              htmlFor="username"
            >
              Username
            </label>
            <input
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              type="text"
              name="username"
              id="username"
              placeholder="Choose a username"
            />
          </div>

          <div className="flex flex-col space-y-1">
            <label
              className="text-sm font-medium text-gray-700"
              htmlFor="password"
            >
              Password
            </label>
            <input
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              type="password"
              name="password"
              id="password"
              placeholder="••••••••"
            />
          </div>

          <div className="flex flex-col space-y-1">
            <label
              className="text-sm font-medium text-gray-700"
              htmlFor="confirm_password"
            >
              Confirm Password
            </label>
            <input
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              type="password"
              name="confirm_password"
              id="confirm_password"
              placeholder="••••••••"
            />
          </div>

          <button
            className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all mt-4"
            type="submit"
          >
            {isLoading ? 'Registering...' : 'Register'}
          </button>

          <p className="text-sm text-gray-600 text-center mt-4">
            Already have an account? <a href="/login" className="text-blue-600 hover:underline">Login</a>
          </p>

        </form>
      </div>
    </div>
  );
}

export default RegistrationPage;
