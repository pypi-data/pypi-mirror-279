import nbformat
import click 
import os
import glob
import textract
import re
import requests
import click_completion
import itertools

click_completion.init()

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
    

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('-r', is_flag=True, help='Check urls recursively in the tree structure')
def check_links(path, r):
    """ Check urls validity in a document passed as an argument."""
    
    allowed_extensions = ['.ipynb', '.doc', '.docx', '.pdf', '.md']
    if r :
        files = [glob.glob(path + '/**/*' + ext, recursive=True) for ext in allowed_extensions ]
        files = list(itertools.chain.from_iterable(files))
        
        for file in files:
            click.secho(click.style("FILE : " + file, bg="white"), bold=True)
            document_url_checker(file)
            click.echo('----------------')
    else :
        document_url_checker(path)

def document_url_checker(file_path):
    
    text = get_text(file_path)
    if text is None:
        return None
    
    urls = extract_urls(text)
    for url in urls:
        code, is_valid = is_url_valid(url)
        if is_valid:
            click.echo(click.style("OK : ", fg="green") + url)
        else:
            click.echo(click.style(f"POK ({code}) : ", fg="red") + url)



def extract_urls(text):
    url_pattern = re.compile(r'https?://(?:www\.)?[-\w]+(?:\.[-\w]+)+(?:/[-\w@:%_+.~#?&/=]*)?')
    urls = url_pattern.findall(text)
    return urls    

def is_url_valid(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    try:
        response = requests.head(url, headers=headers, allow_redirects=True, timeout=5)
        return response.status_code, 200 <= response.status_code < 300
    except requests.RequestException :
        return response.status_code, False
    
def get_text(file_path):
    """ Utility to check if displayed links are valid within documents in a folder."""
    allowed_extensions = textract.parsers._get_available_extensions()
    _, file_extension = os.path.splitext(file_path) 
    
    if file_extension in allowed_extensions:
        text = textract.process(file_path)
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            click.secho(f'Error with file {file_path}', fg='red', bold=True)
            text = None
    return text


cli.add_command(strip_solutions)
cli.add_command(check_links)

if __name__ == '__main__':
    cli()
