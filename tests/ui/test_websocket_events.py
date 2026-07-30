import pytest
from playwright.sync_api import Page, WebSocket
from config.config import Config

@pytest.mark.ui
def test_websocket_connection_monitoring(page: Page):
    """Monitor WebSocket connections and capture frame transmissions in real time."""
    ws_connections = []

    def on_websocket(ws: WebSocket):
        ws_connections.append(ws.url)
        print(f"\n⚡ WebSocket Opened: {ws.url}")

    # Register WebSocket listener
    page.on("websocket", on_websocket)
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    print(f"\n✅ Day 8 Practice: Monitored {len(ws_connections)} active WebSocket connections!")

@pytest.mark.ui
def test_websocket_frame_payload_interception(page: Page):
    """Intercept WebSocket sent and received frame payloads."""
    frames_received = []

    def on_websocket(ws: WebSocket):
        def on_frame_received(payload):
            frames_received.append(payload)

        ws.on("framereceived", on_frame_received)

    page.on("websocket", on_websocket)
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")

    print(f"✅ Day 8 Practice: Captured {len(frames_received)} real-time WebSocket frame events!")
