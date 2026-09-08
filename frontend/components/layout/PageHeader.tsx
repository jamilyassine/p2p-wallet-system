type PageHeaderProps = {
    title: string;
    subtitle: string;
    userName?: string;
    userEmail?: string;
};

export default function PageHeader({
    title,
    subtitle,
    userName,
    userEmail,
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

            <div className="flex items-center gap-3">
                <button className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-white">
                    🔔
                </button>

                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-200 text-sm font-semibold text-slate-600">
                    {userName?.charAt(0).toUpperCase()}
                </div>

                <div className="hidden sm:block">
                    <p className="text-sm font-semibold text-slate-800">
                        {userName}
                    </p>
                    <p className="text-xs text-slate-500">
                        {userEmail}
                    </p>
                </div>
            </div>
        </header>
    );
}