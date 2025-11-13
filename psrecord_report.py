import codecs

import pandas as pd
from rich.console import Console
from rich.style import Style
from rich.table import Table


def get_report_data():
    _df = pd.DataFrame()

    for filename in ['sqlalchemy.txt', 'david8.txt', 'peewee.txt', 'pypika.txt']:
        with codecs.open(f'./psrecord_reports/{filename}') as file:
            # 1 - Elapsed time, CPU - 2, Real MB -3, virtual - 4
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

            elapsed_time, cpu_perc, ream_mb, virtual = [float(e) for e in elements]
            records.append({
                'elapsed_time': elapsed_time,
                'cpu_percent': cpu_perc,
                'real_mb': ream_mb,
                'virtual_mb': virtual,
            })

        package, _ = filename.split('.')
        file_df = pd.DataFrame(records)
        file_df['package'] = package
        _df = pd.concat([_df, file_df], ignore_index=True)

    return _df


def print_table():
    df = (
        get_report_data()
        .groupby('package')
        .max(['package', 'real_mb', 'virtual', 'cpu_percent', 'elapsed_time'])
        .reset_index()
    )

    min_real_mb = df['real_mb'].min()
    min_virtual_mb = df['virtual_mb'].min()
    min_cpu = df['cpu_percent'].min()
    min_elapsed_time = df['elapsed_time'].min()

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

    records = df.groupby('package').max([
        'package',
        'real_mb',
        'virtual_mb',
        'cpu_percent',
        'elapsed_time',
    ]).reset_index().to_dict('records')

    for r in records:
        elapsed_time = r['elapsed_time']
        real_mb = r['real_mb']
        cpu_percent = r['cpu_percent']
        virtual_mb = r['virtual_mb']
        elapsed = f"[green]{elapsed_time}" if elapsed_time == min_elapsed_time else f'{elapsed_time}'
        real_mb = f"[green]{real_mb}" if real_mb == min_real_mb else f'{real_mb}'
        cpu_percent = f"[green]{cpu_percent}" if cpu_percent == min_cpu else f'{cpu_percent}'
        virtual_mb = f"[green]{virtual_mb}" if virtual_mb == min_virtual_mb else f'{virtual_mb}'

        table.add_row(
            f"{r['package']}",
            elapsed,
            real_mb,
            virtual_mb,
            cpu_percent,
            style=Style()
        )

    console.print(table)


print_table()
