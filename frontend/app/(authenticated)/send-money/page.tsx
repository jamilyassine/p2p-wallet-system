"use client";

import { Suspense, FormEvent, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
    UserRound,
    DollarSign,
    ShieldCheck,
} from "lucide-react";

import PageHeader from "../../../components/layout/PageHeader";

function SendMoneyContent() {
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const senderId = userId ?? "";

    const [receiverId, setReceiverId] = useState("");
    const [amount, setAmount] = useState("");
    const [description, setDescription] = useState("");

    const [transferResult, setTransferResult] = useState<{
        sender_balance: number;
        receiver_balance: number;
    } | null>(null);

    const [errorMessage, setErrorMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();

        setErrorMessage("");
        setTransferResult(null);
        setIsLoading(true);

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/transfers/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        request_id: crypto.randomUUID(),
                        sender_id: Number(senderId),
                        receiver_id: Number(receiverId),
                        amount: Number(amount),
                    }),
                }
            );

            const data = await response.json();

            if (response.ok) {
                setTransferResult(data);
                return;
            }

            setErrorMessage(
                data.error ?? "An unexpected error occurred."
            );
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="max-w-4xl">
            <PageHeader
                title="Send Money"
                subtitle="Dashboard  ›  Send Money"
            />

            <section className="rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
                <form onSubmit={handleSubmit} className="space-y-6">

                    {/* Recipient */}
                    <div>
                        <label
                            htmlFor="receiver"
                            className="mb-2 block text-sm font-medium text-gray-800"
                        >
                            Recipient User ID
                        </label>

                        <div className="relative">
                            <UserRound
                                size={18}
                                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                            />

                            <input
                                id="receiver"
                                type="number"
                                placeholder="Enter recipient user ID"
                                value={receiverId}
                                onChange={(e) =>
                                    setReceiverId(e.target.value)
                                }
                                required
                                className="h-11 w-full rounded-lg border border-gray-200 bg-white pl-10 pr-4 text-sm outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
                            />
                        </div>
                    </div>

                    {/* Amount */}
                    <div>
                        <label
                            htmlFor="amount"
                            className="mb-2 block text-sm font-medium text-gray-800"
                        >
                            Amount (USD)
                        </label>

                        <div className="relative">
                            <DollarSign
                                size={18}
                                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                            />

                            <input
                                id="amount"
                                type="number"
                                step="0.01"
                                min="0"
                                placeholder="0.00"
                                value={amount}
                                onChange={(e) =>
                                    setAmount(e.target.value)
                                }
                                required
                                className="h-11 w-full rounded-lg border border-gray-200 bg-white pl-10 pr-4 text-sm outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
                            />
                        </div>
                    </div>

                    {/* Description */}
                    <div>
                        <label
                            htmlFor="description"
                            className="mb-2 block text-sm font-medium text-gray-800"
                        >
                            Description (optional)
                        </label>

                        <input
                            id="description"
                            type="text"
                            placeholder="What's this for?"
                            value={description}
                            onChange={(e) =>
                                setDescription(e.target.value)
                            }
                            className="h-11 w-full rounded-lg border border-gray-200 bg-white px-4 text-sm outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
                        />
                    </div>

                    {/* Review button */}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="h-11 w-full rounded-lg bg-purple-600 font-medium text-white transition hover:bg-purple-700 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        {isLoading
                            ? "Processing..."
                            : "Review Transfer"}
                    </button>

                    {/* Security notice */}
                    <div className="flex items-start gap-3 rounded-lg bg-purple-50 p-4">
                        <ShieldCheck
                            size={22}
                            className="mt-0.5 shrink-0 text-purple-600"
                        />

                        <div>
                            <p className="text-sm font-medium text-gray-800">
                                All transfers are secure and encrypted.
                            </p>

                            <p className="mt-1 text-xs text-gray-500">
                                You will be able to review before confirming.
                            </p>
                        </div>
                    </div>

                    {/* Error */}
                    {errorMessage && (
                        <p className="text-sm text-red-600">
                            {errorMessage}
                        </p>
                    )}

                    {/* Success */}
                    {transferResult && (
                        <div className="rounded-lg bg-green-50 p-4 text-sm text-green-700">
                            <p className="font-medium">
                                Transfer completed successfully!
                            </p>

                            <p>
                                Sender balance:{" "}
                                {transferResult.sender_balance}
                            </p>

                            <p>
                                Receiver balance:{" "}
                                {transferResult.receiver_balance}
                            </p>
                        </div>
                    )}
                </form>
            </section>
        </div>
    );
}

export default function SendMoneyPage() {
    return (
        <Suspense fallback={<div>Loading transfer page...</div>}>
            <SendMoneyContent />
        </Suspense>
    );
}