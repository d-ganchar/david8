import codecs
from os import listdir
from os.path import isfile, join

from rich.console import Console
from rich.table import Table


def get_report_data():
    results = []
    report_dir = './psrecord_reports/'
    files = [f for f in listdir(report_dir) if isfile(join(report_dir, f)) and f.endswith('.txt')]

    for filename in files:
        with codecs.open(join(report_dir, filename)) as file:
            next(file)
            next(file)
            body = file.read()

        lines = body.split("\n")
        if lines and lines[-1] == '':
            lines.pop()

        if lines:
            lines.pop()

        package, _ = filename.split('.')

        for line in lines:
            parts = line.split()
            if not parts:
                continue

            elapsed_time, cpu_perc, real_mb, virtual_mb = map(float, parts)

            results.append({
                "package": package,
                "elapsed_time": elapsed_time,
                "cpu_percent": cpu_perc,
                "real_mb": real_mb,
                "virtual_mb": virtual_mb,
            })

    return results


def group_by_max(records):
    grouped = {}

    for r in records:
        pkg = r["package"]

        if pkg not in grouped:
            grouped[pkg] = {
                "package": pkg,
                "elapsed_time": float("-inf"),
                "cpu_percent": float("-inf"),
                "real_mb": float("-inf"),
                "virtual_mb": float("-inf"),
            }

        g = grouped[pkg]
        g["elapsed_time"] = max(g["elapsed_time"], r["elapsed_time"])
        g["cpu_percent"] = max(g["cpu_percent"], r["cpu_percent"])
        g["real_mb"] = max(g["real_mb"], r["real_mb"])
        g["virtual_mb"] = max(g["virtual_mb"], r["virtual_mb"])

    return list(grouped.values())


def print_table():
    raw_data = get_report_data()
    grouped = group_by_max(raw_data)
    grouped = sorted(grouped, key=lambda r: r["real_mb"])

    min_real_mb = min(r["real_mb"] for r in grouped)
    min_virtual_mb = min(r["virtual_mb"] for r in grouped)
    min_cpu = min(r["cpu_percent"] for r in grouped)
    min_elapsed_time = min(r["elapsed_time"] for r in grouped)

    console = Console(force_terminal=True)
    table = Table(
        title='[bold yellow]psrecord Report[/bold yellow]',
        border_style='magenta',
        header_style='blue',
    )

    table.add_column('Package', justify='left')
    table.add_column('Time (sec)', justify='right')
    table.add_column('Max real memory (mb)', justify='right')
    table.add_column('Max virtual memory (mb)', justify='right')
    table.add_column('Max CPU (%)', justify='right')

    for r in grouped:
        elapsed = r["elapsed_time"]
        real_mb = r["real_mb"]
        virtual_mb = r["virtual_mb"]
        cpu_percent = r["cpu_percent"]

        elapsed_fmt = f"[green]{elapsed}" if elapsed == min_elapsed_time else f"{elapsed}"
        real_fmt = f"[green]{real_mb}" if real_mb == min_real_mb else f"{real_mb}"
        virtual_fmt = f"[green]{virtual_mb}" if virtual_mb == min_virtual_mb else f"{virtual_mb}"
        cpu_fmt = f"[green]{cpu_percent}" if cpu_percent == min_cpu else f"{cpu_percent}"

        table.add_row(
            r["package"],
            elapsed_fmt,
            real_fmt,
            virtual_fmt,
            cpu_fmt,
        )

    console.print(table)


print_table()
