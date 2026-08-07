export interface TransferRead {
    id: number;
    sender_wallet_id: number;
    receiver_wallet_id: number;
    amount: number;
    status: string;
    sender_name: string;
    receiver_name: string;
    created_at: string;

}