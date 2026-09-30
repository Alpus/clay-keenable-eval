# Official Python multi-platform digest, verified on 2026-09-30.
FROM python:3.13.15-slim-bookworm@sha256:2325bb286ec344af3e5898cc224b5844e2707ac6e26b1632516fd3edc84a5e26

ARG TARGETARCH
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 CLAY_EVAL_STATE_DIR=/var/lib/clay-eval

# Official installer provenance: clay-run/agent-plugins/clay/scripts/install-cli.sh.
# Pin both the release artifacts and the full reported CLI version.
RUN TARGETARCH="${TARGETARCH}" python3 - <<'PY'
import hashlib
import os
from pathlib import Path
import subprocess
import urllib.request

artifacts = {
    "arm64": ("clay-linux-arm64", "d04c7c15cb23462153b13bc4f3dd18cd33f8a101d410563fd53dad5308991f43"),
    "amd64": ("clay-linux-x64", "ba4b7b96eafab3a0df0f611ab2982314746db5ac85949d4d74b05a7355587a77"),
}
asset, expected = artifacts[os.environ["TARGETARCH"]]
release = "https://github.com/clay-run/agent-plugins/releases/download/clay-cli-v1.4.0/"
with urllib.request.urlopen(release + asset, timeout=120) as response:
    binary = response.read()
if hashlib.sha256(binary).hexdigest() != expected:
    raise SystemExit("Clay release checksum mismatch")
executable = Path("/usr/local/bin/clay")
executable.write_bytes(binary)
executable.chmod(0o755)
version = subprocess.check_output([str(executable), "--version"], text=True).strip()
if version != "1.4.0+de2a0396a538":
    raise SystemExit(f"Unexpected Clay version: {version}")
print("Verified Clay", version)
PY

WORKDIR /app
COPY eval prompt.txt output-schema.json cases.json ./
RUN mkdir -p /var/lib/clay-eval /results /root/.config/clay
ENTRYPOINT ["./eval"]
CMD ["--help"]
