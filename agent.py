from dotenv import load_dotenv
from metrics import log_metric, save_to_excel

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, UserStateChangedEvent, AgentStateChangedEvent
from livekit.agents import MetricsCollectedEvent
from livekit.plugins import google, cartesia, deepgram, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()

current_metrics = {}

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful voice AI assistant. "
                         "Answer every question clearly in max 2 lines. "
                         "If you don't know the answer, say 'I don't know'. "
                         "You can also ask for more information if needed."
        )

async def entrypoint(ctx: agents.JobContext):

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=google.LLM(model="gemini-2.0-flash", temperature=0.8),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel()
    )

    await ctx.connect()

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    @session.on("user_state_changed")
    def on_user_state_changed(ev: UserStateChangedEvent):
        if ev.new_state == "speaking":
            print("User started speaking")
        elif ev.new_state == "listening":
            print("User stopped speaking")
        elif ev.new_state == "away":
            print("User is not present (e.g. disconnected)")

    @session.on("agent_state_changed")
    def on_agent_state_changed(ev: AgentStateChangedEvent):
        global current_metrics
        if ev.new_state == "initializing":
            print("Agent is starting up")
        elif ev.new_state == "idle":
            print("Agent is ready but not processing")
        elif ev.new_state == "listening":
            print("Agent is listening for user input")
            print("Collected metrics...", current_metrics)
            if current_metrics:
                log_metric(
                    eou_delay=current_metrics.get('eou_delay', 0),
                    ttft=current_metrics.get('ttft', 0),
                    ttfb=current_metrics.get('ttfb', 0),
                    total_latency=current_metrics.get('eou_delay', 0)
                                  + current_metrics.get('ttft', 0)
                                  + current_metrics.get('ttfb', 0)
                )
            current_metrics = {}
        elif ev.new_state == "thinking":
            print("Agent is processing user input and generating a response")
        elif ev.new_state == "speaking":
            print("Agent started speaking")

    @session.on("metrics_collected")
    def on_metrics_collected(ev: MetricsCollectedEvent):
        global current_metrics
        if hasattr(ev.metrics, "type"):
            if ev.metrics.type == "eou_metrics":
                current_metrics['eou_delay'] = ev.metrics.end_of_utterance_delay
                print(f"  ↳ EOU delay: {ev.metrics.end_of_utterance_delay:.3f}s")
            elif ev.metrics.type == "llm_metrics":
                current_metrics['ttft'] = ev.metrics.ttft
                print(f"  ↳ LLM TTFT: {ev.metrics.ttft:.3f}s")
            elif ev.metrics.type == "tts_metrics":
                current_metrics['ttfb'] = ev.metrics.ttfb
                print(f"  ↳ TTFB: {ev.metrics.ttfb:.3f}s")

    async def on_shutdown():
        global current_metrics
        if current_metrics:
            print("Logging final metrics at shutdown:", current_metrics)
            log_metric(
                eou_delay=current_metrics.get('eou_delay', 0),
                ttft=current_metrics.get('ttft', 0),
                ttfb=current_metrics.get('ttfb', 0),
                total_latency=current_metrics.get('eou_delay', 0)
                              + current_metrics.get('ttft', 0)
                              + current_metrics.get('ttfb', 0)
            )
        save_to_excel()

    ctx.add_shutdown_callback(on_shutdown)

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
