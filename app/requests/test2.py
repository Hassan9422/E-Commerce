import os
from pathlib import Path

print(Path(f"{__file__}/../..").resolve().as_posix())
print(Path(f"{os.path.abspath(__file__)}/../..").resolve().as_posix())
