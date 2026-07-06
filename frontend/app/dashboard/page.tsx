import PageHeader from "../../components/layout/PageHeader";
import DashboardLayout from "../../components/layout/DashboardLayout";
import DashboardCard from "../../components/layout/DashboardCard";

export default function DashboardPage() {
  return (
    <DashboardLayout>

    <PageHeader
        title="Dashboard"
        subtitle="Welcome to the P2P Wallet System"
    />


    <DashboardCard
        title="Total Balance"
        value="$0.00"
    />


    <DashboardCard
        title="Recent Transactions"
        value="No transactions yet"
    />

    <DashboardCard
        title="Wallets"
        value="0"
    />

</DashboardLayout>
  );
}
