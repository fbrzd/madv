# MAdv
"Minimalist Adventure"

## How play
* Run it with "python3 adv.py".
* MAdv will search your name in "saves" file and try load your data.
* Interact via commands (cmds from now): __see__, __mov__, __chg__, __run__, __q__ and __empty command__.
* Colored and formated text (on terminal) show the information will you need.
* Saves automatically when input cmd __q__.

## What means what?
__All is registred via _items___. sword means "force" or "work", not literally a sword; book means "wisdom" or "tricks" not only a book. Either, these are consumed, so _item_ is a properly term.

You will move cross zones and only exists two types:
- Towns: For enter you will need _"taxes"_, N items defined in "data file". Here can change (__chg__ cmd) items randomly.
- Dungeons: Here will appears N events, and the player will try automatically use any item to overcome it; you have a limit of items that you can charge.

 In both, you can use a __empty cmd__ for a zone's description, look for all available zones and see what items you have or __mov__ for try move to other zone. Quit with __q__ will save your current position and items.

If you want edit the context of game (names, weakness, meta), "dq1" is a directoy's exmaple for a minimalist version of dragon quest 1.

Some details are omited (probability, event's weak are only one, etc)

## Tool
If you want a vision of your "data" file, can use _tool.py_, this is a module what summarize:
- balance of items in a dungeon, based on events that give items or not. flag __-d__.
- item's "price", with means computing of taxes in town where be changes. flag __-i__.
- event's frequency, count in all dungeons, all events. flag __-e__.

## Future Features
- Better customization via extern files.
- Procedural generation.
- Ascci Art
- Better math tool for analisis of data game