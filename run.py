# -*- coding: utf-8 -*-
import os
import subprocess
import sys

project_root = os.path.dirname(os.path.abspath(__file__))

# Устанавливаем PYTHONPATH
env = os.environ.copy()
env["PYTHONPATH"] = project_root

commands = [
    [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8090", "--reload"],
    ["tuna", "http", "8090", "--subdomain=otpusk"],
]

processes = [subprocess.Popen(cmd, env=env) for cmd in commands]

# (Опционально) дождитесь завершения
for p in processes:
    p.wait()
