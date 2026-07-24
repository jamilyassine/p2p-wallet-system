"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import DashboardCard from "../../components/layout/DashboardCard";
import DashboardLayout from "../../components/layout/DashboardLayout";
import PageHeader from "../../components/layout/PageHeader";

import type { UserResponse } from "../../types/user";
import type { WalletResponse } from "../../types/wallet";
import type { TransferRead } from "../../types/transfer";

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
            .then(setTransfers);
    }, [userId]);

    const recentTransactions =
        transfers.length === 0 ? (
            "No transactions yet"
        ) : (
            transfers.map((transfer) => (
                <div key={transfer.id}>
                    ${transfer.amount} - {transfer.status}
                </div>
            ))
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

            <DashboardCard
                title="Total Balance"
                value={
                    wallet
                        ? `$${wallet.balance}`
                        : "Loading..."
                }
            />

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










