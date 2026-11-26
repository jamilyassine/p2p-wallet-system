import { LedgerEntry } from "@/types/ledger";
import { apiFetch } from "@/lib/api";

export async function getWalletLedger(
    walletId: number,
): Promise<LedgerEntry[]> {
    const response = await apiFetch(
        `/ledger/wallet/${walletId}`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch wallet ledger");
    }

    return response.json();
}
