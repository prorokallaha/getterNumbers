from aiogram import Router


def register_routers(router: Router, *sub_routers: Router) -> None:
    router.include_routers(*sub_routers)
