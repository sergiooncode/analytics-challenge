from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.metrics.core.persistence.utils import Base


class Metric(Base):
    __tablename__ = "metric"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    parent_metric_id = Column(Integer, unique=False, nullable=True)
    level = Column(String(7), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<Metric(id={self.id}, name={self.name}, "
            f"parent_metric_id={self.parent_metric_id}, level={self.level}, "
            f"created_at={self.created_at})>"
        )
