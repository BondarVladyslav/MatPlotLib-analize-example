from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, String, DateTime, SmallInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class Site(Base):
    __tablename__ = "dashboard_site"

    id: Mapped[int] = mapped_column(primary_key=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime)
    link: Mapped[str] = mapped_column(String(255), unique=True)

    responses: Mapped[list["SiteResponse"]] = relationship(
        back_populates="site",
        cascade="all, delete-orphan",
    )


class SiteResponse(Base):
    __tablename__ = "dashboard_siteresponse"

    id: Mapped[int] = mapped_column(primary_key=True)
    status_code: Mapped[Optional[int]] = mapped_column(SmallInteger)
    error: Mapped[Optional[str]] = mapped_column(String(100))
    checked_at: Mapped[datetime] = mapped_column(DateTime)
    site_id: Mapped[int] = mapped_column(ForeignKey("dashboard_site.id"))
    response_time: Mapped[Optional[int]] = mapped_column(Integer)

    site: Mapped["Site"] = relationship(back_populates="responses")
