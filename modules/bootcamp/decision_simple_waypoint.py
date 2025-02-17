"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.has_sent_landing_command = False
        self.command_index = 0
        

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        Make the drone fly to the waypoint.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...
        self.commands = [
            commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - report.position.location_x, 
                self.waypoint.location_y - report.position.location_y)
        ]

        self.has_sent_landing_command = False
        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(self.commands):
            command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            # land if distance to landing pad location is wtihin acceptance_radius
            distance = (self.waypoint.location_x - report.position.location_x)**2 + (self.waypoint.location_y - report.position.location_y)**2
            if distance <= self.acceptance_radius**2:
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True
            else:
                comamnd = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x, 
                    self.waypoint.location_y - report.position.location_y
                )
                
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
