from pathlib import Path

from jamguard.config.loader import load_experiment_config


def test_load_yaml_config(tmp_path: Path) -> None:
    path = tmp_path / "cfg.yaml"
    path.write_text("name: smoke\n", encoding="utf-8")
    cfg = load_experiment_config(path)
    assert cfg.name == "smoke"
