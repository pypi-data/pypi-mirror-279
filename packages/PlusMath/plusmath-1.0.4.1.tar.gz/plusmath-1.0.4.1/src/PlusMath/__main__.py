import sys

version = "1.0.4.1"

if __name__ == "__main__":
    if [s for s in sys.argv if s in ['-v', '-version']]:
        print(f"PlusMath, version: {version}")
