"use client";

import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";

import DashboardCard from "@/components/layout/DashboardCard";
import PageHeader from "@/components/layout/PageHeader";

import type { UserResponse } from "@/types/user";

export default function SettingsPage() {
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
                title="Settings"
                subtitle="Manage your account and security"
                userName={user?.name}
                userEmail={user?.email}
            />

            <div className="space-y-6">
                <DashboardCard
                    title="Account"
                    value={
                        <div className="space-y-4">
                            <div>
                                <p className="text-sm text-gray-500">
                                    Account email
                                </p>
                                <p className="font-medium">
                                    {user?.email}
                                </p>
                            </div>

                            <div>
                                <p className="text-sm text-gray-500">
                                    Authentication
                                </p>
                                <p className="font-medium">
                                    JWT authentication enabled
                                </p>
                            </div>
                        </div>
                    }
                />

                <DashboardCard
                    title="Security"
                    value={
                        <div>
                            <p className="text-sm text-gray-500">
                                Session
                            </p>
                            <p className="font-medium">
                                Your account is protected by authenticated
                                sessions.
                            </p>
                        </div>
                    }
                />
            </div>
        </div>
    );
}

