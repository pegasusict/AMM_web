"""
reflex_amm_web_client/
======================
Fully documented base skeleton for a Reflex-based AMM Web Client.
This structure is modular, scalable, and designed for professional development.
It integrates the AMM API client, uses Pydantic for type safety, and provides
an extendable base for both the public website and the AMM dashboard.
"""

# --- app.py ---
import reflex as rx
from pages import home, about, contact, dashboard

app = rx.App()

app.add_page(home.index, route="/", title="AMM Web Client")
app.add_page(about.index, route="/about", title="About")
app.add_page(contact.index, route="/contact", title="Contact")
app.add_page(dashboard.index, route="/dashboard", title="Dashboard")

app.compile()

# --- config.py ---
"""
Global configuration using pydantic-settings.
All environment variables are automatically loaded.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Global application configuration."""

    API_BASE_URL: str = "https://api.amm.local"
    API_TIMEOUT: int = 10
    SITE_NAME: str = "AMM Web Client"
    SITE_DESCRIPTION: str = "A modular Reflex-based Automated Market Maker interface."
    SENTRY_DSN: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AMM_")

settings = Settings()

# --- core/logging.py ---
"""
Centralized logging configuration.
"""
import logging

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=level,
    )
    logging.getLogger("reflex").setLevel(logging.WARNING)

# --- models/amm.py ---
"""
AMM domain models using Pydantic.
"""

from pydantic import BaseModel, Field
from typing import List

class Token(BaseModel):
    symbol: str
    name: str
    decimals: int = Field(..., ge=0, le=18)
    address: str

class Pool(BaseModel):
    id: str
    token_a: Token
    token_b: Token
    reserve_a: float
    reserve_b: float
    volume_24h: float

# --- services/amm_client.py ---
"""
Wrapper for the AMM API client.
Provides typed access via Pydantic models.
"""

from amm_api import AMMClient
from config import settings
from models.amm import Pool

class AMMService:
    """Service for interacting with the AMM backend API."""

    def __init__(self):
        self.client = AMMClient(base_url=settings.API_BASE_URL)

    def list_pools(self) -> list[Pool]:
        raw_pools = self.client.get_pools()
        return [Pool(**pool) for pool in raw_pools]

    def perform_swap(self, token_in: str, token_out: str, amount: float):
        return self.client.swap(token_in, token_out, amount)

amm_service = AMMService()

# --- state/base_state.py ---
"""Common reactive state shared by all components."""
import reflex as rx

class BaseState(rx.State):
    loading: bool = False
    error: str | None = None

    def set_loading(self, value: bool):
        self.loading = value

    def set_error(self, message: str | None):
        self.error = message

# --- state/amm_state.py ---
"""Manages AMM data and user interactions."""

from services.amm_client import amm_service
from models.amm import Pool
from .base_state import BaseState

class AmmState(BaseState):
    pools: list[Pool] = []

    async def load_pools(self):
        self.set_loading(True)
        try:
            self.pools = amm_service.list_pools()
        except Exception as e:
            self.set_error(str(e))
        finally:
            self.set_loading(False)

# --- components/navbar.py ---
"""Reusable navigation bar component."""
import reflex as rx

def navbar() -> rx.Component:
    return rx.hstack(
        rx.link("Home", href="/"),
        rx.link("About", href="/about"),
        rx.link("Dashboard", href="/dashboard"),
        rx.link("Contact", href="/contact"),
        justify="between",
        padding="1em",
    )

# --- components/footer.py ---
"""Reusable footer component."""
import reflex as rx

def footer() -> rx.Component:
    return rx.center(rx.text("© 2025 AMM Web Client"), padding="1em")

# --- pages/home.py ---
"""Public landing page with hero section."""
import reflex as rx
from components.navbar import navbar
from components.footer import footer

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.center(rx.heading("Welcome to the AMM Web Client")),
        rx.center(rx.text("Trade, provide liquidity, and explore pools effortlessly.")),
        footer(),
    )

# --- pages/about.py ---
import reflex as rx
from components.navbar import navbar
from components.footer import footer

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.center(rx.heading("About the AMM Web Client")),
        rx.text("This project provides a Reflex-based decentralized trading interface."),
        footer(),
    )

# --- pages/contact.py ---
import reflex as rx
from components.navbar import navbar
from components.footer import footer

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.center(rx.heading("Contact Us")),
        rx.text("For inquiries, reach out at contact@ammclient.io"),
        footer(),
    )

# --- pages/dashboard.py ---
"""AMM dashboard page showing pools and actions."""
import reflex as rx
from state.amm_state import AmmState
from components.navbar import navbar
from components.footer import footer

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.heading("Dashboard"),
        rx.foreach(AmmState.pools, lambda pool: rx.text(f"{pool.token_a.symbol}/{pool.token_b.symbol}")),
        footer(),
    )
