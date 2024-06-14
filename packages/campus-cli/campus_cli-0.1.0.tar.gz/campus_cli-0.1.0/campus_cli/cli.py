import nbformat
import click 
import os
import glob

@click.group()
def cli():
    pass

@click.command()
@click.option('-r', is_flag=True, help='Strip solutions recursively in the tree structure')
@click.option('--dry-run', is_flag=True, help='Test what would happen, without doing it.')
@click.argument('path', type=click.Path(exists=True))
def strip_solutions(r, path, dry_run):
    """ Strip the solutions from the specified notebook """

    if path and not r:
        click.echo(f"Cells containing '# Solution' have been stripped and saved. ")
        if not dry_run:
            strip_notebook_solutions_and_save(path)

    if r and os.path.isdir(path): 
        files = glob.glob(f'{path}/**/*.ipynb', recursive = True) 
        files = [f for f in files if '-student' not in f]
        click.echo(files)
        for file_path in files:
            click.echo(f"\n------\nFILE --> {file_path}")
            if not dry_run:
                click.echo("STATE : Cells solutions stripped and saved.")
                strip_notebook_solutions_and_save(file_path)


def strip_notebook_solutions_and_save(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    nb.cells = list(filter(
        lambda cell: cell.cell_type != 'code' or 
            (cell.cell_type == 'code' and '# Solution' not in cell.source),
        nb.cells
    ))
   
    file_name = os.path.basename(notebook_path) + '-student.ipynb'
    dir_name = os.path.dirname(notebook_path)
    output_path = os.path.join(dir_name, file_name)    
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    click.echo('passé')
    

@click.command()
@click.argument('name')
def hello(name):
    """Describe this tool with colors to You."""
    if name:
        click.secho(f"Hello {name}", bold=True, bg='green', fg='black')
        click.secho(
            "This is Command Line Interface which gives information of maker named Piyush.", bg='blue', fg='white')
    else:
        click.secho(
            "This is Command Line Interface which gives information of maker named Piyush.", bg='blue', fg='white')

cli.add_command(strip_solutions)
cli.add_command(hello)

if __name__ == '__main__':
    cli()
