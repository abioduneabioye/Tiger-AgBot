#!/usr/bin/env python3

import argparse
import asyncio
from pathlib import Path

from numpy import clip

from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.pose_pb2 import Twist2d
from farm_ng.core.proto_util import proto_from_json_file


MAX_LINEAR_VELOCITY_MPS = 0.5
MAX_ANGULAR_VELOCITY_RPS = 0.5
VELOCITY_INCREMENT = 0.5


def update_twist_with_key_press(twist: Twist2d, key: str) -> Twist2d:
    print(f"key = {key}")

    # Reset first (safety)
    twist.linear_velocity_x = 0.0
    twist.linear_velocity_y = 0.0
    twist.angular_velocity = 0.0

    # If empty / unknown -> stop (already zero)
    if key == "":
        twist.linear_velocity_x = 0.0
        twist.linear_velocity_y = 0.0
        twist.angular_velocity = 0.0
        return twist

    # Map single-character commands to velocities
    if key == "w":  # forward
        twist.linear_velocity_x = MAX_LINEAR_VELOCITY_MPS
        twist.angular_velocity = 0.0

    elif key == "s":  # reverse (optional)
        twist.linear_velocity_x = -MAX_LINEAR_VELOCITY_MPS
        twist.angular_velocity = 0.0

    elif key == "a":  # turn left
        twist.linear_velocity_x = MAX_LINEAR_VELOCITY_MPS * 0.5
        twist.angular_velocity = MAX_ANGULAR_VELOCITY_RPS

    elif key == "d":  # turn right
        twist.linear_velocity_x = MAX_LINEAR_VELOCITY_MPS * 0.5
        twist.angular_velocity = -MAX_ANGULAR_VELOCITY_RPS

    elif key == "x":  # stop
        twist.linear_velocity_x = 0.0
        twist.angular_velocity = 0.0

    # Clamp (extra safety)
    twist.linear_velocity_x = float(clip(twist.linear_velocity_x, -MAX_LINEAR_VELOCITY_MPS, MAX_LINEAR_VELOCITY_MPS))
    twist.angular_velocity = float(clip(twist.angular_velocity, -MAX_ANGULAR_VELOCITY_RPS, MAX_ANGULAR_VELOCITY_RPS))

    return twist


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    client: EventClient,
    twist: Twist2d,
) -> None:
    peer = writer.get_extra_info("peername")
    print(f"[Controller] Client connected: {peer}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break

            # Your planner sends single characters like b"w" / b"a" / b"d" / b"x"
            key = data.decode(errors="ignore").strip()

            twist = update_twist_with_key_press(twist, key)

            print(
                "[Controller] Sending twist: "
                f"linear_x={twist.linear_velocity_x:.2f}, "
                f"angular={twist.angular_velocity:.2f}"
            )

            # Publish to Amiga motion interface
            await client.publish("/vehicle/twist", twist)

    except Exception as e:
        print(f"[Controller] Error: {e}")

    finally:
        # Always stop on disconnect (safety)
        try:
            twist.linear_velocity_x = 0.0
            twist.linear_velocity_y = 0.0
            twist.angular_velocity = 0.0
            await client.publish("/vehicle/twist", twist)
        except Exception:
            pass

        print(f"[Controller] Client disconnected: {peer}")
        writer.close()
        await writer.wait_closed()


async def main(service_config_path: Path) -> None:
    config: EventServiceConfig = proto_from_json_file(service_config_path, EventServiceConfig)

    client = EventClient(config=config)
    twist = Twist2d()

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, client, twist),
        host="0.0.0.0",
        port=9999,
    )

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[Controller] Listening on {addrs} for planner connections...")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Farm-NG Amiga TCP controller (w/a/s/d/x -> Twist2d)")
    parser.add_argument(
        "--service-config",
        type=Path,
        required=True,
        help="Path to service_config.json",
    )
    args = parser.parse_args()

    asyncio.run(main(args.service_config))