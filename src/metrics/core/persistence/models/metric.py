from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

from src.metrics.core.persistence.models import db


class Metric(db.Model):
    __tablename__ = "metric"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    level = Column(String(7), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    parent_metric_id = Column(Integer, ForeignKey("metric.id"), nullable=True)
    parent_metric = relationship("Metric", remote_side=id)

    children_metrics = relationship(
        "Metric",
        backref=backref("parent", remote_side=id),
        collection_class=attribute_mapped_collection("name"),
        overlaps="parent_metric",
    )

    def __repr__(self):
        return (
            f"<Metric(id={self.id}, name={self.name}, "
            f"parent_metric={self.parent_metric}, "
            f"children_metrics={self.children_metrics}, "
            f"level={self.level}, "
            f"created_at={self.created_at})>"
        )
