"""Dashboard page of the application."""

import reflex as rx
from page_base import page_base


def get_stats():
    """Fetch statistics for the dashboard."""
    # Placeholder values for demonstration purposes
    return {
        "processed": 400_000,
        "imported": 80_000,
        "parsed": 60_000,
        "fingerprinted": 40_000,
        "trimmed": 20_000,
        "converted": 10_000,
        "tags": 5_000,
        "art": 2_000,
        "lyrics": 3_000,
        "converted_files": 15_000,
        "playlists": 1,
        "playlists_tracks": 10_000,
        "users": 500,
        "guest_sessions": 1_000,
        "active_users": 300,
        "active_guests": 200,
        "active_playlists": 50,
    }


stats = get_stats()


@page_base
def dashboard() -> rx.Component:
    """Dashboard page of the application
    Returns:
        rx.Component: dashboard page
    """
    return rx.container(
        rx.vstack(
            rx.heading("AMM - Dashboard", size="2"),
            rx.text(f"Files Processed: {stats['processed']}", size="4", weight="medium"),
            rx.text(f"Files Imported: {stats['imported']}", size="4", weight="medium"),
            rx.text(f"Files Parsed: {stats['parsed']}", size="4", weight="medium"),
            rx.text(f"Files Fingerprinted: {stats['fingerprinted']}", size="4", weight="medium"),
            rx.text(f"Files Trimmed: {stats['trimmed']}", size="4", weight="medium"),
            rx.text(f"Files Converted: {stats['converted']}", size="4", weight="medium"),
            rx.text(f"Tags Retrieved: {stats['tags']}", size="4", weight="medium"),
            rx.text(f"Art Retrieved: {stats['art']}", size="4", weight="medium"),
            rx.text(f"Lyrics Retrieved: {stats['lyrics']}", size="4", weight="medium"),
            rx.text(f"Converted Files: {stats['converted_files']}", size="4", weight="medium"),
            rx.text(f"Playlists Created: {stats['playlists']}", size="4", weight="medium"),
            rx.text(f"Playlists Tracks: {stats['playlists_tracks']}", size="4", weight="medium"),
            rx.text(f"Users: {stats['users']}", size="4", weight="medium"),
            rx.text(f"Guest Sessions: {stats['guest_sessions']}", size="4", weight="medium"),
            rx.text(f"Active Users: {stats['active_users']}", size="4", weight="medium"),
            rx.text(f"Active Guests: {stats['active_guests']}", size="4", weight="medium"),
            rx.text(f"Active Playlists: {stats['active_playlists']}", size="4", weight="medium"),
        )
    )
