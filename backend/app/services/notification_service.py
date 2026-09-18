from app.models.notification import Notification
from app.repositories.notification_repository import notification_repository


class NotificationService:

    def create_notification(
        self,
        db,
        user_id: int,
        notification_type: str,
        message: str,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            message=message,
        )

        return notification_repository.create(
            db,
            notification,
        )

    def get_user_notifications(
        self,
        db,
        user_id: int,
    ) -> list[Notification]:
        return notification_repository.get_by_user_id(
            db,
            user_id,
        )

    def mark_as_read(
        self,
        db,
        notification_id: int,
        user_id: int,
    ) -> Notification | None:
        notification = notification_repository.get_by_id(
            db,
            notification_id,
        )

        if notification is None:
            return None

        if notification.user_id != user_id:
            return None

        return notification_repository.mark_as_read(
            notification,
        )


notification_service = NotificationService()