from typing import Annotated, Union

from aiogram import types
from aiogram.filters import Filter

from src.common.sdi import Depends, inject
from src.core import Settings


class IsAdmin(Filter):
    async def __call__(
        self,
        event: Union[types.CallbackQuery, types.Message],
    ) -> bool:
        return event.from_user.id in self.settings.bot.admins

    @property
    @inject
    def settings(
        self, settings: Annotated[Settings, Depends(Settings, use_cache=True)]
    ) -> Settings:
        return settings
