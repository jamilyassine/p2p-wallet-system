"use client";

import { Suspense, FormEvent, useState } from "react";
import { useSearchParams } from "next/navigation";

function SendMoneyContent() {
    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");

    const senderId = userId ?? "";

    const [receiverId, setReceiverId] = useState("");
    const [amount, setAmount] = useState("");

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
        try{
            const response = await fetch(
                "http://127.0.0.1:8000/transfers/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        request_id:crypto.randomUUID(),
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
            }
        finally {
            setIsLoading(false);
        }
}

    return (
        <main>
            <h1>Send Money</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="sender">
                        Sender
                    </label>

                    <input
                        id="sender"
                        type="number"
                        value={senderId}
                        readOnly
                    />
                </div>

                <div>
                    <label htmlFor="receiver">
                        Receiver
                    </label>

                    <input
                        id="receiver"
                        type="number"
                        placeholder="Enter receiver ID"
                        value={receiverId}
                        onChange={(e) =>
                            setReceiverId(e.target.value)
                        }
                    />
                </div>

                <div>
                    <label htmlFor="amount">
                        Amount
                    </label>

                    <input
                        id="amount"
                        type="number"
                        placeholder="Enter amount"
                        value={amount}
                        onChange={(e) =>
                            setAmount(e.target.value)
                        }
                    />
                </div>

                <button
                    type="submit"
                    disabled={isLoading}
                >
                    {isLoading ? "Sending..." : "Send Money"}
                </button>

                {errorMessage && (
                    <p className="text-red-600">
                        {errorMessage}
                    </p>
                )}


                {transferResult && (
                    <div className="text-green-600">
                        <h2>Transfer completed successfully!</h2>

                        <p>Sender Balance: {transferResult.sender_balance}</p>
                        <p>Receiver Balance: {transferResult.receiver_balance}</p>
                    </div>
                )}
            </form>
        </main>
    );
}

export default function SendMoneyPage() {
    return (
        <Suspense fallback={<div>Loading transfer page...</div>}>
            <SendMoneyContent />
        </Suspense>
    );
}