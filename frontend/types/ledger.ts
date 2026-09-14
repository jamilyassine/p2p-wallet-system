export interface LedgerEntry {
    transfer_id: number;
    wallet_id: number;
    wallet_user_name: string;
    entry_type: "DEBIT" | "CREDIT";
    amount: string;
    created_at: string;
}