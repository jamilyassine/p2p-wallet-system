export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
    <div className="flex flex-col gap-4 w-full max-w-sm bg-white rounded-xl shadow-lg p-10">
      <h1 className="text-3xl font-bold">Welcome back</h1>
      <p className="text-gray-500 mb-4">Login to your account</p>
      <label>Email</label>
      <input type="email"
      placeholder="you@example.com"
      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500" />
      <label>Password</label>
      <input type="password"
      placeholder="••••••••" 
      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"/>
      <button className="w-full py-3 bg-purple-600 hover:bg-purple-700 transition-colors text-white rounded-lg" >Log In</button>
    </div>
    </div>
  );
}
