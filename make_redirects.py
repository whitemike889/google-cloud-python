import json
import os

from pathlib import Path

template = f"""<html>
<head>
 <meta http-equiv="refresh" content="1; url=https://googleapis.dev/python/{{api_name}}/latest/{{relative_path}}" />
 <script>
   window.location.href = "https://googleapis.dev/python/{{api_name}}/latest/{{relative_path}}"
 </script>
</head>
</html>"""


repo_path = "/usr/local/google/home/busunkim/github/google-cloud-python"

api_dirs = [
    Path(repo_path) / p for p in os.listdir(repo_path) if os.path.exists(Path(repo_path) / p / "noxfile.py")
]
name_map = {}  # to use for redirects of _modules

for api in api_dirs:
	# get the api_name from .repo-metadata.json
	with open(api / '.repo-metadata.json') as f:
		metadata =  json.load(f)
		name_map[api.name] = metadata['name']

	api_directory = Path('latest') / api.name
	for f in api_directory.glob('**/*.html'):
		api_name = metadata['name']
		relative_path = f.relative_to(api_directory)
		with open(f, 'w') as file:
			file.write(template.format(api_name=api_name, relative_path=relative_path))

name_map['iam_credentials'] = 'iam'
name_map['errorreporting'] = 'clouderroreporting'
name_map['devtools'] = 'containeranalysis'
name_map['spanner_admin_database'] = 'spanner'
name_map['spanner_admin_instance'] = 'spanner'
name_map['vision_helpers'] = 'vision'
name_map['vision_helpers.html'] = 'vision'
name_map['client.html'] = 'google-cloud-core'


module_dir = Path('latest/_modules')
for f in module_dir.glob('google/cloud/*/**/*.html'):
	api_name = f.relative_to('latest/_modules/google/cloud').parts[0].rsplit("_v")[0]
	new_name = name_map[api_name]
	relative_path = f.relative_to('latest')
	with open(f, 'w') as file:
		file.write(template.format(api_name=new_name, relative_path=relative_path))

# one last loop to get top level client files

module_dir = Path('latest/_modules')
for f in module_dir.glob('google/cloud/*.html'):
	api_name = f.relative_to('latest/_modules/google/cloud').parts[0].rsplit("_v")[0]
	new_name = name_map[api_name]
	relative_path = f.relative_to('latest')
	with open(f, 'w') as file:
		file.write(template.format(api_name=new_name, relative_path=relative_path))

# api core aaaaah

module_dir = Path('latest/_modules/google/api_core')
for f in module_dir.glob('**/*.html'):
	relative_path = f.relative_to('latest')
	with open(f, 'w') as file:
		new_name = 'google-api-core'
		file.write(template.format(api_name=new_name, relative_path=relative_path))