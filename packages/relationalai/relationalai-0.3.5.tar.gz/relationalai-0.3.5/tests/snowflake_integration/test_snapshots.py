from pathlib import Path

from relationalai.clients import config as cfg
from tests.util import all_files_in_dir, do_snapshot_test

@all_files_in_dir(Path(__file__).parent / "test_cases")
def test_snapshots(file_path: Path, snapshot, engine_config: cfg.Config, engine_size):
    do_snapshot_test(engine_config, engine_size, snapshot, file_path)
