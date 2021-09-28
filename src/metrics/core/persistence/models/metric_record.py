from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.metrics.core.persistence.utils import Base


class MetricRecord(Base):
    __tablename__ = "metric_record"

    id = Column(Integer, primary_key=True)
    value = Column(Integer, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    metric_id = Column(Integer, ForeignKey("metric.id"))
    metric = relationship("Metric", backref="metric_record")

    def __repr__(self):
        return (
            f"<MetricRecord(id={self.id}, value={self.value}, "
            f"metric={self.metric}, created_at={self.created_at})>"
        )
