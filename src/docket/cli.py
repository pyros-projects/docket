import sys


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--version"]:
        from docket import __version__
        print(f"docket {__version__}")
        return 0
    print("docket: no command given (try: docket status)", file=sys.stderr)
    return 2


def entry() -> None:  # console-script shim
    raise SystemExit(main())
