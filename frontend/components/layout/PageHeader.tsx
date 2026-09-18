"use client";

import Link from "next/link";
import { createPortal } from "react-dom";
import { useEffect, useRef, useState } from "react";
import { Bell, UserRound } from "lucide-react";

import {
    getNotifications,
    markNotificationAsRead,
    type Notification,
} from "@/lib/notifications";

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
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [isNotificationOpen, setIsNotificationOpen] = useState(false);
    const [notificationPosition, setNotificationPosition] = useState({
        top: 0,
        right: 0,
    });

    const notificationButtonRef = useRef<HTMLButtonElement>(null);
    const notificationMenuRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        async function fetchNotifications() {
            const data = await getNotifications();
            setNotifications(data);
        }

        fetchNotifications();
    }, []);

    const unreadCount = notifications.filter(
        (notification) => !notification.is_read
    ).length;

    function updateNotificationPosition() {
        const button = notificationButtonRef.current;

        if (!button) return;

        const rect = button.getBoundingClientRect();

        setNotificationPosition({
            top: rect.bottom + 8,
            right: window.innerWidth - rect.right,
        });
    }

    useEffect(() => {
        if (!isNotificationOpen) return;

        updateNotificationPosition();

        function handleResize() {
            updateNotificationPosition();
        }

        function handleScroll() {
            updateNotificationPosition();
        }

        window.addEventListener("resize", handleResize);
        window.addEventListener("scroll", handleScroll, true);

        return () => {
            window.removeEventListener("resize", handleResize);
            window.removeEventListener("scroll", handleScroll, true);
        };
    }, [isNotificationOpen]);

    useEffect(() => {
        if (!isNotificationOpen) return;

        function handleOutsideClick(event: MouseEvent) {
            const target = event.target as Node;

            if (
                notificationButtonRef.current?.contains(target) ||
                notificationMenuRef.current?.contains(target)
            ) {
                return;
            }

            setIsNotificationOpen(false);
        }

        document.addEventListener("mousedown", handleOutsideClick);

        return () => {
            document.removeEventListener("mousedown", handleOutsideClick);
        };
    }, [isNotificationOpen]);

    async function handleNotificationClick(
        notification: Notification
    ) {

        if (notification.is_read) return;

        setNotifications((current) =>
            current.map((item) =>
                item.id === notification.id
                    ? { ...item, is_read: true }
                    : item
            )
        );

        setIsNotificationOpen(false);

        const updated = await markNotificationAsRead(notification.id);

        if (!updated) {
            setNotifications((current) =>
                current.map((item) =>
                    item.id === notification.id
                        ? { ...item, is_read: false }
                        : item
                )
            );
        }
    }

    const notificationDropdown =
        isNotificationOpen && typeof document !== "undefined"
            ? createPortal(
                  <div
                      ref={notificationMenuRef}
                      className="fixed z-[9999] w-80 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-lg"
                      style={{
                          top: `${notificationPosition.top}px`,
                          right: `${notificationPosition.right}px`,
                      }}
                  >
                      <div className="border-b border-slate-100 px-4 py-3">
                          <div className="flex items-center justify-between">
                              <h3 className="text-sm font-semibold text-slate-900">
                                  Notifications
                              </h3>

                              {unreadCount > 0 && (
                                  <span className="text-xs text-purple-600">
                                      {unreadCount} unread
                                  </span>
                              )}
                          </div>
                      </div>

                      <div className="max-h-80 overflow-y-auto">
                          {notifications.length === 0 ? (
                              <div className="px-4 py-8 text-center text-sm text-slate-500">
                                  No notifications yet.
                              </div>
                          ) : (
                              notifications.map((notification) => (
                                  <button
                                      key={notification.id}
                                      type="button"
                                      onClick={() =>
                                          handleNotificationClick(
                                              notification
                                          )
                                      }
                                      className={`block w-full border-b border-slate-100 px-4 py-3 text-left transition last:border-b-0 hover:bg-slate-50 ${
                                          notification.is_read
                                              ? "bg-white"
                                              : "bg-purple-50"
                                      }`}
                                  >
                                      <div className="flex items-start gap-3">
                                          <div
                                              className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
                                                  notification.is_read
                                                      ? "bg-slate-100 text-slate-500"
                                                      : "bg-purple-100 text-purple-600"
                                              }`}
                                          >
                                              <Bell size={15} />
                                          </div>

                                          <div className="min-w-0 flex-1">
                                              <p
                                                  className={`text-sm ${
                                                      notification.is_read
                                                          ? "font-medium text-slate-700"
                                                          : "font-semibold text-slate-900"
                                                  }`}
                                              >
                                                  {notification.message}
                                              </p>

                                              <p className="mt-1 text-xs text-slate-500">
                                                  {new Date(
                                                      notification.created_at
                                                  ).toLocaleString()}
                                              </p>
                                          </div>

                                          {!notification.is_read && (
                                              <span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-purple-600" />
                                          )}
                                      </div>
                                  </button>
                              ))
                          )}
                      </div>
                  </div>,
                  document.body
              )
            : null;

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
                        <div className="relative">
                            <div className="relative h-9 w-9">
                                <button
                                    ref={notificationButtonRef}
                                    type="button"
                                    onClick={() => {
                                        setIsNotificationOpen((open) => {
                                            const nextOpen = !open;

                                            if (nextOpen) {
                                                updateNotificationPosition();
                                            }

                                            return nextOpen;
                                        });
                                    }}
                                    className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
                                >
                                    <Bell size={17} />
                                </button>

                                {unreadCount > 0 && (
                                    <span
                                        style={{
                                            position: "absolute",
                                            top: "-6px",
                                            right: "-6px",
                                            minWidth: "20px",
                                            height: "20px",
                                            padding: "0 5px",
                                            borderRadius: "9999px",
                                            backgroundColor: "#dc2626",
                                            color: "#ffffff",
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "center",
                                            fontSize: "10px",
                                            fontWeight: 700,
                                            lineHeight: 1,
                                            border: "2px solid white",
                                            boxSizing: "border-box",
                                            zIndex: 100,
                                        }}
                                    >
                                        {unreadCount > 99
                                            ? "99+"
                                            : unreadCount}
                                    </span>
                                )}
                            </div>
                        </div>
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

            {notificationDropdown}
        </header>
    );
}