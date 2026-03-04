#!/usr/bin/env python3
import json
from pathlib import Path


DEFAULT_CONFIG_PATH = "/home/ubuntu/.openclaw/workspace/ops/reed-agent-os/config/error-classifier.json"


class ErrorClassifier:
    def __init__(self, config: dict):
        self.config = config

    @classmethod
    def from_file(cls, path: str = DEFAULT_CONFIG_PATH):
        p = Path(path)
        if not p.exists():
            return cls({"default_class": "fatal", "retryable": {"exit_codes": [], "stderr_keywords": []}, "fatal": {"exit_codes": [], "stderr_keywords": []}, "step_overrides": {}})
        return cls(json.loads(p.read_text(encoding="utf-8")))

    def classify(self, step_name: str, returncode: int | None, stderr: str) -> str:
        cfg = self.config
        step_overrides = cfg.get("step_overrides", {}).get(step_name, {})

        if step_overrides.get("always") in ("retryable", "fatal", "none"):
            return step_overrides["always"]

        fatal_exit_codes = set(cfg.get("fatal", {}).get("exit_codes", []))
        fatal_exit_codes.update(step_overrides.get("fatal_exit_codes", []))
        retryable_exit_codes = set(cfg.get("retryable", {}).get("exit_codes", []))

        text = (stderr or "").lower()
        fatal_keywords = [k.lower() for k in cfg.get("fatal", {}).get("stderr_keywords", [])]
        retryable_keywords = [k.lower() for k in cfg.get("retryable", {}).get("stderr_keywords", [])]

        if returncode in fatal_exit_codes:
            return "fatal"
        if any(k in text for k in fatal_keywords):
            return "fatal"

        if returncode in retryable_exit_codes:
            return "retryable"
        if any(k in text for k in retryable_keywords):
            return "retryable"

        return cfg.get("default_class", "fatal")
