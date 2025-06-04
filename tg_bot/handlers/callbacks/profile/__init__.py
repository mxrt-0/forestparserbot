from .profile import router as profile_router 
from .referral_program import router as referral_router 

routers_list = [
    profile_router,
    referral_router
]
