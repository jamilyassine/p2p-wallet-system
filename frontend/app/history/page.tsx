"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import DashboardLayout from "../../components/layout/DashboardLayout";
import DashboardCard from "../../components/layout/DashboardCard";
import PageHeader from "../../components/layout/PageHeader";

import type { TransferRead } from "../../types/transfer";
import type { WalletResponse } from "../../types/wallet";

function HistoryContent() {
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const [wallet, setWallet] = useState<WalletResponse | null>(null);
    const [transfers, setTransfers] = useState<TransferRead[]>([]);

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

    return (
        <DashboardLayout>
            <PageHeader
                title="Transfer History"
                subtitle="View all your previous transfers."
            />

            <DashboardCard
                title="Transfer History"
                value={
                    transfers.length === 0 ? (
                        <p>No transfers found.</p>
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
                                        Counterparty
                                    </th>

                                    <th className="text-left border-b px-2 py-2 font-semibold">
                                        Amount
                                    </th>

                                    <th className="text-left border-b px-2 py-2 font-semibold">
                                        Status
                                    </th>

                                    <th className="text-left border-b px-2 py-2 font-semibold">
                                        Date
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                {transfers.map((transfer) => {
                                    const isOutgoing =
                                        transfer.sender_wallet_id === wallet?.id;

                                    const type = isOutgoing ? "To" : "From";

                                    const counterparty = isOutgoing
                                        ? `Wallet ${transfer.receiver_wallet_id}`
                                        : `Wallet ${transfer.sender_wallet_id}`;

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
                                                {Number(
                                                    transfer.amount
                                                ).toLocaleString(undefined, {
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
                    )
                }
            />
        </DashboardLayout>
    );
}

export default function HistoryPage() {
    return (
        <Suspense fallback={<div>Loading history...</div>}>
            <HistoryContent />
        </Suspense>
    );
}