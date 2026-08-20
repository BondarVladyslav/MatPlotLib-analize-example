from sqlalchemy import func, select
from .database import SessionLocal
from .models import Site, SiteResponse


def select_sites_with_avg_time():
    with SessionLocal() as session:
        stmt = (
            select(
                Site.link,
                func.avg(SiteResponse.response_time),
            )
            .join(SiteResponse)
            .group_by(Site.id, Site.link)
        )

        response = session.execute(stmt)
        return response.all()


def select_responses_time():
    with SessionLocal() as session:
        stmt = select(Site.link, SiteResponse.response_time).join(Site)

        response = session.execute(stmt)
        return response.all()


def select_responses_status_code():
    with SessionLocal() as session:
        stmt = select(Site.link, SiteResponse.status_code).join(Site)

        response = session.execute(stmt)
        return response.all()
