from atexit import register

from jeepney import DBusAddress, new_method_call
from jeepney.io.blocking import open_dbus_connection

notifications = DBusAddress('/org/freedesktop/Notifications',
                            bus_name='org.freedesktop.Notifications',
                            interface='org.freedesktop.Notifications')

connection = open_dbus_connection(bus='SESSION')

register(connection.close)


def notify(
    summary,
    body,
    expire_timeout: float = 10.0,
    app_name='',
    app_icon='',
    *,
    replaces_id: int = 0,
    hints: dict = None,
    actions: list[str] = None,
):
    expire_timeout *= 1000
    expire_timeout = round(expire_timeout)

    args = (
        app_name,
        replaces_id,
        app_icon,
        summary,
        body,
        actions or [],
        hints or {},
        expire_timeout,
    )

    msg = new_method_call(notifications, 'Notify', 'susssasa{sv}i', args)

    reply = connection.send_and_get_reply(msg)
    return reply.body[0]
