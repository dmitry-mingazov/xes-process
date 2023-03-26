from pathlib import Path
import click

import pm4py

MIN_SAMPLES = 15

@click.command()
@click.argument('directory', type=click.Path(exists=True, path_type=Path))
def logs2dfg(directory: Path):
    for subdir in directory.iterdir():
        if not subdir.is_dir():
            continue
        files = [f for f in subdir.iterdir() if f.suffix == '.xes']
        if len(files) < MIN_SAMPLES:
            continue
        for file in files:
            print(f"Doing {file}.png")
            log = pm4py.read_xes(str(file))
            log['case:concept:name'] = log['case:concept:name'].astype(int).astype(str)
            # if (log['case:concept:name'].dt == '0').all():
                # continue
            # log = log.dtypes()
            dfg = pm4py.discover_dfg(log)
            pm4py.save_vis_dfg(*dfg, subdir / f"{file.stem}.png")

if __name__ == '__main__':
    logs2dfg()
