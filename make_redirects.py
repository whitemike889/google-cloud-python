import json
import os

from pathlib import Path

template = f"""<html>
<head>
 <meta http-equiv="refresh" content="1; url=https://googleapis.dev/python/{{api_name}}/latest/index.html" />
 <script>
   window.location.href = "https://googleapis.dev/python/{{api_name}}/latest/index.html"
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

	directories = [Path('latest') / api.name, Path('stable') / api.name]
	for api_directory in directories:
		for ext in ['.html', '.md']:
			for f in api_directory.glob(f'**/*{ext}'):
				api_name = metadata['name']
				relative_path = f.relative_to(api_directory)
				with open(f, 'w') as file:
					file.write(template.format(api_name=api_name))
				os.rename(f, str(f).replace('.md', '.html'))

# manual additions
name_map['iam_credentials'] = 'iam'
name_map['errorreporting'] = 'clouderroreporting'
name_map['devtools'] = 'containeranalysis'
name_map['spanner_admin_database'] = 'spanner'
name_map['spanner_admin_instance'] = 'spanner'
name_map['vision_helpers'] = 'vision'
name_map['vision_helpers.html'] = 'vision'
name_map['vision_helpers.md'] = 'vision'
name_map['client.html'] = 'google-cloud-core'
name_map['client.md'] = 'google-cloud-core'
name_map['iam.md'] = 'iam'
name_map['iam.html'] = 'iam'
name_map['resource-manager'] = 'cloudresourcemanager'
name_map['error-reporting'] = 'clouderroreporting'

module_dirs = [Path('latest/_modules'), Path('stable/_modules')]
for module_dir in module_dirs:
	for f in module_dir.glob('google/cloud/*/**/*'):
		if f.suffix == '.md' or f.suffix == '.html':
			api_name = f.relative_to(module_dir / 'google/cloud').parts[0].rsplit("_v")[0]
			new_name = name_map[api_name]
			relative_path = f.relative_to(module_dir.parts[0])
			with open(f, 'w') as file:
				file.write(template.format(api_name=new_name))
			os.rename(f, str(f).replace('.md', '.html'))

# correct top level client files

module_dirs = [Path('latest/_modules'), Path('stable/_modules')]
for module_dir in module_dirs:
	for f in module_dir.glob('google/cloud/*'):
		if f.suffix == '.md' or f.suffix == '.html':
			api_name = f.relative_to(module_dir / 'google/cloud').parts[0].rsplit("_v")[0]
			new_name = name_map[api_name]
			relative_path = f.relative_to(module_dir.parts[0])
			with open(f, 'w') as file:
				file.write(template.format(api_name=new_name))
			os.rename(f, str(f).replace('.md', '.html'))

# api core fixes

module_dirs = [Path('latest/_modules/google/api_core'), Path('stable/_modules/google/api_core')]
for module_dir in module_dirs:
	for f in module_dir.glob('**/*'):
		if f.suffix == '.md' or f.suffix == '.html':
			relative_path = f.relative_to(module_dir.parts[0])
			with open(f, 'w') as file:
				new_name = 'google-api-core'
				file.write(template.format(api_name=new_name))
			os.rename(f, str(f).replace('.md', '.html'))

