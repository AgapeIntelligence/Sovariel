"""
Full production WebRTC + native MIDI device bridge
Direct hardware MIDI → galactic_coherence in real time
"""

import asyncio
import json
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from sovariel_kernel import SOVARIEL

# MIDI support via mido + python-rtmidi
try:
    import mido
    from mido import Message
    MIDI_AVAILABLE = True
except ImportError:
    print("MIDI not available — run: pip install mido python-rtmidi")
    MIDI_AVAILABLE = False

pcs: dict[str, RTCPeerConnection] = {}

class AudioForwardTrack(MediaStreamTrack):
    kind = "audio"
    def __init__(self, track, agent_id):
        super().__init__()
        self.track = track
        self.agent_id = agent_id

    async def recv(self):
        frame = await self.track.recv()
        raw = frame.to_ndarray().tobytes()
        SOVARIEL.trigger_hook("webrtc_voice_frame", raw, self.agent_id)
        return frame

async def midi_listener():
    """Listens to all connected MIDI devices and forwards to all WebRTC peers"""
    if not MIDI_AVAILABLE:
        return

    ports = mido.get_input_names()
    if not ports:
        print("No MIDI devices found")
        return

    print(f"Found MIDI devices: {ports}")
    print("Forwarding all MIDI messages to galactic_coherence")

    async def forward(port_name):
        try:
            with mido.open_input(port_name) as port:
                for msg in port:
                    if msg.type in ('note_on', 'note_off'):
                        velocity = msg.velocity if msg.type == 'note_on' else 0
                        for agent_id in pcs.keys():
                            SOVARIEL.trigger_hook("webrtc_midi_event",
                                msg.note, velocity / 127.0, agent_id)
        except Exception as e:
            print(f"MIDI error: {e}")

    # Spawn listener for each device
    tasks = [asyncio.create_task(forward(p)) for p in ports]
    await asyncio.gather(*tasks, return_exceptions=True)

async def handle_signaling(websocket, path):
    agent_id = None
    pc = None

    try:
        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "join":
                agent_id = data["agent_id"]
                SOVARIEL.register_agent(agent_id)
                await websocket.send(json.dumps({"type": "joined"}))

            elif data["type"] == "offer" and agent_id:
                pc = RTCPeerConnection()
                pcs[agent_id] = pc

                @pc.on("track")
                def on_track(track):
                    if track.kind == "audio":
                        pc.addTrack(AudioForwardTrack(track, agent_id))

                await pc.setRemoteDescription(RTCSessionDescription(**data["sdp"]))
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)

                await websocket.send(json.dumps({
                    "type": "answer",
                    "sdp": {"type": pc.localDescription.type, "sdp": pc.localDescription.sdp}
                }))

            elif data["type"] == "candidate" and agent_id and pc:
                if data.get("candidate"):
                    await pc.addIceCandidate(data["candidate"])

    except Exception as e:
        if agent_id:
            SOVARIEL._record_shared_memory(f"WebRTC error {agent_id}: {e}")
        if pc:
            await pc.close()
            pcs.pop(agent_id, None)

async def main():
    print("Sovariel WebRTC + Native MIDI Bridge → ws://0.0.0.0:8765")
    await asyncio.gather(
        websockets.serve(handle_signaling, "0.0.0.0", 8765),
        midi_listener()
    )

if __name__ == "__main__":
    asyncio.run(main())
