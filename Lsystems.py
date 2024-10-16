import matplotlib.pyplot as plt
import numpy as np

LINDENMAYER_SYSTEMS = {

    "Koch curve": {
        "init": "S",
        "rules": {
            "S": "SLSRSLS",
            "L": "L",
            "R": "R",
        },

        "forward": ["S"],
        "left": ["L"],
        "right": ["R"],
        "scale": 3,
        "angle": {
            "left": (np.pi / 3),
            "right": -((2 * np.pi) / 3),
        },
    },

    "Sierpinski triangle": {
        "init": "A",
        "rules": {
            "A": "BRARB",
            "B": "ALBLA",
            "L": "L",
            "R": "R",
        },
        "forward": ["A", "B"],
        "left": ["L"],
        "right": ["R"],
        "scale": 2,
        "angle": {
            "left": (np.pi / 3),
            "right": -(np.pi / 3),
        },
    },
}

def LindIter(system, N):
    """Calculate N iterations of the system
    Parameters
    ----------
    system : str
        A string containing the name of the L-System for calculation
    N : int
        The number of iterations that should be calculated
    Returns
    -------
    str
        A string containing the output after N iterations of the chosen L-System
    """

    # Get the initial string for selected L-System
    lindenmayerString = LINDENMAYER_SYSTEMS[system]["init"]
    for _ in range(N):
        # Get replacement rules for selected L-System
        rules = LINDENMAYER_SYSTEMS[system]["rules"]

        # First let us prepare a translation table based on our rules using str.maketrans funcion
        # See: https://docs.python.org/3/library/stdtypes.html#str.maketrans

        translate_table = lindenmayerString.maketrans(rules)

        # Then pass the translation table to the translate function which will produce a string with replaced symbols
        # Just what we want! Simple and easy!
        # See: https://docs.python.org/3/library/stdtypes.html#str.translate
        lindenmayerString = lindenmayerString.translate(translate_table)
    return lindenmayerString


#   Requirements for this function are not clear, therefore we decided to take MVP approach here to design solutions for cases from project requirements
#   This might not work for all existing L-Systems
def turtleGraph(lindenmayerString, system, N):
    """Calculate N iterations of the system
    Parameters
    ----------
    lindenmayerString : str
        A string containing the output after N iterations of the chosen L-System
    system : str
        String containing the name of the L-System for calculation
    N : int
        The number of iterations that should be calculated
    Returns
    -------
    numpy.array
        A row vector containing the turtle graphics commands consisting of alternating length and angle specifications
    """

    # Length of the line is constant for all turtle commands
    length = 1 / (LINDENMAYER_SYSTEMS[system]["scale"] ** N)
    # For cases in this specific project, the first command is always a move forward with a 0 angle
    turtleCommands = [length, 0]
    # Simple assert just to make sure our assumption is true
    assert lindenmayerString[0] in LINDENMAYER_SYSTEMS[system]["forward"]
    # Skip the first element due to our assumption
    for symbol in lindenmayerString[1:]:
        # For cases in this specific project, the angle command is always before moving forward
        # We can just find all the angles and based on them construct pair of the length and angle

        if symbol in LINDENMAYER_SYSTEMS[system]["left"]:
            angle = LINDENMAYER_SYSTEMS[system]["angle"]["left"]
            turtleCommands += [length, angle]
        elif symbol in LINDENMAYER_SYSTEMS[system]["right"]:
            angle = LINDENMAYER_SYSTEMS[system]["angle"]["right"]
            turtleCommands += [length, angle]
    return np.array(turtleCommands)


