"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import DashboardCard from "../../../components/layout/DashboardCard";
import PageHeader from "../../../components/layout/PageHeader";
import ActionCard from "../../../components/layout/ActionCard";

import type { UserResponse } from "../../../types/user";
import type { WalletResponse } from "../../../types/wallet";
import type { TransferRead } from "../../../types/transfer";

function DashboardContent() {
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const [user, setUser] = useState<UserResponse | null>(null);
    const [wallet, setWallet] = useState<WalletResponse | null>(null);
    const [transfers, setTransfers] = useState<TransferRead[]>([]);

    useEffect(() => {
        if (!userId) return;

        fetch(`http://localhost:8000/users/${userId}`)
            .then((response) => response.json())
            .then(setUser);
    }, [userId]);

    useEffect(() => {
        if (!userId) return;

        fetch(`http://localhost:8000/wallets/user/${userId}`)
            .then((response) => response.json())
            .then(setWallet);
    }, [userId]);

    useEffect(() => {
        if (!userId) return;

        fetch(`http://localhost:8000/transfers/user/${userId}`)
            .then((response) => response.json())
            .then((data) => setTransfers(data.transactions));
    }, [userId]);

    const recentTransfers = transfers.slice(0, 3);

    const recentTransactions =
        transfers.length === 0 ? (
            <p className="py-4 text-sm text-slate-500">
                No transactions yet
            </p>
        ) : (
            <table className="w-full border-collapse">

                        <tbody>
    {recentTransfers.map((transfer) => {
        const isOutgoing =
            transfer.sender_wallet_id === wallet?.id;

        const counterparty = isOutgoing
            ? transfer.receiver_name
            : transfer.sender_name;
        const type = isOutgoing ? "To" : "From";

        return (
            <tr key={transfer.id}>
                {/* Avatar + Counterparty */}
                <td className="border-b border-slate-100 px-3 py-3">
                    <div className="flex items-center gap-3">
                        <div
    className={`flex h-9 w-9 items-center justify-center rounded-full ${
        isOutgoing
            ? "bg-red-50 text-red-500"
            : "bg-slate-100 text-slate-500"
    }`}
>
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="currentColor"
                                className="h-5 w-5"
                            >
                                <path
                                    fillRule="evenodd"
                                    d="M12 2a5 5 0 1 0 0 10 5 5 0 0 0 0-10ZM4 21a8 8 0 1 1 16 0H4Z"
                                    clipRule="evenodd"
                                />
                            </svg>
                        </div>

                        <span className="text-sm font-semibold text-slate-700">
                            {type} {counterparty}
                        </span>
                    </div>
                </td>

                {/* Amount */}
                <td className="border-b border-slate-100 px-3 py-3 text-sm font-semibold text-slate-700">
                    $
                    {Number(transfer.amount).toLocaleString("en-US", {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                    })}
                </td>

                {/* Status */}
                <td className="border-b border-slate-100 px-3 py-3">
                    <span
                        className={`inline-block rounded-full px-2.5 py-1 text-xs font-semibold ${
                            transfer.status === "SUCCESS"
                                ? "bg-green-100 text-green-700"
                                : "bg-red-100 text-red-700"
                        }`}
                    >
                        {transfer.status}
                    </span>
                </td>

                {/* Date */}
                <td className="border-b border-slate-100 px-3 py-3 text-sm text-slate-500">
                    {new Date(transfer.created_at).toLocaleDateString(
                        "en-GB",
                        {
                            day: "2-digit",
                            month: "short",
                            year: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                        }
                    )}
                </td>
            </tr>
        );
    })}
</tbody>

               
            </table>
        );

    return (
        <>
            <PageHeader
                title={user ? `Welcome back, ${user.name}!` : "Welcome back!"}
                subtitle="Here’s what’s happening with your wallet today."
                userName={user?.name}
                userEmail={user?.email}
            />

            <div className="mb-6">
                <DashboardCard
                    title="Total Balance"
                    value={
    wallet ? (
        <div className="relative flex min-h-[155px] items-center">
            <div>
                <div className="flex items-center gap-2">
                    <span className="text-4xl font-bold text-slate-900">
                        $
                        {Number(wallet.balance).toLocaleString("en-US", {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                        })}
                    </span>

                    <span className="rounded-md bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600">
                        USD
                    </span>
                </div>

                <p className="mt-4 text-xs text-slate-600">
                    Available Balance
                </p>

                <p className="mt-1 text-sm font-semibold text-green-600">
                    $
                    {Number(wallet.balance).toLocaleString("en-US", {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                    })}
                </p>
            </div>

            <img
    src="/images/wallet.png"
    alt="Wallet"
    className="absolute right-1/4 top-[45%] h-52 w-64 -translate-y-1/2 object-contain"
/>
        </div>
    ) : (
        "Loading..."
    )
}
                />
            </div>

            <div className="mb-6 grid grid-cols-1 gap-6 md:grid-cols-2">
                <ActionCard
                    title="Send Money"
                    description="Transfer money to another wallet"
                    href={`/send-money?userId=${userId}`}
                    icon="send"
                />

                <ActionCard
                    title="Transfer History"
                    description="View your previous transfers"
                    href={`/history?userId=${userId}`}
                    icon="clock"
                />
            </div>

        <div className="mb-6">
    <div className="flex items-start justify-between">
        <h2 className="text-base font-bold text-slate-800">
            Recent Transactions
        </h2>

        <a
            href={`/history?userId=${userId}`}
            className="text-sm font-semibold text-indigo-600 hover:text-indigo-700"
        >
            View all
        </a>
    </div>

    <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
        {recentTransactions}
    </div>
</div>
        </>
    );
}

export default function DashboardPage() {
    return (
        <Suspense fallback={<div>Loading dashboard...</div>}>
            <DashboardContent />
        </Suspense>
    );
}










