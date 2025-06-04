from .settings_section import router as s_router
from .categories_section import router as c_router
from .banwords import router as b_router
from .price import router as p_router
from .view_count import router as vc_router

routers_list = [
    s_router,
    c_router,
    b_router,
    p_router,
    vc_router
]
