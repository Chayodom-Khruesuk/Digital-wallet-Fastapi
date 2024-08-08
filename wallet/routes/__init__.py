from . import item_router, merchant_router, wallet_router, transaction_router, auth_router, user_router

def init_routers(app):
    app.include_router(user_router.router)
    app.include_router(auth_router.router)
    app.include_router(item_router.router)
    app.include_router(merchant_router.router)
    app.include_router(wallet_router.router)
    app.include_router(transaction_router.router)