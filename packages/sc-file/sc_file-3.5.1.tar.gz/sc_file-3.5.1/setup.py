# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scfile',
 'scfile.cli',
 'scfile.exceptions',
 'scfile.file',
 'scfile.file.base',
 'scfile.file.data',
 'scfile.file.formats',
 'scfile.file.formats.dae',
 'scfile.file.formats.dds',
 'scfile.file.formats.mcsa',
 'scfile.file.formats.mic',
 'scfile.file.formats.ms3d',
 'scfile.file.formats.ms3d_ascii',
 'scfile.file.formats.obj',
 'scfile.file.formats.ol',
 'scfile.file.formats.png',
 'scfile.io',
 'scfile.utils',
 'scfile.utils.model']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0',
 'lz4>=4.3.2,<5.0.0',
 'numpy>=1.26.3,<2.0.0',
 'rich>=13.0.0,<14.0.0']

entry_points = \
{'console_scripts': ['build = scripts.build:build']}

setup_kwargs = {
    'name': 'sc-file',
    'version': '3.5.1',
    'description': 'Utility & Library for decoding stalcraft assets',
    'long_description': '# SC FILE\n\nUtility and Library for decoding and converting stalcraft assets files, such as models and textures into well-known formats.\n\nDesigned for artworks creation and the like.\n\n> [!NOTE]\n> There is not and will not be encoding back into game formats.\n\n> [!WARNING]\n> Do not use game assets directly. \\\n> Any changes in game client can be detected.\n\nYou can use executable program from [Releases](https://github.com/onejeuu/sc-file/releases) page.\n\n# 📁 Formats\n\n| Type    | Source        | Output                 |\n| ------- | ------------- | ---------------------- |\n| Model   | .mcsa / .mcvd | .dae, .obj, ms3d, .txt |\n| Texture | .ol           | .dds                   |\n| Image   | .mic          | .png                   |\n\n### Models\n\n- Versions supported: 7.0, 8.0, 10.0, 11.0\n- Skeleton and Animations currently unsupported\n\n### Textures\n\n- Formats supported: DXT1, DXT3, DXT5, RGBA8, BGRA8, DXN_XY\n- Formats unsupported: RGBA32F, Cubemaps\n\n# 💻 CLI Utility\n\n## Usage\n\nFrom bash:\n\n```bash\nscfile [FILES]... [OPTIONS]\n```\n\n> [!TIP]\n> You can just drag and drop one or multiple files onto `scfile.exe`.\n\n## Arguments\n\n- `FILES`: **List of file paths to be converted**. Multiple files should be separated by **spaces**. Accepts both full and relative paths. **Does not accept directory**.\n\n## Options\n\n- `-O`, `--output`: **One path to output directory**. If not specified, file will be saved in same directory with a new suffix.\n\n## Examples\n\n1. Convert a single file:\n\n   ```bash\n   scfile file.mcsa\n   ```\n\n   _Will be saved in same directory with a new suffix._\n\n2. Convert multiple files to a specified directory:\n\n   ```bash\n   scfile file1.mcsa file2.mcsa --output path/to/dir\n   ```\n\n3. Convert all `.mcsa` files in current directory:\n\n   ```bash\n   scfile *.mcsa\n   ```\n\n   _Subdirectories are not included._\n\n4. Convert all `.mcsa` files with subdirectories to a specified directory:\n\n   ```bash\n   scfile **/*.mcsa -O path/to/dir\n   ```\n\n   _With `--output` specified, directory structure is not duplicated._\n\n# 📚 Library\n\n## Install\n\n### Pip\n\n```bash\npip install sc-file -U\n```\n\n### Manual\n\n```bash\ngit clone git@github.com:onejeuu/sc-file.git\n```\n\n```bash\ncd sc-file\n```\n\n```bash\npoetry install\n```\n\n## Usage\n\n### Simple\n\n```python\nfrom scfile import convert\n\n# Output path is optional.\n# Defaults to source path with new suffix.\nconvert.mcsa_to_obj("path/to/model.mcsa", "path/to/model.obj")\nconvert.ol_to_dds("path/to/texture.ol", "path/to/texture.dds")\nconvert.mic_to_png("path/to/image.mic", "path/to/image.png")\n\n# Skeleton support via MilkShape3D\nconvert.mcsa_to_ms3d("path/to/model.mcsa", "path/to/model.ms3d")\nconvert.mcsa_to_ms3d_ascii("path/to/model.mcsa", "path/to/model.txt")\n\n# Or determinate it automatically\nconvert.auto("path/to/model.mcsa")\n```\n\n### Advanced\n\n- Default\n\n```python\nfrom scfile.file.data import ModelData\nfrom scfile.file import McsaDecoder, ObjEncoder\n\nmcsa = McsaDecoder("model.mcsa")\ndata: ModelData = mcsa.decode()\nmcsa.close() # ? Necessary to close\n\nobj = ObjEncoder(data)\nobj.encode().save("model.obj") # ? Encoder closes after saving\n```\n\n- Use encoded content bytes\n\n```python\nobj = ObjEncoder(data)\nobj.encode()\n\nwith open("model.obj", "wb") as fp:\n    fp.write(obj.content)\n\nobj.close() # ? Necessary to close\n```\n\n- Use convert methods\n\n```python\nmcsa = McsaDecoder("model.mcsa")\nmcsa.convert_to(ObjEncoder).save("model.obj")\nmcsa.close() # ? Necessary to close\n```\n\n```python\nmcsa = McsaDecoder("model.mcsa")\nmcsa.to_obj().save("model.obj")\nmcsa.close() # ? Necessary to close\n```\n\n- Use context manager\n\n```python\nwith McsaDecoder("model.mcsa") as mcsa:\n    data: ModelData = mcsa.decode()\n\nwith ObjEncoder(data) as obj:\n    obj.encode().save("model.obj")\n```\n\n- Use context manager + convert methods\n\n```python\nwith McsaDecoder("model.mcsa") as mcsa:\n    obj = mcsa.convert_to(ObjEncoder)\n    obj.close()\n```\n\n```python\nwith McsaDecoder("model.mcsa") as mcsa:\n    mcsa.to_obj().save("model.obj")\n```\n\n> [!IMPORTANT]\n> When using `convert_to` buffer remains open. \\\n> `close()` or `save()` or another context (`with`) is necessary.\n\n- Save multiple copies\n\n```python\nwith McsaDecoder("model.mcsa") as mcsa:\n    with mcsa.to_obj() as obj:\n        obj.save_as("model_1.obj")\n        obj.save_as("model_2.obj")\n```\n\n# 🛠️ Build\n\n> [!IMPORTANT]\n> You will need [poetry](https://python-poetry.org) to do compilation.\n\n> [!TIP]\n> Recommended to create virtual environment.\n>\n> ```bash\n> poetry shell\n> ```\n\nThen install dependencies:\n\n```bash\npoetry install\n```\n\nAnd run script to compile:\n\n```bash\npoetry run build\n```\n\nExecutable file will be created in `/dist` directory.\n',
    'author': 'onejeuu',
    'author_email': 'mail@66rk.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/onejeuu/sc-file',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.13',
}


setup(**setup_kwargs)
