"use client";

import { useEffect, useState } from "react";
import { Filter } from "lucide-react";

import PageHeader from "../../../components/layout/PageHeader";

import type { LedgerEntry } from "@/types/ledger";
import type { UserResponse } from "@/types/user";

import { apiFetch } from "@/lib/api";

export default function LedgerPage() {
    const [user, setUser] = useState<UserResponse | null>(null);

    const [entries, setEntries] = useState<LedgerEntry[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [total, setTotal] = useState(0);

    const [entryType, setEntryType] = useState("");
    const [showFilters, setShowFilters] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    const pageSize = 7;
    const totalPages = Math.ceil(total / pageSize);

    const activeFilterCount = entryType !== "" ? 1 : 0;

    useEffect(() => {
        async function fetchUser() {
            try {
                const response = await apiFetch("/users/me");

                if (!response) return;

                const data = await response.json();
                setUser(data);
            } catch (error) {
                console.error(error);
                setError(true);
                setLoading(false);
            }
        }

        fetchUser();
    }, []);

    useEffect(() => {
        async function fetchLedger() {
            try {
                setLoading(true);
                setError(false);

                const params = new URLSearchParams({
                    page: String(currentPage),
                    limit: String(pageSize),
                });

                if (entryType) {
                    params.set("entry_type", entryType);
                }

                const response = await apiFetch(
                    `/ledger/recent?${params.toString()}`
                );

                if (!response) return;

                const data = await response.json();

                setEntries(data.transactions ?? []);
                setTotal(data.total ?? 0);
            } catch (error) {
                console.error(error);
                setError(true);
            } finally {
                setLoading(false);
            }
        }

        fetchLedger();
    }, [currentPage, entryType]);

    function handleFilterChange(value: string) {
        setEntryType(value);
        setCurrentPage(1);
    }

    return (
        <div className="w-full">
            {/* Page Header */}
            <PageHeader
                title="Ledger Entries"
                subtitle="Dashboard  ›  Ledger"
                userName={user?.name}
                userEmail={user?.email}
            />

            {/* Filters */}
            <div className="mb-5 flex justify-end">
                <button
                    onClick={() => setShowFilters((show) => !show)}
                    className="inline-flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm hover:bg-gray-50"
                >
                    <Filter size={16} />
                    Filters

                    {activeFilterCount > 0 && (
                        <span className="ml-1 inline-flex items-center justify-center rounded-full bg-blue-600 px-2 py-0.5 text-xs text-white">
                            {activeFilterCount}
                        </span>
                    )}
                </button>
            </div>

            {/* Filter Panel */}
            {showFilters && (
                <div className="mb-5 rounded-lg border border-gray-200 bg-gray-50 p-4">
                    <div className="flex items-center gap-8">
                        <div className="flex items-center gap-2">
                            <label className="font-medium">
                                Type:
                            </label>

                            <select
                                value={entryType}
                                onChange={(event) =>
                                    handleFilterChange(event.target.value)
                                }
                                className="rounded-lg border border-gray-300 bg-white px-3 py-2"
                            >
                                <option value="">All</option>
                                <option value="DEBIT">Debit</option>
                                <option value="CREDIT">Credit</option>
                            </select>
                        </div>
                    </div>
                </div>
            )}

            {/* Ledger Table */}
            {loading ? (
                <p className="py-6 text-sm text-slate-500">
                    Loading ledger entries...
                </p>
            ) : error ? (
                <p className="py-6 text-sm text-red-500">
                    Failed to load ledger entries.
                </p>
            ) : entries.length === 0 ? (
                <p className="py-6 text-sm text-slate-500">
                    No ledger entries found.
                </p>
            ) : (
                <div className="overflow-hidden rounded-xl bg-white shadow-sm">
                    <div className="overflow-x-auto">
                        <table className="w-full border-collapse text-sm">
                            <thead className="bg-gray-100 text-gray-600">
                                <tr>
                                    <th className="w-[8%] border-b border-gray-200 px-4 py-3 text-left font-semibold">
                                        ID
                                    </th>

                                    <th className="w-[15%] border-b border-gray-200 px-4 py-3 text-left font-semibold">
                                        Transfer ID
                                    </th>

                                    <th className="w-[22%] border-b border-gray-200 px-4 py-3 text-left font-semibold">
                                        Wallet
                                    </th>

                                    <th className="w-[15%] border-b border-gray-200 px-4 py-3 text-left font-semibold">
                                        Type
                                    </th>

                                    <th className="w-[15%] border-b border-gray-200 px-4 py-3 text-left font-semibold">
                                        Amount
                                    </th>

                                    <th className="w-[25%] border-b border-gray-200 px-4 py-3 text-left font-semibold">
                                        Date
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                {entries.map((entry, index) => (
                                    <tr
                                        key={`${entry.transfer_id}-${entry.wallet_id}-${entry.entry_type}`}
                                        className="hover:bg-gray-50"
                                    >
                                        <td className="border-b border-gray-100 px-3 py-3">
                                            #
                                            {(currentPage - 1) *
                                                pageSize +
                                                index +
                                                1}
                                        </td>

                                        <td className="border-b border-gray-100 px-3 py-3">
                                            <span className="font-medium text-blue-600">
                                                #{entry.transfer_id}
                                            </span>
                                        </td>

                                        <td className="border-b border-gray-100 px-3 py-3">
                                            {entry.wallet_user_name}
                                        </td>

                                        <td
                                            className={`border-b border-gray-100 px-3 py-3 font-medium ${
                                                entry.entry_type === "DEBIT"
                                                    ? "text-blue-600"
                                                    : "text-green-600"
                                            }`}
                                        >
                                            {entry.entry_type}
                                        </td>

                                        <td
                                            className={`border-b border-gray-100 px-3 py-3 font-semibold ${
                                                entry.entry_type === "DEBIT"
                                                    ? "text-red-600"
                                                    : "text-green-600"
                                            }`}
                                        >
                                            {entry.entry_type === "DEBIT"
                                                ? "-"
                                                : "+"}
                                            $
                                            {Number(
                                                entry.amount
                                            ).toLocaleString(undefined, {
                                                minimumFractionDigits: 2,
                                                maximumFractionDigits: 2,
                                            })}
                                        </td>

                                        <td className="border-b border-gray-100 px-3 py-3">
                                            {new Date(
                                                entry.created_at
                                            ).toLocaleDateString("en-GB", {
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
                    </div>
                </div>
            )}

            {/* Pagination */}
            {totalPages > 0 && (
                <div
                    style={{
                        height: "120px",
                        display: "flex",
                        alignItems: "flex-end",
                        justifyContent: "center",
                        paddingBottom: "8px",
                    }}
                >
                    <div className="flex items-center justify-center gap-2">
                        <button
                            onClick={() =>
                                setCurrentPage((page) => page - 1)
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
                                setCurrentPage((page) => page + 1)
                            }
                            disabled={currentPage === totalPages}
                            className="flex h-8 w-8 items-center justify-center rounded-md border border-gray-200 bg-white text-sm font-semibold text-slate-700 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40"
                        >
                            ›
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}