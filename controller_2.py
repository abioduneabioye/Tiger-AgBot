import asyncio
import argparse
from pathlib import Path

from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.proto_util import proto_from_json_file
from farm_ng.core.pose_pb2 import Twist2d


def update_twist_with_key_press(twist: Twist2d, key: str):
    """
    Update Twist2d velocities based on keyboard command.
    w = forward
    a = turn left
    d = turn right
    x = stop
    """

    if key == "w":
        twist.linear_velocity_x = 0.5
        twist.angular_velocity = 0.0

    elif key == "a":
        twist.linear_velocity_x = 0.2
        twist.angular_velocity = 0.8

    elif key == "d":
        twist.linear_velocity_x = 0.2
        twist.angular_velocity = -0.8

    elif key == "x":
        twist.linear_velocity_x = 0.0
        twist.angular_velocity = 0.0

    else:
        # Unknown key → stop for safety
        twist.linear_velocity_x = 0.0
        twist.angular_velocity = 0.0

    return twist


async def handle_client(reader: asyncio.StreamReader,
                        writer: asyncio.StreamWriter,
                        client: EventClient,
                        twist: Twist2d):

    print("[Controller] Client connected.")

    try:
        while True:

            data = await reader.read(1024)

            if not data:
                break

            command = data.decode().strip()

            # Update twist from command
            twist = update_twist_with_key_press(twist, command)

            print(f"[Controller] Sending twist: "
                  f"linear_x={twist.linear_velocity_x:.2f}, "
                  f"angular={twist.angular_velocity:.2f}")

            # Publish to robot
            await client.publish("/vehicle/twist", twist)

    except Exception as e:
        print(f"[Controller] Error: {e}")

    finally:
        print("[Controller] Client disconnected.")
        writer.close()
        await writer.wait_closed()


async def main(service_config_path: Path):

    # Load farm-ng service config
    config: EventServiceConfig = proto_from_json_file(
        service_config_path,
        EventServiceConfig,
    )

    client = EventClient(config=config)

    twist = Twist2d()

    # Start TCP server
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, client, twist),
        host="0.0.0.0",
        port=9999,
    )

    addr = server.sockets[0].getsockname()

    print(f"[Controller] Listening on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Farm-ng Amiga TCP controller"
    )

    parser.add_argument(
        "--service-config",
        type=Path,
        required=True,
        help="Path to service_config.json"
    )

    args = parser.parse_args()

    asyncio.run(main(args.service_config))