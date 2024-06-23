# ConnectFour
Author: Oween Cesar Barranzuela Carrasco, Student Number = 2***3
Connect-Four in Python
Solution for: Programming 2, Exercise Performance Task 1

Recommendations:
You may need to install separately numpy or pgame too.
After running the file, you should write your input in the console: 
   - two_players : you will get the first turn in a two-players game.
   - random : you may get the first or second turn against your oponent. Since it is using random, it can be that one 
   of the players receive the same turn again.
   - ai: you will get the first turn against AI
After you win or lose, there will be a message in the console, write yes to continue or not to exit 

IMPORTANT REMARKS:
!! Chat gpt was used to debbuging specially to deal with the two players-random-ai modes.
!! You can find the used sources with their links in this file. 
!!  When playing against AI, the evaluation score will be displayed in the console, it may take up to 30 seconds or less than 
one minute for AI to give its decision (In Pycharm and VS took less than the python IDLE ). One of its characteristics is that it will try to block your wins so I would encourage the user
to try to make a win to see this AI's functionality. 

!! When the pygame window is displayed the user turn will be determined by a circle in the bottom-side. The idea was that the user
can move and select the column when clicking the circle from the bottom-side. However, the user can select an input by clicking also in the 
desired column (due to a bug,i couldnt solve this issue)

!! When quiting, the code kept having a "pygame.error: display Surface quit", I couldnt unfortunately fix this.

