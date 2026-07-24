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
        <section>
            <h2>{title}</h2>
            <div>{value}</div>
        </section>
    );
}