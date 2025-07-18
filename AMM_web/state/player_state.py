import reflex as rx


class PlayerState(rx.State):
    player_data: dict = {}
    current_track: dict = {}
    upcoming_queue: list[dict] = []
    elapsed_seconds: int = 0
    timer_running: bool = False
    volume: int = 75  # 0–100
    show_lyrics: bool = False

    def start_timer(self):
        return rx.script(f"""
        if (!window._playerTimer) {{
            window._playerTimer = setInterval(() => {{
                const state = Reflex.getState("{self.get_full_name()}");
                if (state.timer_running) {{
                    const elapsed = state.elapsed_seconds + 1;
                    const duration = state.current_track?.duration_seconds || 0;
                    Reflex.setState("{self.get_full_name()}", {{ elapsed_seconds: elapsed }});
                    if (duration && elapsed >= duration) {{
                        Reflex.dispatch("{self.get_full_name()}.play_next");
                        Reflex.setState("{self.get_full_name()}", {{ elapsed_seconds: 0 }});
                    }}
                }}
            }}, 1000);
        }}
        """)

    def reset_timer(self):
        self.elapsed_seconds = 0

    def toggle_timer(self, run: bool):
        self.timer_running = run
        if run:
            self.reset_timer()

    def toggle_lyrics(self):
        self.show_lyrics = not self.show_lyrics

    def start_track_subscription(self):
        return rx.script(f'subscribeToTrackChanged("{self.get_full_name()}")')

    async def fetch_player_status(self):
        query = """
        query {
            playerStatus {
                isPlaying
                track {
                    title
                    artists
                }
            }
        }
        """
        script = f"""
        graphqlRequest({query!r}).then(data => {{
            const status = data?.data?.playerStatus || {{}};
            Reflex.setState("{self.get_full_name()}", {{
                player_data: status
            }});
        }});
        """
        return rx.script(script)

    async def trigger_mutation(self, mutation_name: str):
        mutation = f"mutation {{ {mutation_name} }}"
        script = f"""
        graphqlRequest({mutation!r}).then(() => {{
            Reflex.dispatch("{self.get_full_name()}.fetch_player_status");
        }});
        """
        return rx.script(script)

    def play(self):
        return self.trigger_mutation("play")

    def pause(self):
        return self.trigger_mutation("pause")

    def play_next(self):
        return self.trigger_mutation("play_next")
