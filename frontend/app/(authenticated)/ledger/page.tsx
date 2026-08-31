"use client";

import { useEffect, useState } from "react";
import { Filter } from "lucide-react";

import PageHeader from "../../../components/layout/PageHeader";
import DashboardCard from "../../../components/layout/DashboardCard";

import type { LedgerEntry } from "@/types/ledger";

export default function LedgerPage() {
    const [entries, setEntries] = useState<LedgerEntry[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchLedger() {
            try {
                const response = await fetch(
                    "http://localhost:8000/ledger/recent"
                );

                const data: LedgerEntry[] = await response.json();
                setEntries(data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        }

        fetchLedger();
    }, []);

    return (
        <div>
            <div className="mb-6 flex items-start justify-between">
                <PageHeader
                    title="Ledger Entries"
                    subtitle="Dashboard  ›  Ledger"
                />

                <button className="flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-gray-50">
                    <Filter size={16} />
                    Filters
                </button>
            </div>

            <DashboardCard
                title=""
                value={
                    loading ? (
                        <div className="p-6 text-sm text-slate-500">
                            Loading ledger entries...
                        </div>
                    ) : entries.length === 0 ? (
                        <div className="p-6 text-sm text-slate-500">
                            No ledger entries found.
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full border-collapse text-sm">
                                <thead className="bg-gray-100">
                                    <tr>
                                        <th className="border-b px-4 py-3 text-left font-semibold">
                                            ID
                                        </th>
                                        <th className="border-b px-4 py-3 text-left font-semibold">
                                            Transfer ID
                                        </th>
                                        <th className="border-b px-4 py-3 text-left font-semibold">
                                            Wallet
                                        </th>
                                        <th className="border-b px-4 py-3 text-left font-semibold">
                                            Type
                                        </th>
                                        <th className="border-b px-4 py-3 text-left font-semibold">
                                            Amount
                                        </th>
                                        <th className="border-b px-4 py-3 text-left font-semibold">
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
                                            <td className="border-b px-4 py-3">
                                                #{index + 1}
                                            </td>

                                            <td className="border-b px-4 py-3 font-medium text-purple-600">
                                                #{entry.transfer_id}
                                            </td>

                                            <td className="border-b px-4 py-3">
                                                User {entry.wallet_id}
                                            </td>

                                            <td
                                                className={`border-b px-4 py-3 font-medium ${
                                                    entry.entry_type === "DEBIT"
                                                        ? "text-red-600"
                                                        : "text-green-600"
                                                }`}
                                            >
                                                {entry.entry_type}
                                            </td>

                                            <td
                                                className={`border-b px-4 py-3 font-medium ${
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
                                                ).toLocaleString(
                                                    undefined,
                                                    {
                                                        minimumFractionDigits: 2,
                                                        maximumFractionDigits: 2,
                                                    }
                                                )}
                                            </td>

                                            <td className="border-b px-4 py-3">
                                                {new Date(
                                                    entry.created_at
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
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )
                }
            />
        </div>
    );
}