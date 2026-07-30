"use client";

import { useEffect, useState } from "react";

import { LedgerEntry } from "@/types/ledger";

export default function LedgerPage() {
    const [entries, setEntries] = useState<LedgerEntry[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchLedger() {
            try {
                const response = await fetch("http://localhost:8000/ledger/recent");

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

    if (loading) {
        return <p>Loading...</p>;
    }

    if (entries.length === 0) {
        return <p>No ledger entries found.</p>;
    }


    return (
        <div>
            <table>
                <thead>
                    <tr>
                        <th>Transfer ID</th>
                        <th>Entry Type</th>
                        <th>Amount</th>
                        <th>Wallet ID</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {entries.map((entry) => (
                    <tr
                        key={`${entry.transfer_id}-${entry.wallet_id}-${entry.entry_type}`}
                    >
                        <td>{entry.transfer_id}</td>
                        <td
                            className={
                            entry.entry_type === "DEBIT"
                            ? "text-red-600"
                            : "text-green-600"
                            }
                        >
                            {entry.entry_type}
                        </td>
                        <td>{entry.amount}</td>
                        <td>{entry.wallet_id}</td>
                        <td>{new Date(entry.created_at).toLocaleString()}</td>

                    </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );

}