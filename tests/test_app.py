from datetime import datetime, timezone
from types import SimpleNamespace

import dis_frontend_dataset_controller.app as app_module


def test_hello_and_build_metadata(monkeypatch):
    build_time = "1792500000"
    monkeypatch.setenv("BUILD_TIME", build_time)
    monkeypatch.setenv("VERSION", "test-version")
    monkeypatch.setenv("GIT_COMMIT", "test-commit")

    captured = {}

    class FakeRegistry:
        def __init__(self, build_info):
            captured["build_info"] = build_info

        def register(self, *args, **kwargs):
            pass

        async def run_all_checks(self):
            return {"status": "OK"}

    monkeypatch.setattr(app_module, "HealthCheck", FakeRegistry)
    monkeypatch.setattr(
        app_module,
        "ExternalAPIHealthCheck",
        lambda *args: SimpleNamespace(check=lambda: None),
    )
    monkeypatch.setattr(app_module.threading.Thread, "start", lambda self: None)

    client = app_module.create_app().test_client()

    response = client.get("/hello")
    assert response.status_code == 200

    build_info = captured["build_info"]
    expected = datetime.fromtimestamp(int(build_time), tz=timezone.utc)
    assert datetime.fromisoformat(build_info.build_time) == expected