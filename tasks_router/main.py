from fastapi import FastAPI

from tasks_router.routers.task_router import router as task_router
from tasks_router.routers.user_router import router as user_router
from tasks_router.routers.system_router import router as system_router
from tasks_router.database.initiate_db import Database, Base
from tasks_router.database.config_db import settings

db: Database = Database(settings)
Base.metadata.create_all(bind=db.get_engine())

router = FastAPI(redirect_slashes=False)

router.include_router(task_router)
router.include_router(user_router)
router.include_router(system_router)