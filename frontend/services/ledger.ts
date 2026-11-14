import { LedgerEntry } from "@/types/ledger";
import { API_URL } from "@/lib/api";

export async function getWalletLedger(
    walletId: number,
): Promise<LedgerEntry[]> {
    const response = await fetch(
        `${API_URL}/ledger/wallet/${walletId}`
    );

    return response.json();
}

