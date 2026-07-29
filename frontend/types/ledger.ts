export interface LedgerEntry {
    id: number;
    transfer_id: number;
    wallet_id: number;
    entry_type: "DEBIT" | "CREDIT";
    amount: number;
    created_at: string;
}

