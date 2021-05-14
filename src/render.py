#! /usr/bin/env python
from os.path import join, basename, dirname, splitext
import glob
import jinja2

def comic_from_filepath(filepath: str):
  return splitext(basename(filepath))[0]

def image_url_from_filepath(filepath: str):
  # return filepath
  return f'https://www.lonesomecuboid.com/{filepath}'

def url_from_comic(comic: str):
  # return f'{comic}.html'
  return f'https://www.lonesomecuboid.com/{comic}.html'

def render():
  target = dirname(dirname(__file__))

  # Convoluted jinja code
  template_file = join(dirname(__file__), 'template.html')
  templateLoader = jinja2.FileSystemLoader(searchpath=target)
  templateEnv = jinja2.Environment(loader=templateLoader)
  template = templateEnv.get_template(template_file)

  files = list(glob.iglob('comics/*.png'))
  first_comic = comic_from_filepath(files[0])
  last_comic = comic_from_filepath(files[-1])
  for index, filepath  in enumerate(files):
    is_first = (index == 0)
    is_last = (index == len(files) - 1)
    comic = comic_from_filepath(filepath)
    prev_comic = comic_from_filepath(files[index-1])
    next_comic = comic_from_filepath(files[index+1]) if not is_last else ''
    print(comic)

    outputText = template.render(
      title = f'The Lonesome Cuboid - {comic}',
      image_url= image_url_from_filepath(filepath),
      url = url_from_comic(comic),
      description = 'The struggles of a lonesome cuboid in an intimidating, geometrical world',
      content = f"""
      <img width="100%" src="{image_url_from_filepath(filepath)}" />
      <img hidden width="100%" src="{image_url_from_filepath(files[index-1])}" />
      <img hidden width="100%" src="{image_url_from_filepath(files[(index+1)%(len(files))])}" />
      """,
      first = f'<a href="{url_from_comic(first_comic)}">&lt;&lt;</a>',
      last = f'<a href="{url_from_comic(last_comic)}">&gt;&gt;</a>',
      prev = f'<a href="{url_from_comic(prev_comic)}">&lt; Prev</a>' if not is_first else '<span>-</span>',
      next = f'<a href="{url_from_comic(next_comic)}">Next &gt;</a>' if not is_last else '<span>-</span>',
    )

    with open(join(target, f'{comic}.html'), 'w') as f:
        f.write(outputText)

    if is_last:
      with open(join(target, 'index.html'), 'w') as f:
        f.write(outputText)

  outputText = template.render(
    title = f'The Lonesome Cuboid - page not found',
    image_url= image_url_from_filepath('404.png'),
    url = url_from_comic(first_comic),
    description = 'The struggles of a lonesome cuboid in an intimidating, geometrical world',
    content = f"""
    <img width="100%" src="{image_url_from_filepath('404.png')}" />
    """,
    first = f'<a href="{url_from_comic(first_comic)}">&lt;&lt;</a>',
    last = '',
    prev = '',
    next = '',
  )

  with open(join(target, '404.html'), 'w') as f:
        f.write(outputText)

if __name__ == '__main__':
  render()

