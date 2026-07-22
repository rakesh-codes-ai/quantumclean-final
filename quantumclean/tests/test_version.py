import quantumclean


def test_version_is_1_0_0():
    assert quantumclean.__version__ == "1.0.0"


def test_public_api_is_exported():
    # the stable public surface must stay importable
    for name in [
        "Schema", "EmailValidator", "QualityScorer",
        "QualitySLA", "LineageTracker", "get_backend",
    ]:
        assert hasattr(quantumclean, name), f"{name} missing from public API"
