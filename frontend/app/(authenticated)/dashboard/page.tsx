"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
    ArrowRight,
    Clock,
    Send,
    UserRound,
} from "lucide-react";

import DashboardCard from "../../../components/layout/DashboardCard";
import PageHeader from "../../../components/layout/PageHeader";
import { apiFetch } from "../../../lib/api";

import type { UserResponse } from "../../../types/user";
import type { WalletResponse } from "../../../types/wallet";
import type { TransferRead } from "../../../types/transfer";

function DashboardContent() {
    const [user, setUser] = useState<UserResponse | null>(null);
    const [wallet, setWallet] = useState<WalletResponse | null>(null);
    const [transfers, setTransfers] = useState<TransferRead[]>([]);

    useEffect(() => {
        async function fetchUser() {
            try {
                const response = await apiFetch("/users/me");

                if (!response) return;

                const data = await response.json();
                setUser(data);
            } catch (error) {
                console.error(error);
            }
        }

        fetchUser();
    }, []);

    useEffect(() => {
        if (!user) return;

        const userId = user.id;

        async function fetchWallet() {
            try {
                const response = await apiFetch(
                    `/wallets/user/${userId}`
                );

                if (!response) return;

                const data = await response.json();
                setWallet(data);
            } catch (error) {
                console.error(error);
            }
        }

        fetchWallet();
    }, [user]);

    useEffect(() => {
        if (!user) return;

        const userId = user.id;

        async function fetchTransfers() {
            try {
                const response = await apiFetch(
                    `/transfers/user/${userId}`
                );

                if (!response) return;

                const data = await response.json();
                setTransfers(data.transactions ?? []);
            } catch (error) {
                console.error(error);
            }
        }

        fetchTransfers();
    }, [user]);

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
                                <td className="border-b border-slate-100 px-3 py-3">
                                    <div className="flex items-center gap-3">
                                        <div
                                            className={`flex h-9 w-9 items-center justify-center rounded-full ${
                                                isOutgoing
                                                    ? "bg-red-50 text-red-500"
                                                    : "bg-slate-100 text-slate-500"
                                            }`}
                                        >
                                            <UserRound size={18} />
                                        </div>

                                        <span className="text-sm font-semibold text-slate-700">
                                            {type} {counterparty}
                                        </span>
                                    </div>
                                </td>

                                <td className="border-b border-slate-100 px-3 py-3 text-sm font-semibold text-slate-700">
                                    $
                                    {Number(
                                        transfer.amount
                                    ).toLocaleString("en-US", {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2,
                                    })}
                                </td>

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

                                <td className="border-b border-slate-100 px-3 py-3 text-sm text-slate-500">
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
                title={user ? `Welcome back, ${user.name}!` : "Welcome back!"}
                subtitle="Here’s what’s happening with your wallet today."
                userName={user?.name}
                userEmail={user?.email}
            />

            {/* Balance */}
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
                                            {Number(
                                                wallet.balance
                                            ).toLocaleString("en-US", {
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
                                        {Number(
                                            wallet.balance
                                        ).toLocaleString("en-US", {
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

            {/* Action cards */}
            <div className="mb-6 grid grid-cols-1 gap-6 md:grid-cols-2">
                <Link
                    href="/send-money"
                    className="group flex min-h-[120px] items-center justify-between rounded-xl border border-gray-200 bg-white px-6 py-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
                >
                    <div className="flex items-center gap-5">
                        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-purple-50 text-purple-600">
                            <Send size={30} />
                        </div>

                        <div>
                            <h2 className="text-lg font-semibold text-slate-800">
                                Send Money
                            </h2>

                            <p className="mt-1 text-sm text-slate-500">
                                Transfer money to another wallet
                            </p>
                        </div>
                    </div>

                    <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-purple-600 text-white transition group-hover:bg-purple-700">
                        <ArrowRight size={20} />
                    </div>
                </Link>

                <Link
                    href="/history"
                    className="group flex min-h-[120px] items-center justify-between rounded-xl border border-gray-200 bg-white px-6 py-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
                >
                    <div className="flex items-center gap-5">
                        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-purple-50 text-purple-600">
                            <Clock size={30} />
                        </div>

                        <div>
                            <h2 className="text-lg font-semibold text-slate-800">
                                Transfer History
                            </h2>

                            <p className="mt-1 text-sm text-slate-500">
                                View your previous transfers
                            </p>
                        </div>
                    </div>

                    <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-purple-600 text-white transition group-hover:bg-purple-700">
                        <ArrowRight size={20} />
                    </div>
                </Link>
            </div>

            {/* Recent transactions */}
            <div className="mb-6">
                <div className="flex items-start justify-between">
                    <h2 className="text-base font-bold text-slate-800">
                        Recent Transactions
                    </h2>

                    <Link
                        href="/history"
                        className="text-sm font-semibold text-indigo-600 hover:text-indigo-700"
                    >
                        View all
                    </Link>
                </div>

                <div className="mt-2 overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
                    {recentTransactions}
                </div>
            </div>
        </>
    );
}

export default function DashboardPage() {
    return <DashboardContent />;
}