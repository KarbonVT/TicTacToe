def interpret(speech2txt):
    """
    Take converted text from OpenAI API and translate into tic-tac-toe board commands
    """
    x_coord = None
    y_coord = None
    speech2txt = speech2txt.upper()
    if "TOP" in speech2txt:
        y_coord = 0
    elif "BOT" in speech2txt:
        y_coord = 2
    elif "M" in speech2txt:
        y_coord = 1

    if "LEFT" in speech2txt:
        x_coord = 0
    elif "RIGHT" in speech2txt:
        x_coord = 2
    elif "M" in speech2txt:
        x_coord = 1

    print(speech2txt)
    print(x_coord, y_coord)
    return x_coord, y_coord