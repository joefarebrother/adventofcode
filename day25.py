from intcode import *
from utils import *

Machine("input25", ascii_input, ascii_output).run()


'''
Transcript:


== Hull Breach ==
You got in through a hole in the floor here. To keep your ship from also freezing, the hole has been sealed.

Doors here lead:
- north
- south
- west

Command?
south



== Holodeck ==
Someone seems to have left it on the Giant Grid setting.

Doors here lead:
- north
- west

Items here:
- infinite loop

Command?
west



== Corridor ==
The metal walls and the metal floor are slightly different colors. Or are they?

Doors here lead:
- north
- east

Command?
north



== Crew Quarters ==
The beds are all too small for you.

Doors here lead:
- south
- west

Items here:
- fuel cell

Command?
take fuel cell

You take the fuel cell.

Command?
south



== Corridor ==
The metal walls and the metal floor are slightly different colors. Or are they?

Doors here lead:
- north
- east

Command?
east



== Holodeck ==
Someone seems to have left it on the Giant Grid setting.

Doors here lead:
- north
- west

Items here:
- infinite loop

Command?
north



== Hull Breach ==
You got in through a hole in the floor here. To keep your ship from also freezing, the hole has been sealed.

Doors here lead:
- north
- south
- west

Command?
north



== Stables ==
Reindeer-sized. They're all empty.

Doors here lead:
- north
- east
- south

Items here:
- escape pod

Command?
east



== Gift Wrapping Center ==
How else do you wrap presents on the go?

Doors here lead:
- north
- south
- west

Items here:
- candy cane

Command?
take candy cane

You take the candy cane.

Command?
north



== Sick Bay ==
Supports both Red-Nosed Reindeer medicine and regular reindeer medicine.

Doors here lead:
- south

Items here:
- photons

Command?
north

You can't go that way.

Command?
south



== Gift Wrapping Center ==
How else do you wrap presents on the go?

Doors here lead:
- north
- south
- west

Command?
south



== Engineering ==
You see a whiteboard with plans for Springdroid v2.

Doors here lead:
- north
- east

Items here:
- hypercube

Command?
take hypercube

You take the hypercube.

Command?
east



== Passages ==
They're a little twisty and starting to look all alike.

Doors here lead:
- west

Command?
west



== Engineering ==
You see a whiteboard with plans for Springdroid v2.

Doors here lead:
- north
- east

Command?
north



== Gift Wrapping Center ==
How else do you wrap presents on the go?

Doors here lead:
- north
- south
- west

Command?
north



== Sick Bay ==
Supports both Red-Nosed Reindeer medicine and regular reindeer medicine.

Doors here lead:
- south

Items here:
- photons

Command?
south



== Gift Wrapping Center ==
How else do you wrap presents on the go?

Doors here lead:
- north
- south
- west

Command?
west



== Stables ==
Reindeer-sized. They're all empty.

Doors here lead:
- north
- east
- south

Items here:
- escape pod

Command?
east



== Gift Wrapping Center ==
How else do you wrap presents on the go?

Doors here lead:
- north
- south
- west

Command?
north



== Sick Bay ==
Supports both Red-Nosed Reindeer medicine and regular reindeer medicine.

Doors here lead:
- south

Items here:
- photons

Command?
south



== Gift Wrapping Center ==
How else do you wrap presents on the go?

Doors here lead:
- north
- south
- west

Command?
west



== Stables ==
Reindeer-sized. They're all empty.

Doors here lead:
- north
- east
- south

Items here:
- escape pod

Command?
north



== Observatory ==
There are a few telescopes; they're all bolted down, though.

Doors here lead:
- east
- south
- west

Items here:
- coin

Command?
take coin

You take the coin.

Command?
west



== Arcade ==
None of the cabinets seem to have power.

Doors here lead:
- north
- east
- south

Items here:
- spool of cat6

Command?
take spool of cat6

You take the spool of cat6.

Command?
west

You can't go that way.

Command?
east



== Observatory ==
There are a few telescopes; they're all bolted down, though.

Doors here lead:
- east
- south
- west

Command?
east



== Hallway ==
This area has been optimized for something; you're just not quite sure what.

Doors here lead:
- west

Items here:
- tambourine

Command?
take tambourine

You take the tambourine.

Command?
west



== Observatory ==
There are a few telescopes; they're all bolted down, though.

Doors here lead:
- east
- south
- west

Command?
west



== Arcade ==
None of the cabinets seem to have power.

Doors here lead:
- north
- east
- south

Command?
north



== Navigation ==
Status: Stranded. Please supply measurements from fifty stars to recalibrate.

Doors here lead:
- south
- west

Items here:
- weather machine

Command?
take weather machine

You take the weather machine.

Command?
west



== Hot Chocolate Fountain ==
Somehow, it's still working.

Doors here lead:
- east
- west

Items here:
- mutex

Command?
take mutex

You take the mutex.

Command?
west 



== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- east
- west

Command?
inv

Items in your inventory:
- spool of cat6
- hypercube
- weather machine
- coin
- candy cane
- tambourine
- fuel cell
- mutex

Command?
west



== Pressure-Sensitive Floor ==
Analyzing...

Doors here lead:
- east

A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.



== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- east
- west

Command?
inv

Items in your inventory:
- spool of cat6
- hypercube
- weather machine
- coin
- candy cane
- tambourine
- fuel cell
- mutex

Command?
drop coin

You drop the coin.

Command?
west



== Pressure-Sensitive Floor ==
Analyzing...

Doors here lead:
- east

A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.



== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- east
- west

Items here:
- coin

Command?
drop candy cane

You drop the candy cane.

Command?
west



== Pressure-Sensitive Floor ==
Analyzing...

Doors here lead:
- east

A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.



== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- east
- west

Items here:
- coin
- candy cane

Command?
drop weather machine

You drop the weather machine.

Command?
west



== Pressure-Sensitive Floor ==
Analyzing...

Doors here lead:
- east

A loud, robotic voice says "Alert! Droids on this ship are heavier than the detected value!" and you are ejected back to the checkpoint.



== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- east
- west

Items here:
- weather machine
- coin
- candy cane

Command?
take weather machine

You take the weather machine.

Command?
drop spool of cat6

You drop the spool of cat6.

Command?
west



== Pressure-Sensitive Floor ==
Analyzing...

Doors here lead:
- east

A loud, robotic voice says "Alert! Droids on this ship are heavier than the detected value!" and you are ejected back to the checkpoint.



== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- east
- west

Items here:
- spool of cat6
- coin
- candy cane

Command?
take spool of cat6

You take the spool of cat6.

Command?
west



== Pressure-Sensitive Floor ==
Analyzing...

Doors here lead:
- east

A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.



== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- east
- west

Items here:
- coin
- candy cane

Command?
drop mutex

You drop the mutex.

Command?
west



== Pressure-Sensitive Floor ==
Analyzing...

Doors here lead:
- east

A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.



== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- east
- west

Items here:
- coin
- candy cane
- mutex

Command?
drop fuel cell

You drop the fuel cell.

Command?
west



== Pressure-Sensitive Floor ==
Analyzing...

Doors here lead:
- east

A loud, robotic voice says "Analysis complete! You may proceed." and you enter the cockpit.
Santa notices your small droid, looks puzzled for a moment, realizes what has happened, and radios your ship directly.
"Oh, hello! You should be able to get in by typing 84410376 on the keypad at the main airlock."

'''


