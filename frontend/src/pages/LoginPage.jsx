import { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import { useNavigate } from "react-router";

function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    if (!data.email_or_password || !data.password) {
      toast.error("Please fill in all fields");
      setIsLoading(false);
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:8000/auth/login",
        data,
      );
      console.log("Login successful", response.data);
      toast.success("Login successful");
      navigate("/dashboard");
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail || "Registration failed";
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-md p-8 text-gray-800">
        <h2 className="text-2xl font-bold text-center mb-6">Welcome Back</h2>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-5">
          <div className="flex flex-col space-y-1">
            <label
              className="text-sm font-medium text-gray-700"
              htmlFor="email_or_password"
            >
              Email or Username
            </label>
            <input
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              type="text"
              name="email_or_password"
              id="email_or_password"
              required
              placeholder="Enter your email or username"
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
              required
              placeholder="••••••••"
            />
          </div>

          <button
            className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all mt-2"
            type="submit"
          >
            {isLoading ? "Logging in..." : "Login"}
          </button>

          <p className="text-sm text-gray-600 text-center mt-4">
            Don't have an account?{" "}
            <a href="/register" className="text-blue-600 hover:underline">
              Register
            </a>
          </p>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
