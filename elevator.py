UP = 1
DOWN = 2
FLOOR_COUNT = 6

class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this is done.
    """

    def __init__(self):
        # Feel free to add any instance variables you want.
        self.destination_floors = []
        self.callbacks = None
        self.direction = None

    def cmp_floors(self, here, there):
        if here < there:
            return UP
        elif here > there:
            return DOWN
    
    def queue_floor(self, floor):
        if len(self.destination_floors) == 0:
            self.direction = None
        if self.direction is not None:
            self.destination_floors.append(floor)
            return
        current_floor = self.callbacks.current_floor
        self.direction = self.cmp_floors(current_floor, floor)
    
    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        self.queue_floor(floor)
        self.destination_floors.append(floor)

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        self.queue_floor(floor)
        self.destination_floors.append(floor)

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        if self.callbacks.current_floor in self.destination_floors:
            self.callbacks.motor_direction = None
            self.destination_floors.remove(self.callbacks.current_floor)

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        if len([floor for floor in self.destination_floors if self.cmp_floors(self.callbacks.current_floor, floor) == self.direction]) == 0:
            self.direction = None
        self.callbacks.motor_direction = self.direction