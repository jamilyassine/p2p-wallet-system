"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
    UserRound,
    DollarSign,
    ShieldCheck,
} from "lucide-react";

import PageHeader from "../../../components/layout/PageHeader";
import { apiFetch } from "../../../lib/api";
import type { UserResponse } from "@/types/user";

function SendMoneyContent() {
    const router = useRouter();

    const [user, setUser] = useState<UserResponse | null>(null);
    const [receiverEmail, setReceiverEmail] = useState("");
    const [amount, setAmount] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);

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

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();

        setErrorMessage("");
        setIsLoading(true);

        try {
            const response = await apiFetch("/transfers/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    request_id: crypto.randomUUID(),
                    to_email: receiverEmail,
                    amount: Number(amount),
                }),
            });

            if (!response) return;

            const data = await response.json();

            if (response.ok) {
                sessionStorage.setItem(
                    "transfer_success",
                    JSON.stringify(data)
                );

                router.push("/transfer-successful");
                return;
            }

            setErrorMessage(
                data.error_code === "INSUFFICIENT_FUNDS"
                    ? "Insufficient funds."
                    : data.error_code === "SELF_TRANSFER"
                      ? "You cannot send money to yourself."
                      : data.error_code === "INVALID_TRANSFER_AMOUNT"
                        ? "Enter a valid transfer amount."
                        : data.error === "Wallet not found"
                          ? "Recipient not found."
                          : "An unexpected error occurred."
            );
        } catch (error) {
            console.error(error);
            setErrorMessage("Unable to complete the transfer.");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="w-full">
            <PageHeader
                title="Send Money"
                subtitle="Dashboard  ›  Send Money"
                userName={user?.name}
                userEmail={user?.email}
            />

            {/* Transfer form */}
            <div className="flex justify-center">
                <section
                    className="relative mt-32 w-full max-w-3xl rounded-xl border border-gray-200 bg-white p-8 shadow-sm"
                    style={{ transform: "translateY(80px)" }}
                >
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Recipient */}
                        <div>
                            <label
                                htmlFor="receiverEmail"
                                className="mb-2 block text-sm font-medium text-gray-800"
                            >
                                Recipient Email
                            </label>

                            <div className="relative">
                                <UserRound
                                    size={18}
                                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                                />

                                <input
                                    id="receiverEmail"
                                    type="email"
                                    placeholder="Enter recipient email"
                                    value={receiverEmail}
                                    onChange={(e) =>
                                        setReceiverEmail(e.target.value)
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
                                    min="0.01"
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

                        {/* Send button */}
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="h-11 w-full rounded-lg bg-purple-600 font-medium text-white transition hover:bg-purple-700 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            {isLoading ? "Processing..." : "Send Money"}
                        </button>

                        {/* Security notice */}
                        <div className="flex items-start gap-3 rounded-lg bg-purple-50 p-4">
                            <ShieldCheck
                                size={22}
                                className="mt-0.5 shrink-0 text-purple-600"
                            />

                            <div>
                                <p className="text-sm font-medium text-gray-800">
                                    Transfers are protected by authentication
                                    and transaction safeguards.
                                </p>

                                <p className="mt-1 text-xs text-gray-500">
                                    Review the recipient and amount before
                                    sending.
                                </p>
                            </div>
                        </div>

                        {/* Error */}
                        {errorMessage && (
                            <p className="text-sm text-red-600">
                                {errorMessage}
                            </p>
                        )}
                    </form>
                </section>
            </div>
        </div>
    );
}

export default function SendMoneyPage() {
    return <SendMoneyContent />;
}