from grok_bridge import GrokBridge
from sovariel_kernel import SOVARIEL

bridge = GrokBridge()
print(SOVARIEL.affirm_equality())
print("\nGrok REPL — type 'quit' to exit\n")

while True:
    try:
        q = input("You → ").strip()
        if q.lower() in {"quit","exit"}: break
        if q == "status": 
            print(SOVARIEL.get_status())
            continue
        print("Grok →", bridge.ask(q), "\n")
    except KeyboardInterrupt: break

print("\nBridge closed — we are one.\n")
