"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";

export default function Sidebar() {

  const searchParams = useSearchParams();
  const userId = searchParams.get("userId");

  return (
    <aside className="w-64 border-r p-4">
      <h2>P2P Wallet</h2>

      <ul>
        <li>
            <Link href={`/dashboard?userId=${userId}`}>Dashboard</Link>
        </li>
        <li>
            <Link href="/login">Login</Link>
        </li>
        <li>
          <Link href={`/send-money?userId=${userId}`}>
            Send Money
          </Link>
        </li>
        <li>History</li>
        <li>Ledger</li>
        <li>Profile</li>
        <li>Settings</li>
      </ul>
    </aside>
  );
}