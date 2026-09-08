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
        <section className="w-full min-h-[180px] bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <h2 className="px-5 pt-4 text-base font-semibold">
                {title}
            </h2>

            <div className="px-5 py-6">
                {value}
            </div>
        </section>
    );
}