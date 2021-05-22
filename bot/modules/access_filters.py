from telegram.ext import BaseFilter
from main import OWNER_ID


class CustomFilter:
    class _OwnerFilter(BaseFilter):
        def filter(self, message):
            return bool(message.from_user.id == OWNER_ID)
    owner_filter = _OwnerFilter()
