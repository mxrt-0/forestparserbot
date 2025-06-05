from constants import REQUIRED_CHANNELS 
from .check_channels_subscription import CheckSubscriptionQuery, CheckUsernameQuery, UpdateUser , CheckSubscription, CheckUsername

middlewares_message_list = [
    CheckSubscription(REQUIRED_CHANNELS),
    CheckUsername()
]

middlewares_query_list = [
    CheckSubscriptionQuery(REQUIRED_CHANNELS),
    #UpdateUser(),
    CheckUsernameQuery(),
]



