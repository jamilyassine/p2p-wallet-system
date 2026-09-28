from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.funding import Funding


class FundingRepository:

    def create(
        self,
        db: Session,
        funding: Funding,
    ) -> bool:

        stmt = (
            insert(Funding)
            .values(
                funding_id=funding.funding_id,
                wallet_id=funding.wallet_id,
                amount=funding.amount,
            )
            .on_conflict_do_nothing(
                index_elements=[Funding.funding_id],
            )
            .returning(Funding.id)
        )

        result = db.execute(stmt)
        inserted_id = result.scalar_one_or_none()

        if inserted_id is None:
            return False

        funding.id = inserted_id

        return True

    def get_by_funding_id(
        self,
        db: Session,
        funding_id: UUID,
    ) -> Funding | None:

        return (
            db.query(Funding)
            .filter(Funding.funding_id == funding_id)
            .first()
        )

    def get_by_funding_id_for_update(
        self,
        db: Session,
        funding_id: UUID,
    ) -> Funding | None:

        return (
            db.query(Funding)
            .filter(Funding.funding_id == funding_id)
            .with_for_update()
            .first()
        )


funding_repository = FundingRepository()