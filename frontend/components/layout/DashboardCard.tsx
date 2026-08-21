import { ReactNode } from "react";

type DashboardCardProps = {
    value: ReactNode;
};

export default function DashboardCard({
    value,
}: DashboardCardProps) {
    return (
        <section className="w-full bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden mb-6">
            {value}
        </section>
    );
}