def turtlePlot(turtleCommands, system):
    """Calculate N iterations of the system
    Parameters
    ----------
    turtleCommands : numpy.array
        A row vector containing the turtle graphics commands consisting of alternating length and angle specifications
    system : str
        A string containing the name of the L-System for calculation

    Returns
    -------
    None
    """

    # Initial d and x vectors
    d = np.array([1, 0])
    x = np.array([0, 0])
    # Reshape input vector to 2D array
    # It is easier to work on 2D array as a list of length and angle pairs than 1D row vector
    commands = np.reshape(turtleCommands, (len(turtleCommands) // 2, 2))
    # Create data array for turtle plot with a starting point in (0,0)
    turtle = np.array(x)
    # For every pair of the length and angle, calculate the next point to draw
    for length, angle in commands:
        # 2D.1 equation from the project description
        mod = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        d = np.dot(mod, d)
        # 2D.2 equation from the project description
        x = x + length * d
        # Add point to the data array
        turtle = np.vstack((turtle, x))

    # Draw plot, limit x-axis 0-1, add title
    plt.xlim([0, 1])
    plt.title(f"L-System: {system}")
    plt.plot(turtle[:, 0], turtle[:, 1])
    plt.show()

# Simple tests just for the development process
# To be removed
assert LindIter("Koch curve", 0) == "S"
assert LindIter("Koch curve", 1) == "SLSRSLS"
assert LindIter("Koch curve", 2) == "SLSRSLSLSLSRSLSRSLSRSLSLSLSRSLS"
assert (
    LindIter("Koch curve", 3)
    == "SLSRSLSLSLSRSLSRSLSRSLSLSLSRSLSLSLSRSLSLSLSRSLSRSLSRSLSLSLSRSLSRSLSRSLSLSLSRSLSRSLSRSLSLSLSRSLSLSLSRSLSLSLSRSLSRSLSRSLSLSLSRSLS"
)

assert LindIter("Sierpinski triangle", 0) == "A"
assert LindIter("Sierpinski triangle", 1) == "BRARB"
assert LindIter("Sierpinski triangle", 2) == "ALBLARBRARBRALBLA"
assert LindIter("Sierpinski triangle", 3) == "BRARBLALBLALBRARBRALBLARBRARBRALBLARBRARBLALBLALBRARB"

# Creating menu
def get_iteration(range):
    """ Get number of iteration from the user
    Parameters
    ----------
    range : tuple
        A tuple with allowed range for user input - (min, max)
    Returns 
    -------
    int
        Number of iteration
    """
    info = f"""
Choose an iteration ({range[0]} to {range[1]}):
Please enter how many iterations you would like to be displayed:"""
    while True: # Loop for iterations of Koch Curve.
        try:
            iteration = int(input(info))
            if (iteration<range[0]) or (iteration>range[1]):
                raise ValueError #If there is an error exit the try block and execute the except block
            break
        except: # Handle/print the error and loop back to "try"
            print ("--------------------------------------")
            print(f"You have selected an option outside of defined range, Please choose an iteration within the limits {range[0]} to {range[1]}. ")
    return iteration

choice = ""
b=False
while(True):  #Loop forever for the main script until break.
    # Front page of the program when running.
    s = """
Which step would you like to pick?:
    1) Choose type of Lindenmayer system and the number of iterations
    2) Generate plots
    3) Quit
Entered choice:"""
    choice=input(s) # Put "s" int choice
    choice =choice.strip() # .strip removes any leading (spaces at the beginning)
    # And trailing (spaces at the end) characters (space is the default leading character to remove).
    if (choice=="1"): # Choosing option 1.
        b = True # This is to check if option 1 is chosen before option 2.
        # "w" is the display shown when the user chose option 1.
        w = """
Please choose the curve you'd like to display:
    1) Koch curves
    2) Sierpinski Triangle
Please enter the number of curves you'd like to continue with:"""
        choice2 = input(w) # Put w int choice 2.
        choice2 =choice2.strip() # .strip removes any leading (spaces at the beginning)
        # And trailing (spaces at the end) characters (space is the default leading character to remove)
        while True: # Keep looping until break for choice 1 in Koch curve.
            try: # Allowing to test the code for input errors.
                if choice2=="1": #Choosing Koch curve.
                    INPUT_SYSTEM = "Koch curve"
                    INPUT_N = get_iteration((0,5))
                    break
                elif choice2 == "2": # Choosing Sierpinkski triangle
                    INPUT_SYSTEM = "Sierpinski triangle"
                    INPUT_N = get_iteration((0,8))
                    break
                else:
                    raise ValueError # If there error, exit the try block and execute the except block.
                break
            except: # Loop here when after choosing option 1, user did not choose Koch or Sierpinski.
                # It will liip to the main page.
                print ("")
                print("-----------------------------------------")
                print("You have selected an option outside of defined range. You are redirected to the main menu, Please try again.")
            break


    elif(choice=="2"):
        if b == True: # To ensure that the user has input option 1 before option 2.
            lindenmayerString = LindIter(INPUT_SYSTEM, INPUT_N)
            turtleCommands = turtleGraph(lindenmayerString, INPUT_SYSTEM, INPUT_N)
            turtlePlot(turtleCommands, INPUT_SYSTEM)

        else: # If the user has not input option 1, it will loop into here.
            print ("")
            print("-----------------------------------------")
            print("Please try again and choose option 1 to define the input.")



    elif(choice=="3"):# Break/quit program.
        break

    else:# If the user keyed in any number either then 1,2 0r 3 loop into here.
        print("")
        print("-----------------------------------------")
        print ("Please try again entering a valid number from 1 to 3.")
