# MAdv
"Minimalist Adventure". A text-based adventure, with very minimalist rules. Useful for write scenearios.

## How play
* Run it with "python3 front.py".
* MAdv will search your name in "saves" file and try load your data.
* Many times you will have to choice a "class", wich define your inital items, max-hp & max-capacity
* Interact via commands (cmds from now): __mov__, __chg__, __rol__, __q__ and __empty command__.
* Colored and formated text (on terminal) show the information will you need.
* Saves automatically when input cmd __q__.

## What means what?
You will move cross zones and only exists two types:
- Towns: For enter you will need _"taxes"_, N items defined in "data file". Here can change (__chg__ cmd) items randomly.
- Dungeons: Here will appears N events, and the player will try automatically use any item to overcome it; you have a limit of items that you can charge.

In both, you can use a __empty cmd__ for a zone's description, look for all available zones and see what items you have. Also __mov__ for try move to other zone. Quit with __q__ will save your current position and items & show some advice about that context (events, zones, etc).

## Goals & Turns
"Goals" are defined in "data file", this can be overcome events, collect items, etc. For self challenge also register number of _"turns"_, this is how many times you has mov cross zones. Both information is showed with __rol__ cmd.

Some details are omited (probability, event's weak are only one, etc)

## Make & Tool
You can edit the context of game (names, weakness, meta), "exp/" is a directoy with exmaple's folders (many based on dragon quest).

If you want a vision of your "data" file, can use _tool.py_, this is a module what summarize:
- balance of items & hp in a dungeon, based on events that give items and hp's restore. flag __-d__.
- item's "price", with means computing of taxes in town where be changes. flag __-i__.
- event's frequency, count in all dungeons, all events. flag __-e__.

## Future Features
- Procedural generation.
- Ascci Art