"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import DashboardCard from "../../components/layout/DashboardCard";
import DashboardLayout from "../../components/layout/DashboardLayout";
import PageHeader from "../../components/layout/PageHeader";

import type { UserResponse } from "../../types/user";
import type { WalletResponse } from "../../types/wallet";
import type { TransferRead } from "../../types/transfer";
import ActionCard from "../../components/layout/ActionCard";


function DashboardContent() {
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const [user, setUser] = useState<UserResponse | null>(null);
    const [wallet, setWallet] = useState<WalletResponse | null>(null);
    const [transfers, setTransfers] = useState<TransferRead[]>([]);

    const [users, setUsers] = useState<UserResponse[]>([]);

    useEffect(() => {
    fetch("http://localhost:8000/users")
        .then((response) => response.json())
        .then(setUsers);
    }, []);


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
            .then(setTransfers);
    }, [userId]);

    const recentTransactions =
    transfers.length === 0 ? (
        "No transactions yet"
    ) : (
        <table className="w-full border-collapse mt-2">
            <thead className="bg-gray-100">
                <tr>
                    <th className="text-left border-b px-2 py-2 font-semibold">
                        ID
                    </th>
                    <th className="text-left border-b px-2 py-2 font-semibold">
                        Type
                    </th>
                    <th className="text-left border-b px-2 py-2 font-semibold">
                        CounterParty
                    </th>
                    <th className="text-left border-b px-2 py-2 font-semibold">
                        Amount
                    </th>
                    <th className="text-left border-b px-2 py-2 font-semibold">
                        Status
                    </th>
                    <th className="text-left border-b px-2 py-2 font-semibold">
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
                            <td className="border-b px-2 py-2">
                                {transfer.id}
                            </td>

                            <td className="border-b px-2 py-2">
                                <span
                                    className={`inline-block rounded-full px-3 py-1 text-sm font-medium ${
                                        isOutgoing
                                            ? "bg-red-100 text-red-700"
                                            : "bg-green-100 text-green-700"
                                    }`}
                                >
                                    {type}
                                </span>
                            </td>

                            <td className="border-b px-2 py-2">
                                {counterparty}
                            </td>

                            <td className="border-b px-2 py-2">
                                $
                                {Number(transfer.amount).toLocaleString(undefined, {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2,
                                })}
                            </td>

                            <td className="border-b px-2 py-2">
                                <span
                                    className={`inline-block rounded-full px-3 py-1 text-sm font-medium ${
                                        transfer.status === "SUCCESS"
                                            ? "bg-green-100 text-green-700"
                                            : "bg-red-100 text-red-700"
                                    }`}
                                >
                                    {transfer.status}
                                </span>
                            </td>

                            <td className="border-b px-2 py-2">
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
        <DashboardLayout>
            <PageHeader
                title="Dashboard"
                subtitle={
                    user
                        ? `Welcome, ${user.name}!`
                        : "Loading..."
                }
            />

            <div className="mb-6">
                <DashboardCard
                    title="Total Balance"
                    value={
                        wallet ? (
                            <div className="text-3xl font-bold">
                                $
                                {Number(wallet.balance).toLocaleString(undefined, {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                                })}
                            </div>
                            ) : (
                            "Loading..."
                        )
                    }
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">

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

            
        </DashboardLayout>
    );
}

export default function DashboardPage() {
    return (
        <Suspense fallback={<div>Loading dashboard...</div>}>
            <DashboardContent />
        </Suspense>
    );
}










