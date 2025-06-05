from .start import router as start_router
from .callbacks import routers_list as callback_routers
from .admin_panel import router as admin_router


routers_list = [
    admin_router,
    start_router,
    *callback_routers,
]




