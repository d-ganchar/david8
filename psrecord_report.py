import codecs

import pandas as pd
from rich.align import Align
from rich.console import Console
from rich.style import Style
from rich.table import Table


def get_report_data():
    _df = pd.DataFrame()

    for filename in ['sqlalchemy.txt', 'david8.txt', 'peewee.txt', 'pypika.txt']:
        with codecs.open(f'./psrecord_reports/{filename}') as file:
            # 1 - Elapsed time, CPU - 2, Real MB -3
            next(file)
            next(file)
            body = file.read()

        lines = body.split("\n")
        if lines[-1] == '' and len(lines) > 1:
            lines.pop(-1)

        lines.pop(-1)
        body = "\n".join(lines)
        records = []

        for line in body.split("\n"):
            elements = line.split()
            if not elements:
                continue
            elapsed_time, cpu_perc, ream_mb, _ = [float(e) for e in elements]
            records.append({
                'elapsed_time': elapsed_time,
                'cpu_percent': cpu_perc,
                'real_mb': ream_mb,
            })

        package, _ = filename.split('.')
        file_df = pd.DataFrame(records)
        file_df['package'] = package
        _df = pd.concat([_df, file_df], ignore_index=True)

    return _df


df = (
    get_report_data()
    .groupby('package')
    .max(['package', 'real_mb', 'cpu_percent', 'elapsed_time'])
    .reset_index()
)

min_real_mb = df['real_mb'].min()
min_cpu = df['cpu_percent'].min()
min_elapsed_time = df['elapsed_time'].min()

console = Console()
table = Table(
    title='[bold yellow]psrecord Report[/bold yellow]',
    border_style='magenta',
    header_style='blue',
    width=100,
)

table.add_column('Package', justify='left')
table.add_column('Elapsed Time (sec)', justify='right')
table.add_column('Max Real (MB)', justify='right')
table.add_column('Max CPU (%)', justify='right')

records = df.groupby('package').max([
    'package',
    'real_mb',
    'cpu_percent',
    'elapsed_time',
]).reset_index().to_dict('records')

for r in records:
    elapsed_time = r['elapsed_time']
    real_mb = r['real_mb']
    cpu_percent = r['cpu_percent']
    elapsed = f"[green]{elapsed_time}" if elapsed_time == min_elapsed_time else f'{elapsed_time}'
    real_mb = f"[green]{real_mb}" if real_mb == min_real_mb else f'{real_mb}'
    cpu_percent = f"[green]{cpu_percent}" if cpu_percent == min_cpu else f'{cpu_percent}'

    table.add_row(
        f"{r['package']}",
        elapsed,
        real_mb,
        cpu_percent,
        style=Style()
    )

console.print(Align.center(table))
