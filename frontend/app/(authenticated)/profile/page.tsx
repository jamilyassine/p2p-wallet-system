"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";

import DashboardCard from "@/components/layout/DashboardCard";
import PageHeader from "@/components/layout/PageHeader";

import type { UserResponse } from "@/types/user";

export default function ProfilePage() {
    const [user, setUser] = useState<UserResponse | null>(null);

    useEffect(() => {
        async function fetchUser() {
            try {
                const response = await apiFetch("/users/me");

                if (!response) return;

                const data = await response.json();
                setUser(data);
            } catch (error) {
                console.error(error);
            }
        }

        fetchUser();
    }, []);

    return (
        <div>
            <PageHeader
                title="Profile"
                subtitle="View your account information"
                userName={user?.name}
                userEmail={user?.email}
            />

            <DashboardCard
                title="Personal Information"
                value={
                    <div className="space-y-4">
                        <div>
                            <p className="text-sm text-gray-500">Name</p>
                            <p className="font-medium">{user?.name}</p>
                        </div>

                        <div>
                            <p className="text-sm text-gray-500">Email</p>
                            <p className="font-medium">{user?.email}</p>
                        </div>

                        <div>
                            <p className="text-sm text-gray-500">
                                Member since
                            </p>
                            <p className="font-medium">
                                {user?.created_at
                                    ? new Date(
                                          user.created_at
                                      ).toLocaleDateString()
                                    : ""}
                            </p>
                        </div>
                    </div>
                }
            />
        </div>
    );
}