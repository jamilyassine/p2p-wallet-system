import { LedgerEntry } from "@/types/ledger";

export async function getWalletLedger(
    walletId: number,
): Promise<LedgerEntry[]> {
    const response = await fetch(
        `http://localhost:8000/ledger/wallet/${walletId}`
    );

    return response.json();
}

