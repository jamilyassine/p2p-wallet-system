"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
    const router = useRouter();

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleRegister = async () => {
        setError("");

        const response = await fetch("http://localhost:8000/users/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name,
                email,
                password,
            }),
        });

        if (!response.ok) {
            const data = await response.json();
            setError(data.detail ?? "Registration failed");
            return;
        }

        router.push("/login");
    };

    return (
    <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col gap-4 w-full max-w-sm bg-white rounded-xl shadow-lg p-10">
            <h1 className="text-3xl font-bold">Create Account</h1>

            <p className="text-gray-500">
                Create your wallet account
            </p>

            <label>Name</label>
            <input
                placeholder="Your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />

            <label>Email</label>
            <input
                type="email"
                placeholder="john@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />

            <label>Password</label>
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />

            {error && <p className="text-red-600">{error}</p>}

            <button
                onClick={handleRegister}
                className="w-full py-3 bg-purple-600 hover:bg-purple-700 transition-colors text-white rounded-lg"
            >
                Register
            </button>

            <p className="text-sm text-gray-500 text-center">
                Already have an account?{" "}
                <button
                    onClick={() => router.push("/login")}
                    className="text-purple-600 hover:text-purple-700 font-medium"
                >
                    Log in
                </button>
            </p>
        </div>
    </div>
);
}