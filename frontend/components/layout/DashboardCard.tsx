import { ReactNode } from "react";

type DashboardCardProps = {
    title: string;
    value: ReactNode;
};

export default function DashboardCard({
    title,
    value,
}: DashboardCardProps) {
    return (
        <section className="w-full bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden mb-6">
            <h2 className="px-6 pt-5 text-lg font-semibold">
                {title}
            </h2>

            <div className="px-6 py-5">
                {value}
            </div>
        </section>
    );
}