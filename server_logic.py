import random
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def avoid_board_edge(board_height: int, board_width: int, my_head: Dict[str, int], possible_moves: List[str]) -> List[str]:
    if my_head["x"] == board_width - 1:
        possible_moves.remove("right")
    
    if my_head["x"] == 0:
        possible_moves.remove("left")
    
    if my_head["y"] == board_height - 1:
        possible_moves.remove("up")
    
    if my_head["y"] == 0:
        possible_moves.remove("down")

    return possible_moves

def avoid_my_body(my_head: Dict[str, int], my_body: List[Dict[str, int]], possible_moves: List[str]) -> List[str]:
    if { "x": my_head["x"] + 1, "y": my_head["y"] } in my_body:
        possible_moves.remove("right")

    if { "x": my_head["x"] - 1, "y": my_head["y"] } in my_body:
        possible_moves.remove("left")

    if { "x": my_head["x"], "y": my_head["y"] + 1 } in my_body:
        possible_moves.remove("up")

    if { "x": my_head["x"], "y": my_head["y"] - 1 } in my_body:
        possible_moves.remove("down")

    return possible_moves

def avoid_bad_objects(my_head: Dict[str, int], hazards: List[Dict[str, int]], possible_moves: List[str]) -> List[str]:
    if { "x": my_head["x"] + 1, "y": my_head["y"] } in hazards:
        possible_moves.remove("right")

    if { "x": my_head["x"] - 1, "y": my_head["y"] } in hazards:
        possible_moves.remove("left")

    if { "x": my_head["x"], "y": my_head["y"] + 1 } in hazards:
        possible_moves.remove("up")

    if { "x": my_head["x"], "y": my_head["y"] - 1 } in hazards:
        possible_moves.remove("down")

    return possible_moves

def move_if_food(my_head: Dict[str, int], food: List[Dict[str, int]], possible_moves: List[str]) -> List[str]:
    food_moves: List[str] = []

    if { "x": my_head["x"] + 1, "y": my_head["y"] } in food:
        food_moves.append("right")

    if { "x": my_head["x"] - 1, "y": my_head["y"] } in food:
        food_moves.append("left")

    if { "x": my_head["x"], "y": my_head["y"] + 1 } in food:
        food_moves.append("up")

    if { "x": my_head["x"], "y": my_head["y"] - 1 } in food:
        food_moves.append("down")
    
    if len(food_moves) > 0:
        return food_moves
    else:
        return possible_moves

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    # Don't let our snake move off the board
    board_height = data["board"]["height"]
    board_width = data["board"]["width"]

    possible_moves = avoid_board_edge(board_height, board_width, my_head, possible_moves)

    # Don't let our snake hit it's own body
    possible_moves = avoid_my_body(my_head, my_body, possible_moves)

    # Don't let our snake hit other objects
    hazards: List[Dict[str, int]] = data["board"]["hazards"]

    for snake in data["board"]["snakes"]:
        hazards.append(snake["head"])
        hazards.extend(snake["body"])

    possible_moves = avoid_bad_objects(my_head, hazards, possible_moves)

    # Move towards food if present
    possible_moves = move_if_food(my_body, data["board"]["food"], possible_moves)

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
