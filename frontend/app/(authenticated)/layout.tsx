"use client";

import { useEffect, useSyncExternalStore } from "react";
import { useRouter } from "next/navigation";

import DashboardLayout from "@/components/layout/DashboardLayout";
import { getAccessToken } from "@/lib/auth";

function subscribe(callback: () => void) {
    window.addEventListener("storage", callback);

    return () => {
        window.removeEventListener("storage", callback);
    };
}

function getClientSnapshot() {
    return getAccessToken();
}

function getServerSnapshot() {
    return null;
}

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    const router = useRouter();

    const token = useSyncExternalStore(
        subscribe,
        getClientSnapshot,
        getServerSnapshot
    );

    useEffect(() => {
        if (!token) {
            router.replace("/login");
        }
    }, [token, router]);

    if (!token) {
        return null;
    }

    return <DashboardLayout>{children}</DashboardLayout>;
}