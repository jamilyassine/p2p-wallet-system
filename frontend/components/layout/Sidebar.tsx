"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import {
    LayoutDashboard,
    Send,
    History,
    BookOpen,
    User,
    Settings,
    LogOut,
    WalletCards,
} from "lucide-react";

export default function Sidebar() {
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const withUserId = (path: string) =>
        userId ? `${path}?userId=${userId}` : path;

    const navItems = [
        {
            label: "Dashboard",
            href: withUserId("/dashboard"),
            path: "/dashboard",
            icon: LayoutDashboard,
        },
        {
            label: "Send Money",
            href: withUserId("/send-money"),
            path: "/send-money",
            icon: Send,
        },
        {
            label: "History",
            href: withUserId("/history"),
            path: "/history",
            icon: History,
        },
        {
            label: "Ledger",
            href: withUserId("/ledger"),
            path: "/ledger",
            icon: BookOpen,
        },
        {
            label: "Profile",
            href: withUserId("/profile"),
            path: "/profile",
            icon: User,
        },
        {
            label: "Settings",
            href: withUserId("/settings"),
            path: "/settings",
            icon: Settings,
        },
    ];

    return (
        <aside className="fixed left-0 top-0 flex h-screen w-[220px] flex-col bg-[#0B1633] px-5 py-5 text-white">

            {/* Logo */}
            <div className="mb-12 flex items-center gap-3">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#4C3BDB]">
                    <WalletCards size={20} />
                </div>

                <span className="text-base font-semibold">
                    P2P Wallet
                </span>
            </div>

            {/* Navigation */}
            <nav className="flex-1">
                <ul className="flex flex-col justify-between h-[420px]">
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
                className="flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-slate-300 transition hover:bg-[#17244A] hover:text-white"
            >
                <LogOut size={19} />
                <span>Logout</span>
            </button>
        </aside>
    );
}