from .check_channels_subscription import router as ccs_router
from .step_back import router as sb_router
from .subscription import routers_list as subscription_routers
from .profile import routers_list as profile_routers 
from .settings import routers_list as settings_routers
from .parser import routers_list as parser_routers

routers_list = [
    ccs_router,
    sb_router,
    *subscription_routers,
    *profile_routers,
    *settings_routers,
    *parser_routers,
]

