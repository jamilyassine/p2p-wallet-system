"use client";

import { useEffect, useSyncExternalStore } from "react";
import { useRouter } from "next/navigation";
import { CheckCircle2 } from "lucide-react";

import { getAccessToken } from "@/lib/auth";

type TransferSuccessData = {
    transfer_id?: number | string;
    sender_name?: string;
    receiver_name?: string;
    amount?: number | string;
    created_at?: string;
};

let cachedRawTransfer: string | null = null;
let cachedTransfer: TransferSuccessData | null = null;

function getTransferSnapshot(): TransferSuccessData | null {
    if (typeof window === "undefined") {
        return null;
    }

    const storedTransfer = sessionStorage.getItem("transfer_success");

    if (storedTransfer === cachedRawTransfer) {
        return cachedTransfer;
    }

    cachedRawTransfer = storedTransfer;

    if (!storedTransfer) {
        cachedTransfer = null;
        return cachedTransfer;
    }

    try {
        cachedTransfer = JSON.parse(storedTransfer);
    } catch {
        cachedTransfer = null;
    }

    return cachedTransfer;
}

function getServerSnapshot(): TransferSuccessData | null {
    return null;
}

function subscribe(callback: () => void) {
    window.addEventListener("storage", callback);

    return () => {
        window.removeEventListener("storage", callback);
    };
}

export default function TransferSuccessfulPage() {
    const router = useRouter();

    const transfer = useSyncExternalStore(
        subscribe,
        getTransferSnapshot,
        getServerSnapshot
    );

    useEffect(() => {
        if (!getAccessToken()) {
            router.replace("/login");
            return;
        }

        if (!transfer) {
            sessionStorage.removeItem("transfer_success");
            router.replace("/dashboard");
        }
    }, [router, transfer]);

    const formattedDate = transfer?.created_at
        ? new Date(transfer.created_at).toLocaleString()
        : "—";

    return (
        <main
            style={{
                minHeight: "100vh",
                padding: "40px 24px",
                background:
                    "radial-gradient(circle at 50% 20%, #f0fdf4 0%, #ffffff 48%, #ecfdf5 100%)",
                overflow: "hidden",
            }}
        >
            <div
                style={{
                    width: "100%",
                    maxWidth: "900px",
                    margin: "0 auto",
                    textAlign: "center",
                }}
            >
                <div
                    style={{
                        position: "relative",
                        width: "420px",
                        height: "190px",
                        margin: "0 auto",
                    }}
                >
                    <span
                        style={{
                            position: "absolute",
                            left: "35px",
                            top: "65px",
                            width: "9px",
                            height: "16px",
                            background: "#60a5fa",
                            transform: "rotate(25deg)",
                            borderRadius: "2px",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            left: "90px",
                            top: "22px",
                            width: "9px",
                            height: "9px",
                            background: "#f472b6",
                            borderRadius: "50%",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            left: "145px",
                            top: "5px",
                            width: "9px",
                            height: "16px",
                            background: "#facc15",
                            transform: "rotate(-30deg)",
                            borderRadius: "2px",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            right: "145px",
                            top: "10px",
                            width: "9px",
                            height: "9px",
                            background: "#34d399",
                            borderRadius: "50%",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            right: "85px",
                            top: "30px",
                            width: "9px",
                            height: "16px",
                            background: "#fb923c",
                            transform: "rotate(30deg)",
                            borderRadius: "2px",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            right: "30px",
                            top: "72px",
                            width: "9px",
                            height: "9px",
                            background: "#60a5fa",
                            borderRadius: "50%",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            left: "70px",
                            bottom: "35px",
                            width: "9px",
                            height: "16px",
                            background: "#fb923c",
                            transform: "rotate(-25deg)",
                            borderRadius: "2px",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            right: "75px",
                            bottom: "32px",
                            width: "9px",
                            height: "16px",
                            background: "#f472b6",
                            transform: "rotate(25deg)",
                            borderRadius: "2px",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            left: "125px",
                            bottom: "12px",
                            width: "9px",
                            height: "9px",
                            background: "#34d399",
                            borderRadius: "50%",
                            zIndex: 10,
                        }}
                    />

                    <span
                        style={{
                            position: "absolute",
                            right: "120px",
                            bottom: "8px",
                            width: "9px",
                            height: "9px",
                            background: "#facc15",
                            borderRadius: "50%",
                            zIndex: 10,
                        }}
                    />

                    <div
                        style={{
                            position: "absolute",
                            left: "50%",
                            top: "50%",
                            transform: "translate(-50%, -50%)",
                            width: "78px",
                            height: "78px",
                            borderRadius: "50%",
                            backgroundColor: "#22c55e",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            boxShadow:
                                "0 8px 20px rgba(34,197,94,0.25)",
                            zIndex: 5,
                        }}
                    >
                        <CheckCircle2
                            size={48}
                            strokeWidth={2.8}
                            color="#ffffff"
                        />
                    </div>
                </div>

                <h1
                    style={{
                        margin: "0",
                        fontSize: "30px",
                        fontWeight: 700,
                        color: "#0f172a",
                    }}
                >
                    Transfer Successful!
                </h1>

                <p
                    style={{
                        marginTop: "8px",
                        fontSize: "14px",
                        color: "#64748b",
                    }}
                >
                    Your money has been sent successfully.
                </p>

                <div
                    style={{
                        width: "560px",
                        maxWidth: "100%",
                        margin: "32px auto 0",
                        padding: "20px 24px",
                        background: "rgba(255,255,255,0.97)",
                        border: "1px solid #dcfce7",
                        borderRadius: "12px",
                        boxShadow:
                            "0 10px 30px rgba(34,197,94,0.10)",
                        textAlign: "left",
                    }}
                >
                    <div
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "16px",
                        }}
                    >
                        {[
                            ["Transfer ID", transfer?.transfer_id ?? "—"],
                            ["From", transfer?.sender_name ?? "—"],
                            ["To", transfer?.receiver_name ?? "—"],
                            [
                                "Amount",
                                transfer?.amount !== undefined
                                    ? `$${Number(
                                          transfer.amount
                                      ).toFixed(2)}`
                                    : "$0.00",
                            ],
                            ["Date", formattedDate],
                        ].map(([label, value]) => (
                            <div
                                key={label}
                                style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    gap: "24px",
                                }}
                            >
                                <span
                                    style={{
                                        fontSize: "14px",
                                        color: "#64748b",
                                    }}
                                >
                                    {label}
                                </span>

                                <span
                                    style={{
                                        fontSize: "14px",
                                        fontWeight:
                                            label === "Amount"
                                                ? 600
                                                : 500,
                                        color: "#0f172a",
                                    }}
                                >
                                    {value}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                <div
                    style={{
                        width: "560px",
                        maxWidth: "100%",
                        margin: "24px auto 0",
                        display: "flex",
                        gap: "12px",
                    }}
                >
                    <button
                        onClick={() => router.push("/dashboard")}
                        style={{
                            flex: 1,
                            height: "44px",
                            border: "none",
                            borderRadius: "8px",
                            background: "#9810fa",
                            color: "#ffffff",
                            fontWeight: 500,
                            cursor: "pointer",
                        }}
                    >
                        Go to Dashboard
                    </button>

                    <button
                        onClick={() => router.push("/history")}
                        style={{
                            flex: 1,
                            height: "44px",
                            border: "1px solid #e2e8f0",
                            borderRadius: "8px",
                            background: "#ffffff",
                            color: "#334155",
                            fontWeight: 500,
                            cursor: "pointer",
                        }}
                    >
                        View History
                    </button>
                </div>
            </div>
        </main>
    );
}