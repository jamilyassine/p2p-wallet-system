export default function TransferPage() {
  return (
    <div>
      <h1>Transfer</h1>

      <form>
        <div>
          <label>Sender Wallet ID</label>
          <input type="number" />
        </div>

        <div>
          <label>Receiver Wallet ID</label>
          <input type="number" />
        </div>

        <div>
          <label>Amount</label>
          <input type="number" step="0.01" />
        </div>

        <button type="submit">Transfer</button>
      </form>
    </div>
  );
}