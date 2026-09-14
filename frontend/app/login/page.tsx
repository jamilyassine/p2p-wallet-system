"use client";

import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
    const router = useRouter();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async () => {
        setError("");

        try {
            const response = await fetch(
                "http://localhost:8000/users/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email,
                        password,
                    }),
                }
            );

            if (!response.ok) {
                setError("Invalid email or password");
                return;
            }

            const data = await response.json();

            localStorage.setItem("access_token", data.access_token);

            router.push("/dashboard");
        } catch (error) {
            console.error(error);
            setError("Unable to connect to the server");
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 p-5">
            <div className="mx-auto flex min-h-[calc(100vh-40px)] w-full max-w-7xl overflow-hidden rounded-2xl bg-white shadow-xl">
                {/* Left branding panel */}
                <div className="relative hidden w-1/2 overflow-hidden bg-[#07133f] px-10 py-10 text-white lg:flex lg:flex-col">
                    <div className="flex items-center gap-3">
                        <Image
                            src="/images/p2p-wallet-logo.png"
                            alt="P2P Wallet"
                            width={40}
                            height={40}
                            className="rounded-xl"
                            priority
                        />

                        <span className="text-xl font-semibold">
                            P2P Wallet
                        </span>
                    </div>

                    <div className="mt-8 max-w-sm">
                        <h2 className="text-lg font-semibold">
                            Secure. Fast. Reliable.
                        </h2>

                        <p className="mt-2 text-sm leading-6 text-slate-300">
                            Peer-to-peer money transfers you can trust.
                        </p>
                    </div>

                    <div className="flex flex-1 items-center justify-center py-8">
                        <Image
                            src="/images/login-illustration.png"
                            alt="P2P money transfer"
                            width={520}
                            height={520}
                            className="max-h-[420px] w-auto object-contain"
                            priority
                        />
                    </div>
                </div>

                {/* Login panel */}
                <div className="flex w-full items-center justify-center px-6 py-10 lg:w-1/2 lg:px-12">
                    <div className="w-full max-w-md">
                        <h1 className="text-3xl font-bold text-slate-900">
                            Welcome back
                        </h1>

                        <p className="mt-2 text-sm text-slate-500">
                            Login to your account
                        </p>

                        <div className="mt-8 space-y-5">
                            <div>
                                <label
                                    htmlFor="email"
                                    className="mb-2 block text-sm font-medium text-slate-800"
                                >
                                    Email
                                </label>

                                <input
                                    id="email"
                                    type="email"
                                    placeholder="you@example.com"
                                    value={email}
                                    onChange={(e) =>
                                        setEmail(e.target.value)
                                    }
                                    className="h-11 w-full rounded-lg border border-slate-200 px-3 text-sm outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
                                />
                            </div>

                            <div>
                                <label
                                    htmlFor="password"
                                    className="mb-2 block text-sm font-medium text-slate-800"
                                >
                                    Password
                                </label>

                                <input
                                    id="password"
                                    type="password"
                                    placeholder="Password"
                                    value={password}
                                    onChange={(e) =>
                                        setPassword(e.target.value)
                                    }
                                    onKeyDown={(e) => {
                                        if (e.key === "Enter") {
                                            handleLogin();
                                        }
                                    }}
                                    className="h-11 w-full rounded-lg border border-slate-200 px-3 text-sm outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
                                />
                            </div>

                            {error && (
                                <p className="text-sm text-red-600">
                                    {error}
                                </p>
                            )}

                            <button
                                onClick={handleLogin}
                                className="h-11 w-full rounded-lg bg-purple-600 font-medium text-white transition hover:bg-purple-700"
                            >
                                Log in
                            </button>

                            <p className="text-center text-sm text-slate-500">
                                Don't have an account?{" "}
                                <button
                                    onClick={() => router.push("/register")}
                                    className="font-medium text-purple-600 hover:text-purple-700"
                                >
                                    Sign up
                                </button>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}


