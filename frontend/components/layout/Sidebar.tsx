import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-64 border-r p-4">
      <h2>P2P Wallet</h2>

      <ul>
        <li>
            <Link href="/dashboard">Dashboard</Link>
        </li>
        <li>
            <Link href="/login">Login</Link>
        </li>
        <li>History</li>
        <li>Ledger</li>
        <li>Profile</li>
        <li>Settings</li>
      </ul>
    </aside>
  );
}