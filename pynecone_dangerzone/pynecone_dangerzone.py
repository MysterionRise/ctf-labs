"""Main application entry point"""
import pynecone as pc
import pytz


class State(pc.State):
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1


def index():
    return pc.hstack(
        pc.button(
            "Decrement",
            color_scheme="red",
            border_radius="1em",
            on_click=State.decrement,
        ),
        pc.heading(State.count, font_size="2em"),
        pc.button(
            "Increment",
            color_scheme="green",
            border_radius="1em",
            on_click=State.increment,
        ),
    )


# Endpoint for creating a new event
# @app.route('/events', methods=['POST'])
def create_event():
    # TODO
    # data = request.json
    data = None
    # Get the event details from the request
    event_name = data["event_name"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    participants = data["participants"]

    # Create a new event
    event = pc.create_event(event_name, start_time, end_time)

    # Add participants to the event
    for participant in participants:
        # Get the participant's timezone from the request
        timezone = pytz.timezone(participant["timezone"])

        # Add the participant to the event
        pc.add_participant(event, participant["name"], timezone)

    # Return the event details
    return {
        "event_id": event.event_id,
        "event_name": event_name,
        "start_time": start_time,
        "end_time": end_time,
        "participants": participants,
    }

    # Endpoint for getting the time of an event in a participant's timezone
    # @app.route('/events/<int:event_id>/time', methods=['GET'])


def get_event_time(event_id):
    # TODO
    # data = request.json
    data = None

    # Get the participant's timezone from the request
    timezone = pytz.timezone(data["timezone"])

    # Get the event from the Pynecone instance
    event = pc.get_event(event_id)

    # Get the time of the event in the participant's timezone
    event_time = event.get_time_in_timezone(timezone)

    # Return the event time
    return {
        "event_id": event_id,
        "event_time": event_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
    }


app = pc.App(state=State)
app.add_page(index)
app.compile()
