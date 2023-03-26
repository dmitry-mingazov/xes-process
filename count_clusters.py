from pathlib import Path
import csv

import click

@click.command()
@click.argument('directory', 
                type=click.Path(exists=True, path_type=Path))
def count_clusters(directory: Path):
    headers = ['run', 'clusters', 'xes_total']
    rows = []
    subdirs = [subdir for subdir in directory.iterdir() 
               if subdir.is_dir()]
    subdirs = sorted(subdirs, key=lambda x: x.stem)
    for subdir in subdirs:
        cluster_file = subdir / 'kmedoids_clustering.csv'
        with open(cluster_file, 'r') as f:
            reader = csv.DictReader(f)
            # next(reader)
            clusters = set()
            logs = set()
            for row in reader:
                logs.add(row['NomeLog'])
                clusters.add(row['ClusterId'])
        rows.append({
            'run': subdir.stem,
            'clusters': len(clusters),
            'xes_total': len(logs),
        })
    with open(directory / 'clusters_summary.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
                # rows.append([subdir.stem] + row)

if __name__ == '__main__':
    count_clusters()