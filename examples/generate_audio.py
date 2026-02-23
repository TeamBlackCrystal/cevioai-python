"""Generate speech audio with CeVIO AI RemoteService2."""

from cevioai_python.cevioai_control import ServiceControl2, Talker2


def main() -> None:
    # If CeVIO AI is not installed in the default path, set install_dir or dll_path.
    # install_dir = r"C:\Program Files\CeVIO\CeVIO AI"
    install_dir = None

    # Start CeVIO AI if it is not running.
    result = ServiceControl2.start_host(no_wait=False, install_dir=install_dir)
    print(f"StartHost: {result.name}")

    talker = Talker2(install_dir=install_dir)

    # Optionally choose a cast.
    available = Talker2.available_casts(install_dir=install_dir)
    print("Available casts:", available)
    talker.cast = available[0]

    # Basic parameters (0-100).
    talker.volume = 100
    talker.speed = 50
    talker.tone = 80
    talker.alpha = 50
    talker.tone_scale = 50

    text = "Hello from CeVIO AI."
    output_path = "output.wav"

    ok = talker.output_wave_to_file(text, output_path)
    print(f"OutputWaveToFile: {ok} -> {output_path}")


if __name__ == "__main__":
    main()
