from os.path import join
import glob
import jinja2

from shutil import copyfile

def render():
  template_file = "template.html"
  templateLoader = jinja2.FileSystemLoader(searchpath="./")
  templateEnv = jinja2.Environment(loader=templateLoader)
  template = templateEnv.get_template(template_file)
  outputText = template.render()  # this is where to put args to the template renderer

  with open(join('dist', 'index.html'), 'w') as f:
    f.write(outputText)

  for filepath in glob.iglob('comics/*.png'):
    print(filepath)
    copyfile(filepath, filepath.replace('comics', 'dist'))
  


if __name__ == "__main__":
  render()

