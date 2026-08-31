import { ReactNode } from "react";

import Sidebar from "./Sidebar";

type DashboardLayoutProps = {
    children: ReactNode;
};

export default function DashboardLayout({
    children,
}: DashboardLayoutProps) {
    return (
        <div className="flex min-h-screen bg-slate-50">
            <Sidebar />

            <main className="ml-[220px] flex-1 min-w-0 p-8">
                {children}
            </main>
        </div>
    );
}