import { createClient } from "graphql-ws";

const client = createClient({
  url: "ws://localhost:8000/graphql",  // adjust if using HTTPS
  connectionParams: () => {
    const token = localStorage.getItem("auth_token");
    return {
      headers: {
        Authorization: token ? `Bearer ${token}` : ""
      }
    };
  },
});

let pollInterval = null;

function startPolling(stateName) {
  pollInterval = setInterval(async () => {
    const res = await fetch("http://localhost:8000/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("auth_token")
      },
      body: JSON.stringify({
        query: `
          query {
            playerStatus {
              track { title subtitle artists }
              queue { title subtitle artists }
            }
          }
        `
      }),
    });
    const data = await res.json();
    const status = data?.data?.playerStatus;
    if (status) {
      Reflex.setState(stateName, {
        current_track: status.track,
        upcoming_queue: status.queue.slice(0, 3)
      });
    }
  }, 3000);
}

export function subscribeToTrackChanged(stateName) {
    try {
      client.subscribe(
        {
          query: `
            subscription {
              trackChanged {
                title
                subtitle
                artists
              }
            }
          `,
        },
        {
          next: (data) => {
            Reflex.setState(stateName, {
              current_track: data?.data?.trackChanged,
            });
          },
          error: (err) => {
            console.error("WebSocket failed, falling back to polling.", err);
            startPolling(stateName);
          },
          complete: () => {
            console.log("Subscription closed.");
          },
        }
      );
    } catch (err) {
      startPolling(stateName);
    }
  }