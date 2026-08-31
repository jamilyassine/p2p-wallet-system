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

    const recentTransactions =
        transfers.length === 0 ? (
            <p className="py-4 text-sm text-slate-500">
                No transactions yet
            </p>
        ) : (
            <table className="w-full border-collapse">
                <thead className="bg-slate-50">
                    <tr>
                        <th className="border-b px-3 py-2 text-left text-sm font-semibold">
                            ID
                        </th>
                        <th className="border-b px-3 py-2 text-left text-sm font-semibold">
                            Type
                        </th>
                        <th className="border-b px-3 py-2 text-left text-sm font-semibold">
                            CounterParty
                        </th>
                        <th className="border-b px-3 py-2 text-left text-sm font-semibold">
                            Amount
                        </th>
                        <th className="border-b px-3 py-2 text-left text-sm font-semibold">
                            Status
                        </th>
                        <th className="border-b px-3 py-2 text-left text-sm font-semibold">
                            Time
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {transfers.map((transfer) => {
                        const isOutgoing =
                            transfer.sender_wallet_id === wallet?.id;

                        const type = isOutgoing ? "To" : "From";

                        const counterparty = isOutgoing
                            ? transfer.receiver_name
                            : transfer.sender_name;

                        return (
                            <tr key={transfer.id}>
                                <td className="border-b px-3 py-2 text-sm">
                                    {transfer.id}
                                </td>

                                <td className="border-b px-3 py-2 text-sm">
                                    <span
                                        className={`inline-block rounded-full px-2.5 py-1 text-xs font-medium ${
                                            isOutgoing
                                                ? "bg-red-100 text-red-700"
                                                : "bg-green-100 text-green-700"
                                        }`}
                                    >
                                        {type}
                                    </span>
                                </td>

                                <td className="border-b px-3 py-2 text-sm">
                                    {counterparty}
                                </td>

                                <td className="border-b px-3 py-2 text-sm">
                                    $
                                    {Number(transfer.amount).toLocaleString(
                                        undefined,
                                        {
                                            minimumFractionDigits: 2,
                                            maximumFractionDigits: 2,
                                        }
                                    )}
                                </td>

                                <td className="border-b px-3 py-2 text-sm">
                                    <span
                                        className={`inline-block rounded-full px-2.5 py-1 text-xs font-medium ${
                                            transfer.status === "SUCCESS"
                                                ? "bg-green-100 text-green-700"
                                                : "bg-red-100 text-red-700"
                                        }`}
                                    >
                                        {transfer.status}
                                    </span>
                                </td>

                                <td className="border-b px-3 py-2 text-sm">
                                    {new Date(
                                        transfer.created_at
                                    ).toLocaleDateString("en-GB", {
                                        day: "2-digit",
                                        month: "short",
                                        year: "numeric",
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    })}
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
                title="Dashboard"
                subtitle={
                    user
                        ? `Welcome, ${user.name}!`
                        : "Loading..."
                }
            />

            <div className="mb-5">
                <DashboardCard
                    title="Total Balance"
                    value={
                        wallet ? (
                            <div className="text-3xl font-bold">
                                $
                                {Number(wallet.balance).toLocaleString(
                                    undefined,
                                    {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2,
                                    }
                                )}
                            </div>
                        ) : (
                            "Loading..."
                        )
                    }
                />
            </div>

            <div className="mb-5 grid grid-cols-1 gap-5 md:grid-cols-2">
                <ActionCard
                    title="Send Money"
                    description="Transfer money to another wallet"
                    href={`/send-money?userId=${userId}`}
                />

                <ActionCard
                    title="Transfer History"
                    description="View your previous transfers"
                    href={`/history?userId=${userId}`}
                />
            </div>

            <DashboardCard
                title="Recent Transactions"
                value={recentTransactions}
            />
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










