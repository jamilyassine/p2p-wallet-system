import { getAccessToken } from "@/lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function apiFetch(
    path: string,
    options: RequestInit = {}
): Promise<Response> {
    const token = getAccessToken();

    const headers = new Headers(options.headers);

    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }

    const response = await fetch(`${API_URL}/api${path}`, {
        ...options,
        headers,
    });

    if (response.status === 401 && token) {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
    }

    return response;
}

export { API_URL };
