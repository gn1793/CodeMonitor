import os

def get_env_interval(default: float) -> float:
    v = os.environ.get("CM_INTERVAL")
    try:
        return float(v) if v else default
    except Exception:
        return default

def get_env_outdir(default: str) -> str:
    return os.environ.get("CM_OUT_DIR", default)
