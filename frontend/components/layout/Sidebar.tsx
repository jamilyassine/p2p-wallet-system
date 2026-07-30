"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";

export default function Sidebar() {
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

    return (
        <aside className="w-64 border-r p-4">
            <h2>P2P Wallet</h2>

            <nav>
                <ul>
                    <li>
                        <Link href={dashboardHref}>
                            Dashboard
                        </Link>
                    </li>

                    <li>
                        <Link href="/login">
                            Login
                        </Link>
                    </li>

                    <li>
                        <Link href={sendMoneyHref}>
                            Send Money
                        </Link>
                    </li>

                    <li>History</li>
                    <li>
                        <Link href={ledgerHref}>
                            Ledger
                        </Link>
                    </li>
                    <li>Profile</li>
                    <li>Settings</li>
                </ul>
            </nav>
        </aside>
    );
}