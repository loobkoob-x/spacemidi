"""
list_ports.py — List available MIDI output ports.
Use this to find the correct midi_output_id for config.json.
"""

import pygame.midi

pygame.midi.init()

print("\nAvailable MIDI output ports:\n")
for i in range(pygame.midi.get_count()):
    info = pygame.midi.get_device_info(i)
    interface, name, is_input, is_output, is_open = info
    if is_output:
        print(f"  ID {i} → {name.decode()} {'(open)' if is_open else ''}")

print()
pygame.midi.quit()
