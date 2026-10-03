"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import DashboardLayout from "@/components/layout/DashboardLayout";
import { getAccessToken } from "@/lib/auth";

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    const router = useRouter();

    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const accessToken = getAccessToken();

        if (!accessToken) {
            router.replace("/login");
            return;
        }

        setToken(accessToken);
        setIsLoading(false);
    }, [router]);

    if (isLoading) {
        return null;
    }

    if (!token) {
        return null;
    }

    return <DashboardLayout>{children}</DashboardLayout>;
}

