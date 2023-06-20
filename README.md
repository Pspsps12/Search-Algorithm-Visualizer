 # Search Algorithm Visualizer
    #### Video Demo:  https://youtu.be/61qOJQTUSNg
    #### Description:
        This project was created in order to demonstrate how some search algorithms work while allowing the user to interactively play with them in a fun way.
        This program was made using pygame.

        When the user first opens the program, they will see four buttons on the left, each representing a different searching algorithm, and a large square on the right. In that square, the user can draw a maze by holding down the left mouse button on one of the uncolored squares and dragging the mouse. To make a square a square empty again, the user should press the mouse button on a black square and then drag the mouse. The light green is the start of the maze, and the dark green is the end of the maze. Black squares are walls, and white squares are empty. When selecting one of the four algorithms the program will try to find a path from the start to the end. When the program “visits” a square, it turns light blue. When / if the program finds a path from the start to the end, it colors the path orange. 

        The four searching algorithms:
        Breadth-first search - expands in all directions. Always finds the shortest solution, but takes the most amount of steps to find it.
        Depth First Search - takes a path randomly. Sometimes it finds a solution fast, sometimes slowly, but the solution is likely to take a lot of steps.
        Greedy Best First Search - goes to the square that is the closest to the end (using Manhattan distance). Tends to find a solution relatively fast, but the shortest solution is not guaranteed.
        A* search - expands towards the end. This algorithm is guaranteed to find the fastest solution, but it also tends to take many steps. This algorithm is the best combination of speed and solution length (if the end position is known).
