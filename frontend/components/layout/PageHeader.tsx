type PageHeaderProps = {
    title: string;
    subtitle: string;
};

export default function PageHeader({
    title,
    subtitle,
}: PageHeaderProps) {
    return (
        <header className="mb-2">
            <h1 className="whitespace-nowrap text-2xl font-bold text-slate-900">
                {title}
            </h1>

            <div className="mt-1 text-sm text-gray-500">
                Dashboard <span className="mx-1">›</span> History
            </div>

        </header>
    );
}