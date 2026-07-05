import PageHeader from "../../components/layout/PageHeader";
import DashboardLayout from "../../components/layout/DashboardLayout";

export default function DashboardPage() {
  return (
    <DashboardLayout>

    <PageHeader
        title="Dashboard"
        subtitle="Welcome to the P2P Wallet System"
    />

    <div>
        <h2>Total Balance</h2>
        <p>$0.00</p>
    </div>

    <div>
        <h2>Recent Transactions</h2>
        <p>No transactions yet</p>
    </div>

</DashboardLayout>
  );
}
