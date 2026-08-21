"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";

export default function Sidebar() {
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const dashboardHref = userId
        ? `/dashboard?userId=${userId}`
        : "/dashboard";

    const sendMoneyHref = userId
        ? `/send-money?userId=${userId}`
        : "/send-money";

    const ledgerHref = userId
        ? `/ledger?userId=${userId}`
        : "/ledger";

    const historyHref = userId
        ? `/history?userId=${userId}`
        : "/history";

    const linkClass = (path: string) =>
        `block rounded-lg px-4 py-3 ${
            pathname === path
                ? "bg-purple-600 font-medium"
                : "hover:bg-slate-800"
        }`;

    return (
        <aside className="w-60 min-h-screen bg-slate-900 text-white p-5">
            <h2 className="text-xl font-bold mb-8">
                P2P Wallet
            </h2>

            <nav>
                <ul className="space-y-2">
                    <li>
                        <Link
                            href={dashboardHref}
                            className={linkClass("/dashboard")}
                        >
                            Dashboard
                        </Link>
                    </li>

                    <li>
                        <Link
                            href="/login"
                            className={linkClass("/login")}
                        >
                            Login
                        </Link>
                    </li>

                    <li>
                        <Link
                            href={sendMoneyHref}
                            className={linkClass("/send-money")}
                        >
                            Send Money
                        </Link>
                    </li>

                    <li>
                        <Link
                            href={historyHref}
                            className={linkClass("/history")}
                        >
                            History
                        </Link>
                    </li>

                    <li>
                        <Link
                            href={ledgerHref}
                            className={linkClass("/ledger")}
                        >
                            Ledger
                        </Link>
                    </li>

                    <li className="px-4 py-3">
                        Profile
                    </li>

                    <li className="px-4 py-3">
                        Settings
                    </li>
                </ul>
            </nav>
        </aside>
    );
}