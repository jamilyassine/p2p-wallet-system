"use client";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import PageHeader from "../../components/layout/PageHeader";
import DashboardLayout from "../../components/layout/DashboardLayout";
import DashboardCard from "../../components/layout/DashboardCard";

export default function DashboardPage() {

    const searchParams = useSearchParams();
    const userId = searchParams.get("userId");
    const [user, setUser] = useState<any>(null);
    const [wallet, setWallet] = useState<any>(null);
    const [transfers, setTransfers] = useState<any[]>([]);
    
    useEffect(() => {
        if (!userId) return;

        fetch(`http://localhost:8000/users/${userId}`)
            .then((response) => response.json())
            .then((data) => {
            setUser(data);
        });
   }, [userId]);

   useEffect(() => {
        if (!userId) return;

        fetch(`http://localhost:8000/wallets/user/${userId}`)
        .then((response) => response.json())
        .then((data) => {
        setWallet(data);
        });
    }, [userId]);

    useEffect(() => {
        if (!userId) return;

        fetch(`http://localhost:8000/transfers/user/${userId}`)
            .then((response) => response.json())
            .then((data) => {
            setTransfers(data);
            });
        }, [userId]);


  return (
    <DashboardLayout>

    <PageHeader
        title="Dashboard"
        subtitle={
            user
                ? `Welcome, ${user.name}!`
                : "Loading..."
            }
    />


    <DashboardCard
        title="Total Balance"
        value={wallet ? `$${wallet.balance}` : "Loading..."}
    />


    <DashboardCard
        title="Recent Transactions"
        value={
            transfers.length === 0
            ? "No transactions yet"
            : transfers.map((transfer: any) => (
                <div key={transfer.id}>
                    ${transfer.amount} - {transfer.status}
                </div>
            ))
        }
    />

    

</DashboardLayout>
  );
}
