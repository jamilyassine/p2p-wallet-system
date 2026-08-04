import Link from "next/link";
import DashboardCard from "./DashboardCard";

type ActionCardProps = {
    title: string;
    description: string;
    href: string;
};

export default function ActionCard({
    title,
    description,
    href,
}: ActionCardProps) {
    return (
        <Link href={href}>
            <DashboardCard
                title={title}
                value={
                    <p className="text-gray-500">
                        {description}
                    </p>
                }
            />
        </Link>
    );
}