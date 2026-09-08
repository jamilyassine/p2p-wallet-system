import Link from "next/link";
import { ArrowRight, Clock, Send } from "lucide-react";

type ActionCardProps = {
    title: string;
    description: string;
    href: string;
    icon: "send" | "clock";
};

export default function ActionCard({
    title,
    description,
    href,
    icon,
}: ActionCardProps) {
    const Icon = icon === "send" ? Send : Clock;

    return (
        <Link
            href={href}
            className="flex items-center justify-between rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition hover:shadow-md"
        >
            <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
                    <Icon className="h-5 w-5" />
                </div>

                <div>
                    <h2 className="text-sm font-semibold text-slate-800">
                        {title}
                    </h2>

                    <p className="mt-1 text-xs text-slate-500">
                        {description}
                    </p>
                </div>
            </div>

            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white">
                <ArrowRight className="h-4 w-4" />
            </div>
        </Link>
    );
}