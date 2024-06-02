import machine
import time

# Simple hack to allow normal micropython serial comms 
# while still utilizing the same serial comm for other things.

# This is the PRG button
prg_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

# By default, we want to run the main program
run_transmit = True

# Give the programmer 10 seconds to hold the button
for i in range(10):
    if not prg_button.value():
        # button pressed
        print("PRG BUTTON PRESSED. NOT RUNNING TRANSMIT!")
        run_transmit = False
        break
    else:
        print(f"WAITING ({i}): BUTTON NOT PRESSED.")

    time.sleep(1)

# If the button was pressed, this will be false. Otherwise, proceed.
if run_transmit:
    import transmit
    transmit.main()
