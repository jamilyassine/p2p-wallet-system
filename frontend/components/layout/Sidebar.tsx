"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
    LayoutDashboard,
    Send,
    History,
    BookOpen,
    User,
    Settings,
    LogOut,
} from "lucide-react";

export default function Sidebar() {
    const pathname = usePathname();
    const router = useRouter();

    function handleLogout() {
        localStorage.removeItem("access_token");
        router.replace("/login");
    }

    const navItems = [
        {
            label: "Dashboard",
            href: "/dashboard",
            path: "/dashboard",
            icon: LayoutDashboard,
        },
        {
            label: "Send Money",
            href: "/send-money",
            path: "/send-money",
            icon: Send,
        },
        {
            label: "History",
            href: "/history",
            path: "/history",
            icon: History,
        },
        {
            label: "Ledger",
            href: "/ledger",
            path: "/ledger",
            icon: BookOpen,
        },
        {
            label: "Profile",
            href: "/profile",
            path: "/profile",
            icon: User,
        },
        {
            label: "Settings",
            href: "/settings",
            path: "/settings",
            icon: Settings,
        },
    ];

    return (
        <aside className="fixed left-0 top-0 flex h-screen w-[220px] flex-col bg-[#0B1633] px-5 py-5 text-white">
            {/* Logo */}
            <div className="mb-12 flex items-center gap-3">
                <Image
                    src="/images/p2p-wallet-logo.png"
                    alt="P2P Wallet"
                    width={36}
                    height={36}
                    className="shrink-0 rounded-xl"
                    priority
                />

                <span className="text-base font-semibold">
                    P2P Wallet
                </span>
            </div>

            {/* Navigation */}
            <nav className="flex-1">
                <ul className="flex h-[420px] flex-col justify-between">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const active = pathname === item.path;

                        return (
                            <li key={item.label}>
                                <Link
                                    href={item.href}
                                    className={`flex items-center gap-3 rounded-lg px-4 py-4 text-sm font-medium transition ${
                                        active
                                            ? "bg-[#4C3BDB] text-white"
                                            : "text-slate-300 hover:bg-[#17244A] hover:text-white"
                                    }`}
                                >
                                    <Icon
                                        size={19}
                                        className="shrink-0"
                                    />

                                    <span>{item.label}</span>
                                </Link>
                            </li>
                        );
                    })}
                </ul>
            </nav>

            {/* Logout */}
            <button
                onClick={handleLogout}
                className="flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-slate-300 transition hover:bg-[#17244A] hover:text-white"
            >
                <LogOut size={19} />
                <span>Logout</span>
            </button>
        </aside>
    );
}