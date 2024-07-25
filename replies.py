def start_response() -> str:
    return (
        "Hi, I am engrmark. What can I help you with?\n"
        "A. Tell me about Teamflow.\n"
        "B. How can I register for Teamflow.\n"
        "C. Help me with Teamflow support contact.\n"
        "D. Exit"
    )


def pick_response(command: str, LINK: str) -> str:
    responses = {
        "A": response_A(),
        "B": response_B(LINK),
        "C": response_C(),
        "D": "Goodbye!"
    }
    # Return the corresponding response or the start message for invalid commands
    return responses.get(command, start_response())


def response_A() -> str:
    return (
        "Teamflow is a platform that helps you manage your team. "
        "You can use it for team and project management, real-time communication, "
        "document sharing, and collaboration."
    )


def response_B(LINK: str) -> str:
    return (
        f"To register for Teamflow, visit the link below to create an account:\n"
        f'<a href="{LINK}">Teamflow</a>'
    )


def response_C() -> str:
    return (
        "Please contact the Teamflow support team:\n"
        "Email: support@teamflow.com\n"
        "Phone: +234 818 000 0000"
    )
