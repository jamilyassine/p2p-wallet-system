export interface LedgerEntry {
    transfer_id: number;
    wallet_id: number;
    entry_type: "DEBIT" | "CREDIT";
    amount: string;
    created_at: string;
}