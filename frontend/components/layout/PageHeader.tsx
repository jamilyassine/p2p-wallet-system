type PageHeaderProps = {
    title: string;
    subtitle: string;
};

export default function PageHeader({
    title,
    subtitle,
}: PageHeaderProps) {
    return (
        <header>
            <h1>{title}</h1>

            <p>{subtitle}</p>
        </header>
    );
}