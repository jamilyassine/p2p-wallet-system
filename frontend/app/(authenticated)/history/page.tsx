"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import DashboardCard from "../../../components/layout/DashboardCard";
import PageHeader from "../../../components/layout/PageHeader";

import type { TransferRead } from "../../../types/transfer";
import type { WalletResponse } from "../../../types/wallet";

function HistoryContent() {
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const [wallet, setWallet] = useState<WalletResponse | null>(null);
    const [transfers, setTransfers] = useState<TransferRead[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [total, setTotal] = useState(0);

    const [search, setSearch] = useState("");
    const [status, setStatus] = useState("");
    const [sort, setSort] = useState("");
    const [showFilters, setShowFilters] = useState(false);

    const pageSize = 7;
    const totalPages = Math.ceil(total / pageSize);

    const activeFilterCount =
        (status !== "" ? 1 : 0) + (sort !== "" ? 1 : 0);
    
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        if (!userId) return;

        fetch(`http://localhost:8000/wallets/user/${userId}`)
            .then((response) => response.json())
            .then(setWallet)
            .catch(() => {
                setError(true);
            });

    }, [userId]);

    useEffect(() => {
        if (!userId) return;

        const params = new URLSearchParams({
            page: String(currentPage),
            limit: String(pageSize),
        });

        if (search) params.set("search", search);
        if (status) params.set("status", status);
        if (sort) params.set("sort", sort);

        fetch(
            `http://localhost:8000/transfers/user/${userId}?${params.toString()}`
        )
            .then((response) => response.json())
            .then((data) => {
                setTransfers(data.transactions);
                setTotal(data.total);
            })
            .catch(() => {
                setError(true);
            })
            .finally(() => {
                setLoading(false);
            });
    }, [userId, currentPage, search, status, sort]);

    return (
        <>
            <div className="w-full max-w-8xl mx-auto">
                <PageHeader
                    title="Transfer History"
                    subtitle="View all your previous transfers."
                />

                <div className="-mt-10 mb-4 flex justify-end">
                    <button
                        onClick={() => setShowFilters(!showFilters)}
                        className="inline-flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm hover:bg-gray-50"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            className="h-4 w-4"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="M3 5h18M6 12h12m-8 7h4"
                            />
                        </svg>

                        Filters

                        {activeFilterCount > 0 && (
                            <span className="ml-2 inline-flex items-center justify-center rounded-full bg-blue-600 px-2 py-0.5 text-xs text-white">
                                {activeFilterCount}
                            </span>
                        )}
                    </button>
                </div>
            </div>

            {showFilters && (
                <div className="mb-5 rounded-lg border border-gray-200 bg-gray-50 p-4">
                    <input
                        type="text"
                        placeholder="Search transactions..."
                        value={search}
                        onChange={(event) => {
                            setSearch(event.target.value);
                            setCurrentPage(1);
                        }}
                        className="mb-4 w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <div className="flex items-center gap-8">
                        <div className="flex items-center gap-2">
                            <label className="font-medium">Status:</label>

                            <select
                                value={status}
                                onChange={(event) => {
                                    setStatus(event.target.value);
                                    setCurrentPage(1);
                                }}
                                className="rounded-lg border border-gray-300 bg-white px-3 py-2"
                            >
                                <option value="">All</option>
                                <option value="SUCCESS">Success</option>
                                <option value="FAILED">Failed</option>
                            </select>
                        </div>

                        <div className="flex items-center gap-2">
                            <label className="font-medium">Sort:</label>

                            <select
                                value={sort}
                                onChange={(event) => {
                                    setSort(event.target.value);
                                    setCurrentPage(1);
                                }}
                                className="rounded-lg border border-gray-300 bg-white px-3 py-2"
                            >
                                <option value="">Date</option>
                                <option value="amount">Amount</option>
                            </select>
                        </div>
                    </div>
                </div>
            )}

            <div className="w-full max-w-8xl mx-auto">
                <DashboardCard
                    title="Transfer History"
                    value={
                        loading ? (
                            <p className="p-5 text-sm text-slate-500">
                                Loading transactions...
                            </p>
                        ) : error ? (
                            <p className="p-5 text-sm text-red-500">
                                Failed to load transactions.
                            </p>
                        ) : transfers.length === 0 ? (
                            <p className="p-5 text-sm text-slate-500">
                                No transfers found.
                            </p>
                        ) : (
                            <table className="w-full border-collapse text-sm">
                                <thead className="bg-gray-100 text-gray-600">
                                    <tr>
                                        <th className="w-[8%] border-b px-4 py-3 text-left font-semibold">
                                            ID
                                        </th>
                                        <th className="w-[12%] border-b px-4 py-3 text-left font-semibold">
                                            Type
                                        </th>
                                        <th className="w-[22%] border-b px-4 py-3 text-left font-semibold">
                                            Counterparty
                                        </th>
                                        <th className="w-[15%] border-b px-4 py-3 text-left font-semibold">
                                            Amount
                                        </th>
                                        <th className="w-[15%] border-b px-4 py-3 text-left font-semibold">
                                            Status
                                        </th>
                                        <th className="w-[28%] border-b px-4 py-3 text-left font-semibold">
                                            Date
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {transfers.map((transfer) => {
                                        const isOutgoing =
                                            transfer.sender_wallet_id ===
                                            wallet?.id;

                                        const type = isOutgoing
                                            ? "To"
                                            : "From";

                                        const counterparty = isOutgoing
                                            ? transfer.receiver_name
                                            : transfer.sender_name;

                                        return (
                                            <tr key={transfer.id}>
                                                <td className="border-b border-gray-100 px-3 py-3">
                                                    {transfer.id}
                                                </td>

                                                <td className="border-b border-gray-100 px-3 py-3">
                                                    {type}
                                                </td>

                                                <td className="border-b border-gray-100 px-3 py-3">
                                                    {counterparty}
                                                </td>

                                                <td className="border-b border-gray-100 px-3 py-3 font-semibold">
                                                    $
                                                    {Number(
                                                        transfer.amount
                                                    ).toLocaleString(
                                                        undefined,
                                                        {
                                                            minimumFractionDigits: 2,
                                                            maximumFractionDigits: 2,
                                                        }
                                                    )}
                                                </td>

                                                <td className="border-b border-gray-100 px-3 py-3">
                                                    <span
                                                        className={`inline-block rounded-md px-3 py-1 text-xs font-semibold ${
                                                            transfer.status ===
                                                            "SUCCESS"
                                                                ? "bg-green-100 text-green-700"
                                                                : "bg-red-100 text-red-700"
                                                        }`}
                                                    >
                                                        {transfer.status}
                                                    </span>
                                                </td>

                                                <td className="border-b border-gray-100 px-3 py-3">
                                                    {new Date(
                                                        transfer.created_at
                                                    ).toLocaleDateString(
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
                        )
                    }
                />

                <div className="mt-4 flex items-center justify-center gap-2">
                    <button
                        onClick={() =>
                            setCurrentPage(currentPage - 1)
                        }
                        disabled={currentPage === 1}
                        className="flex h-8 w-8 items-center justify-center rounded-md border border-gray-200 bg-white text-sm font-semibold text-slate-700 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                        ‹
                    </button>

                    {Array.from(
                        { length: totalPages },
                        (_, index) => index + 1
                    ).map((page) => (
                        <button
                            key={page}
                            onClick={() => setCurrentPage(page)}
                            className={`flex h-8 w-8 items-center justify-center rounded-md text-sm font-semibold ${
                                currentPage === page
                                    ? "bg-purple-600 text-white"
                                    : "border border-gray-200 bg-white text-slate-700 hover:bg-gray-100"
                            }`}
                        >
                            {page}
                        </button>
                    ))}

                    <button
                        onClick={() =>
                            setCurrentPage(currentPage + 1)
                        }
                        disabled={currentPage === totalPages}
                        className="flex h-8 w-8 items-center justify-center rounded-md border border-gray-200 bg-white text-sm font-semibold text-slate-700 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                        ›
                    </button>
                </div>
            </div>
        </>
    );
}

export default function HistoryPage() {
    return (
        <Suspense fallback={<div>Loading history...</div>}>
            <HistoryContent />
        </Suspense>
    );
}