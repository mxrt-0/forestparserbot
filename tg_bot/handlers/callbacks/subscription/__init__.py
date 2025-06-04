from .subscription_section import router as ss_router
from .top_up_balance import router as tub_router
from .buy_subscription import router as bs_router

routers_list = [
    ss_router,
    tub_router,
    bs_router
]

