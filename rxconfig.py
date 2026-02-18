import reflex as rx

config = rx.Config(
    app_name="AMM_web",
    state_auto_setters=True,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
