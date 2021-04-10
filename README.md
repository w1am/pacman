**PyGame Pacman**
Pacman is a 1980s video game in which the player controls a yellow circular character through a maze in order to avoid being trapped by four hunting ghosts with different attack strategies. The goal is to get the highest score possible by collecting pellets, which can occasionally be used as power-ups.
![enter image description here](https://i.imgur.com/CYrtOh5.png)

**Installations**
| Package | Version |
|--|--|
| PyGame | 2.0.0 |

    py -m pip install -U pygame=2.0.0 --user
    
**Implementation**
The entire game was designed using the PyGame GUI module, which was assessed based on the Pacman game's various criteria and requirements. Our core GUI library had to run across multiple platforms and operating systems, be fast enough, and adhere to our programming style. It was observed that the object-oriented approach will be better for us because it helps us to build modular designs and makes software maintenance easier to manage in future updates. In terms of storage, we wanted something simple and quick. We found that pickle would be optimal for storing Python objects in a byte stream. It allows us to store and easily update data while the game is running.

**Ghost Patterns**
Each ghost has a unique method for capturing Pacman. To see the grid and target lines. set **DEBUG** to True
![enter image description here](https://i.imgur.com/Oz5NZY9.png)

**Player Class**
|Method| Description |
|--|--|
| resetPacman | Reset pacman’s position |
| getSurrounds | Indexes one block away from the character |
| move | Move the character |
| control | Sprite animation and collision detection |

**Enemy Class**
|Method| Description |
|--|--|
| toggleRelease | Release ghost from cage |
| resetGhost | Reset ghost position |
| resetCharacters | Reset all of the game's characters |
| eat | Action taken after the ghost eats Pacman, or vice versa |
| scatter | Distribute ghosts to their assigned scattering points |
| chase | Chase mode |
| pointTo | Point to the desired location on the map |

**Game Class**
|Method| Description |
|--|--|
| setIndex | Index setter method when pacman steps on tile |
| generateSprite |Create the corresponding sprite for each character movement. |
| animateText |Blink text animation when level increases|
| updateLevel | Update level|
| startScreen | Start menu screen / pause screen|
| gameOverEndScreen | Game over screen|
| walkCharacters | Walk characters after key arrow presses|
| generatePellets | Generate pellets when game initiates|
| drawPlayer|Draw player on screen|
| drawGhost|Draw ghost on screen|
| displayStatus|Generate text at center of screen|
| displayNumbers |Display scores, level and remaining lives at the bottom|
| initialize |Initialize the game|
| startGame |Start the game and elease the ghosts.|

**Future Work**
 - Multiplayer Option
- Increase the difficulty as the player progresses	
- Create new maps for each level
- Organize the codes even more
