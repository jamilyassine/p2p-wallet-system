import { ReactNode } from "react";
import Sidebar from "./Sidebar";

type DashboardLayoutProps = {
  children: ReactNode;
};

export default function DashboardLayout({
  children,
}: DashboardLayoutProps) {
  return (
    <div className="min-h-screen flex">
      <Sidebar />

      <main className="flex-1 p-6">
        {children}
      </main>
    </div>
  );
}