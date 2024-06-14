from fast_dev_cli.cli import dev, run_and_echo, runserver


def test_runserver(capsys):
    runserver(dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev" == out.replace("--> ", "")
    runserver(port=8000, dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev" == out.replace("--> ", "")
    runserver(port=9000, dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev --port=9000" == out.replace("--> ", "")
    runserver(host="0.0.0.0", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev --host=0.0.0.0" == out.replace("--> ", "")
    runserver(port=9000, host="0.0.0.0", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev --port=9000 --host=0.0.0.0" == out.replace("--> ", "")


def test_dev(capsys):
    dev(None, None, dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev" == out.replace("--> ", "")
    dev(port=8000, host="", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev" == out.replace("--> ", "")
    dev(port=9000, host=None, dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev --port=9000" == out.replace("--> ", "")
    dev(8000, host="0.0.0.0", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev --host=0.0.0.0" == out.replace("--> ", "")
    dev(port=9000, host="0.0.0.0", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev --port=9000 --host=0.0.0.0" == out.replace("--> ", "")
    dev(8001, host="0.0.0.0", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev --port=8001 --host=0.0.0.0" == out.replace("--> ", "")
    dev(None, file="8001", host="0.0.0.0", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev --port=8001 --host=0.0.0.0" == out.replace("--> ", "")
    dev(None, file="main.py", host="0.0.0.0", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev main.py --host=0.0.0.0" == out.replace("--> ", "")
    dev(8001, file="main.py", host="0.0.0.0", dry=True)
    out = capsys.readouterr().out.strip()
    assert "fastapi dev main.py --port=8001 --host=0.0.0.0" == out.replace("--> ", "")


def test_fast_dev(tmp_path):
    out = tmp_path / "a.txt"
    run_and_echo(f"fast dev 9000 --dry > {out}", verbose=False)
    assert "fastapi dev --port=9000" in out.read_text()
    run_and_echo(f"fast dev main.py --dry > {out}", verbose=False)
    assert "fastapi dev main.py" in out.read_text()
    run_and_echo(f"fast dev main.py --port=9000 --dry > {out}", verbose=False)
    assert "fastapi dev main.py --port=9000" in out.read_text()
    run_and_echo(
        f"fast dev main.py --port=9000 --host=0.0.0.0 --dry > {out}", verbose=False
    )
    assert "fastapi dev main.py --port=9000 --host=0.0.0.0" in out.read_text()
    run_and_echo(f"fast dev 9000 --host=0.0.0.0 --dry > {out}", verbose=False)
    assert "fastapi dev --port=9000 --host=0.0.0.0" in out.read_text()


def test_run_by_module(tmp_path):
    out = tmp_path / "b.txt"
    fast = "python -m fast_dev_cli"
    run_and_echo(f"{fast} dev 9000 --dry > {out}", verbose=False)
    assert "fastapi dev --port=9000" in out.read_text()
    run_and_echo(f"{fast} dev main.py --dry > {out}", verbose=False)
    assert "fastapi dev main.py" in out.read_text()
    run_and_echo(f"{fast} dev main.py --port=9000 --dry > {out}", verbose=False)
    assert "fastapi dev main.py --port=9000" in out.read_text()
    run_and_echo(
        f"{fast} dev main.py --port=9000 --host=0.0.0.0 --dry > {out}", verbose=False
    )
    assert "fastapi dev main.py --port=9000 --host=0.0.0.0" in out.read_text()
    run_and_echo(f"{fast} dev 9000 --host=0.0.0.0 --dry > {out}", verbose=False)
    assert "fastapi dev --port=9000 --host=0.0.0.0" in out.read_text()
