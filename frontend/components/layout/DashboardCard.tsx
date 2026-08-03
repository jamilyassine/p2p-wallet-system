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
    <section className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">
            {title}
        </h2>

        <div>
            {value}
        </div>
    </section>
);
}