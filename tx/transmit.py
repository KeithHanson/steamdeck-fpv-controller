import micropython
import select
import sys

while True:
  while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:        
    line = sys.stdin.readline().strip()
    print("Got line " + line)
