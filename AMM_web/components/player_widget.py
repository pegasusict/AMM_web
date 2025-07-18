import reflex as rx
from state.player_state import PlayerState


def PlayerWidget() -> rx.Component:
    return rx.box(
        # Scripts
        rx.script(src="/graphql/subscriptions.js", is_module=True),
        rx.script(PlayerState.start_track_subscription()),
        rx.script(PlayerState.start_timer()),
        # Header
        rx.heading("🎧 Music Player", size="5", weight="bold"),
        # Controls
        rx.hstack(
            rx.button("📝 Lyrics", on_click=PlayerState.toggle_lyrics),

            rx.modal(
                is_open=PlayerState.show_lyrics,
                on_close=PlayerState.toggle_lyrics,
                header="Lyrics",
                body=rx.text(PlayerState.current_track.get("lyrics", "No lyrics available.")),
                footer=rx.button("Close", on_click=PlayerState.toggle_lyrics),
            ),

            rx.button("▶️", on_click=[PlayerState.play, PlayerState.toggle_timer(True)]),
            rx.button("⏸️", on_click=[PlayerState.pause, PlayerState.toggle_timer(False)]),
            rx.button("⏭️", on_click=[PlayerState.play_next, PlayerState.toggle_timer(True)]),
            rx.slider(
                value=PlayerState.volume,
                on_change=lambda v: PlayerState.set_state("volume", v),
                min_=0,
                max_=100,
                step=5,
                width="100px",
            ),
            rx.text(f"🔊 {PlayerState.volume}%", size="1", color="gray"),
            spacing="4",
            wrap="wrap",
            align="center",
        ),
        rx.divider(),
        # Now playing
        rx.cond(
            PlayerState.current_track,
            lambda: rx.hstack(
                # Art
                rx.image(
                    src=PlayerState.current_track.get("album_picture", "/placeholder.png"),
                    alt="Album Art",
                    box_size="120px",
                    border_radius="lg",
                    fallback_src="/placeholder.png",
                ),
                # Info + progress
                rx.vstack(
                    rx.text(PlayerState.current_track.get("title", "Untitled"), weight="bold", size="4"),
                    rx.text(", ".join(PlayerState.current_track.get("artists", ["Unknown Artist"]))),
                    rx.text(PlayerState.current_track.get("subtitle", "")),
                    rx.progress(
                        value=PlayerState.elapsed_seconds,
                        max=PlayerState.current_track.get("duration_seconds", 100),
                        color_scheme="green",
                        size="sm",
                        width="100%",
                    ),
                    rx.text(
                        f"{PlayerState.elapsed_seconds} / {PlayerState.current_track.get('duration_seconds', 0)} sec",
                        size="1",
                        color="gray",
                    ),
                    rx.slider(
                        value=PlayerState.elapsed_seconds,
                        max=PlayerState.current_track.get("duration_seconds", 100),
                        on_change=lambda v: [
                            PlayerState.set_state("elapsed_seconds", v),
                            rx.script(f'graphqlRequest("mutation {{ setPosition(seconds: {v}) }}")')
                        ],
                        color_scheme="green",
                        width="100%",
                    ),

                ),
                spacing="4",
                wrap="wrap",
                align="start",
            ),
            rx.text("🎵 Nothing playing."),
        ),
        rx.divider(),
        # Queue
        rx.box(
            rx.heading("🎶 Up Next:"),
            rx.foreach(PlayerState.upcoming_queue, lambda track: rx.text(f"{track.get('title', 'Untitled')} — {', '.join(track.get('artists', []) or [])}")),
        ),
        rx.slider(
            value=PlayerState.volume,
            on_change=lambda v: [
                PlayerState.set_state("volume", v),
                rx.script(f'graphqlRequest("mutation {{ setVolume(level: {v}) }}")')
            ],
            min_=0,
            max_=100,
            step=5,
        )

        # Style
        padding="1em",
        width="100%",
        max_width="800px",
        border="1px solid #ccc",
        border_radius="md",
        box_shadow="md",
        background="white",
        margin_y="1em",
    )
