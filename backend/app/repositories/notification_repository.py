from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationRepository:

    def create(
        self,
        db: Session,
        notification: Notification,
    ) -> Notification:
        db.add(notification)
        db.flush()
        return notification

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> list[Notification]:
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        notification_id: int,
    ) -> Notification | None:
        return (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    def mark_as_read(
        self,
        notification: Notification,
    ) -> Notification:
        notification.is_read = True
        return notification


notification_repository = NotificationRepository()