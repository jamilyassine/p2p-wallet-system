"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import DashboardCard from "../../components/layout/DashboardCard";
import DashboardLayout from "../../components/layout/DashboardLayout";
import PageHeader from "../../components/layout/PageHeader";
import { getWalletLedger } from "../../services/ledger";

import type { UserResponse } from "../../types/user";
import type { WalletResponse } from "../../types/wallet";
import type { TransferRead } from "../../types/transfer";
import type { LedgerEntry } from "../../types/ledger";


function DashboardContent() {
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const [user, setUser] = useState<UserResponse | null>(null);
    const [wallet, setWallet] = useState<WalletResponse | null>(null);
    const [transfers, setTransfers] = useState<TransferRead[]>([]);

    const [ledgerEntries, setLedgerEntries] = useState<LedgerEntry[]>([]);

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
        if (!wallet) return;

        const walletId = wallet.id;

        async function fetchLedger() {
            const entries = await getWalletLedger(walletId);
            setLedgerEntries(entries);
        }

        fetchLedger();
    }, [wallet]);

    

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
                        Sender
                    </th>
                    <th className="text-left border-b px-2 py-2 font-semibold">
                        Receiver
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
                {transfers.map((transfer) => (
                    <tr key={transfer.id}>
                        <td className="border-b px-2 py-2">
                            {transfer.id}
                        </td>

                        <td className="border-b px-2 py-2">
                            Wallet {transfer.sender_wallet_id}
                        </td>

                        <td className="border-b px-2 py-2">
                            Wallet {transfer.receiver_wallet_id}
                        </td>

                        <td className="border-b px-2 py-2">
                            ${transfer.amount}
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
                            {new Date(transfer.created_at).toLocaleDateString("en-GB", {
                                day: "2-digit",
                                month: "short",
                                year: "numeric",
                                hour: "2-digit",
                                minute: "2-digit",
                            })}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );

    const totalDebits = ledgerEntries
    .filter((entry) => entry.entry_type === "DEBIT")
    .reduce((sum, entry) => sum + Number(entry.amount), 0);

    const totalCredits = ledgerEntries
    .filter((entry) => entry.entry_type === "CREDIT")
    .reduce((sum, entry) => sum + Number(entry.amount), 0);

    const ledgerEntryCount = ledgerEntries.length;


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

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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

                <DashboardCard
                title="Ledger Summary"
                value={
                    <>
                    <div>Total Debits: ${totalDebits}</div>
                    <div>Total Credits: ${totalCredits}</div>
                    <div>Ledger Entries: {ledgerEntryCount}</div>
                    </>
                }
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










