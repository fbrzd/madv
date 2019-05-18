# MAdv
"Minimalist Adventure"

## How play
* Run it with "python3 adv.py".
* MAdv will search your name in "saves" file and try load your data.
* Interact via commands (cmds from now): __see__, __mov__, __chg__, run, __q__ and __empty command__.
* Colored and formated text (on terminal) show the information will you need.
* Saves automatically when input cmd __q__.

## What means what?
__All is registred via _items___. sword means "force" or "work", not literally a sword; book means "wisdom" or "tricks" not only a book. Either, these are consumed, so _item_ is a properly term.

Only exists two types of zones: towns and dungeons. In both, you can __see__ for a zone's description, __mov__ for move to other zone or use __empty cmd_ for view all zones available; only in towns you can change items (cmd __chg__) randomly, because not ever find the best trade.

Basically, the game has two modes: _"in zone"_ and _"dungeon/travel"_. When you arrive to a town or just completed a dungeon, you be _"in zone"_, can __see__, __mov__, __chg__ (if the zone is a town), use a __empty cmd__ and __q__ (quit & save).

When you will __mov__ to other zone, you will be in _"dungeon"_ (if your destiny is a dungeon) or _"travel"_ (if your destiny is a town); both are identical, but complete the "dungeon" state will reward you. _"dungeon/travel"_ consists in x random _events_ where only can use a __empty cmd__ to try win the event with any _item_ in your bag, or __run__ and back on step in the _"travel/dungeon"_.

Some details are omited (probability, event's weak are only one, "time" variable for future extras, stc-adv file for load & customize the game)

## Future Features
- Music, very son.
- Better customization via extern files.
- Procedural generation.
- Real use for time variable and lvl in travels.
