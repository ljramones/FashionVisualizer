from backend.app.contracts import SystemCapabilities


def get_system_capabilities() -> SystemCapabilities:
    """Return conservative placeholder capabilities until engines are installed."""

    return SystemCapabilities()
