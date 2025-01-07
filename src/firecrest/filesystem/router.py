# helpers
from lib.helpers.router_helper import create_router

# routers
from firecrest.filesystem.transfer.router import router as transfer_router
from firecrest.filesystem.ops.router import router as ops_router


router = create_router(
    prefix="/filesystem",
    tags=["filesystem"],
)

router.include_router(router=transfer_router)
router.include_router(router=ops_router)
