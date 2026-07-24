export interface TransferRead {
    id: number;
    sender_wallet_id: number;
    receiver_wallet_id: number;
    amount: number;
    status: string;
    created_at: string;
}