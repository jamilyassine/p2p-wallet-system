

type DashboardCardProps = {
  title: string;
  value: string;
};



export default function DashboardCard({
  title,
  value,
}: DashboardCardProps) {
  return (
    <div>
        <h2>{title}</h2>
        <p>{value}</p>
    </div>
  );
}