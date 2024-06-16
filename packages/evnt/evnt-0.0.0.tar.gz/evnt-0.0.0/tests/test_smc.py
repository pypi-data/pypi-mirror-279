import sys
import quakeio
from quakeio.parse.smc import read_event


filename = "dat/LomaPrieta_17Oct1989_NP01103P.smc.zip"

if len(sys.argv) > 1:
    filename = sys.argv[1]

event = quakeio.read(filename, parser="smc.read_event")

print(event)


for m in event.motions.values():
    print(m)
    for c in m.components.values():
        print("    ", c)

