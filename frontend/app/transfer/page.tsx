export default function TransferPage() {
    return (
        <main>
            <h1>Transfer</h1>

            <form>
                <div>
                    <label htmlFor="senderWalletId">
                        Sender Wallet ID
                    </label>

                    <input
                        id="senderWalletId"
                        type="number"
                    />
                </div>

                <div>
                    <label htmlFor="receiverWalletId">
                        Receiver Wallet ID
                    </label>

                    <input
                        id="receiverWalletId"
                        type="number"
                    />
                </div>

                <div>
                    <label htmlFor="amount">
                        Amount
                    </label>

                    <input
                        id="amount"
                        type="number"
                        step="0.01"
                    />
                </div>

                <button type="submit">
                    Transfer
                </button>
            </form>
        </main>
    );
}