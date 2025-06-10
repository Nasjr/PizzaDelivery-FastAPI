from database.database import eninge,Base
from database.models import User,Order

Base.metadata.create_all(bind=eninge)