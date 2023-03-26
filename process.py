from datetime import datetime
import glob
import subprocess
import shutil
from pathlib import Path
import click

from kmedoids import kmedoids_clustering

XES_INPUT = Path('input')

REACME_OUTPUT = Path('output')
BASE_OUTPUT_DIR = Path(f"clusters_output_{datetime.now().strftime('%d_%b_%H_%M_%S')}")
BASE_OUTPUT_DIR.mkdir()

MIN_SAMPLES = 15

# PARAMETERS = [
#     ['0','0','0','0'],
#     ['0','0','1','0'],
#     ['0','1','0','0'],
#     ['0','1','1','0'],
# ]

PARAMETERS = [
    ['0','0','0','0'],
    ['0','0','1','0'],
    ['1','0','0','0'],
    ['1','1','0','0'],
    ['0.5','0','0','0'],
    ['0.5','1','1','0'],
]

@click.command()
@click.argument('directory', type=click.Path(exists=True, path_type=Path))
def process(directory: Path):
    for subdir in directory.iterdir():
        if subdir.is_dir():
            cluster_dir(subdir)
    # for path in directory.glob('*.txt'):
        # click.echo(path)

def cluster_dir(directory: Path):
    xes_files = [f for f in directory.iterdir() if f.suffix == '.xes']
    if len(xes_files) < MIN_SAMPLES:
        print(f"Skipping {directory} because it has less than 3 xes files")
        return
    try:
        shutil.rmtree(XES_INPUT)
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(REACME_OUTPUT)
    except FileNotFoundError:
        pass
    XES_INPUT.mkdir(exist_ok=True)
    REACME_OUTPUT.mkdir(exist_ok=True)

    for file in xes_files:
        shutil.copyfile(file, XES_INPUT / file.name)

    for parameters in PARAMETERS:
        subprocess.call('java -jar reacme_hm.jar ' + ' '.join(parameters), shell=True)

        output_dir = BASE_OUTPUT_DIR / f"{directory.stem}_{''.join(parameters)}"
        output_dir.mkdir()

        distance_matrix = next(REACME_OUTPUT.glob("DistanceGraph*.csv"))
        shutil.copyfile(distance_matrix, output_dir / distance_matrix.name)
        try:
            heatmap_file = REACME_OUTPUT / 'select_all_from_attivita.csv'
            shutil.copyfile(heatmap_file, output_dir / heatmap_file.name)
        except FileNotFoundError:
            print(f"Warning: {heatmap_file} not found")
        clusters = kmedoids_clustering(distance_matrix, len(xes_files), output_dir)
        for cluster, files in clusters.items():
            clust_dir = output_dir / str(cluster)
            clust_dir.mkdir()
            for file in files:
                dfg_file = directory / f"{file}.png"
                shutil.copyfile(dfg_file, clust_dir / f"{file}.png")
        # deletes output files
        distance_matrix.unlink()
        heatmap_file.unlink(missing_ok=True)
    # for file in directory.iterdir():
    #     if file.suffix != '.xes':
    #         continue
        # xes_files.append(file)
    # for path in directory.glob('*.txt'):
        # yield path
    
if __name__ == '__main__':
    process()