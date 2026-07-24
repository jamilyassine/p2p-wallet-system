"use client";
import type { UserResponse } from "../../types/user";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
    const router = useRouter();

    const [users, setUsers] = useState<UserResponse[]>([]);
    const [selectedUser, setSelectedUser] = useState<UserResponse | null>(null);

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/users")
            .then((response) => response.json())
            .then(setUsers);
    }, []);

    const handleCreateUser = () => {
        fetch("http://localhost:8000/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name,
                email,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                setUsers((previousUsers) => [...previousUsers, data]);
                setSelectedUser(data);
                setName("");
                setEmail("");
            });
    };

    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="flex flex-col gap-4 w-full max-w-sm bg-white rounded-xl shadow-lg p-10">
                <h1 className="text-3xl font-bold">
                    Mock Login
                </h1>

                <p className="text-gray-500 mb-4">
                    Select an existing user or create a new one
                </p>

                <h2 className="font-semibold">
                    Existing Users
                </h2>

                {users.map((user) => (
                    <button
                        key={user.id}
                        onClick={() => {
                            setSelectedUser(user);
                            router.push(`/dashboard?userId=${user.id}`);
                        }}
                        className="w-full text-left px-3 py-2 border rounded hover:bg-gray-100"
                    >
                        {user.name}
                    </button>
                ))}

                {selectedUser && (
                    <p className="text-green-600">
                        Selected: {selectedUser.name}
                    </p>
                )}

                <hr className="my-4" />

                <h2 className="font-semibold">
                    Create New User
                </h2>

                <label>Name</label>

                <input
                    type="text"
                    placeholder="John Doe"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />

                <label>Email</label>

                <input
                    type="email"
                    placeholder="john@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />

                <button
                    onClick={handleCreateUser}
                    className="w-full py-3 bg-purple-600 hover:bg-purple-700 transition-colors text-white rounded-lg"
                >
                    Create User
                </button>
            </div>
        </div>
    );
}