import Link from "next/link";
import { Bell, UserRound } from "lucide-react";

type PageHeaderProps = {
    title: string;
    subtitle: string;
    userName?: string;
    userEmail?: string;
    showNotification?: boolean;
    showUser?: boolean;
};

export default function PageHeader({
    title,
    subtitle,
    userName,
    userEmail,
    showNotification = true,
    showUser = true,
}: PageHeaderProps) {
    return (
        <header className="mb-6 flex items-start justify-between">
            <div>
                <h1 className="text-2xl font-bold text-slate-900">
                    {title}
                </h1>

                <p className="mt-1 text-sm text-slate-500">
                    {subtitle}
                </p>
            </div>

            {showUser && (
                <div className="flex items-center gap-3">
                    {showNotification && (
                        <button className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600">
                            <Bell size={17} />
                        </button>
                    )}

                    <Link
                        href="/profile"
                        className="flex items-center gap-3"
                    >
                        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-200 text-slate-600">
                            <UserRound size={18} />
                        </div>

                        <div className="hidden sm:block">
                            <p className="text-sm font-semibold text-slate-800">
                                {userName}
                            </p>

                            <p className="text-xs text-slate-500">
                                {userEmail}
                            </p>
                        </div>
                    </Link>
                </div>
            )}
        </header>
    );
}
