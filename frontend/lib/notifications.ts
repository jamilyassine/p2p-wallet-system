import { apiFetch } from "@/lib/api";

export type Notification = {
    id: number;
    type: string;
    message: string;
    is_read: boolean;
    created_at: string;
};

export async function getNotifications(): Promise<Notification[]> {
    const response = await apiFetch("/notifications/");

    if (!response || !response.ok) {
        return [];
    }

    return response.json();
}

export async function markNotificationAsRead(
    notificationId: number
): Promise<Notification | null> {
    const response = await apiFetch(
        `/notifications/${notificationId}/read`,
        {
            method: "PATCH",
        }
    );

    if (!response || !response.ok) {
        return null;
    }

    return response.json();
}