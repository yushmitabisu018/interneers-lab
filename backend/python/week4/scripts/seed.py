import logging
from ..models import ProductCategory
logger = logging.getLogger(__name__)


def seed_categories():
    categories = ["Food", "Electronics", "Clothing"]

    for title in categories:
        if not ProductCategory.objects(title=title):
            ProductCategory(title=title).save()
    logger.info("Seeding done")