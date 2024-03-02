import yaml


def main():
    with open('../materials/todo.yml') as fl:
        data: dict = yaml.safe_load(fl)
    playbook: dict = {
        'name': 'deploy',
        'hosts': 'all',
        'tasks': []
    }
    playbook = install_packages(data, playbook)
    playbook = copy_files(data, playbook)
    playbook = run_files(data, playbook)
    with open('deploy.yml', 'w') as fl:
        yaml.dump(playbook, fl)


def install_packages(data: dict, playbook: dict) -> dict:
    todo: dict = data.get('server')
    if todo:
        name_pack: dict = todo.get('install_packages')
        if name_pack:
            playbook['tasks'].append({
                'name': 'Install packages',
                'yum': {
                    'name': name_pack,
                    'state': 'present'
                }
            })
    return playbook


def copy_files(data: dict, playbook: dict):
    todo: dict = data.get('server')
    if todo:
        name_files: dict = todo.get('exploit_files')
        if name_files:
            playbook['tasks'].append({
                'name': 'Copy files',
                'copy': {
                    'src': name_files,
                    'dest': '/tmp',
                }
            })
    return playbook


def run_files(data:dict, playbook: dict):
    bad_gays: list = data.get('bad_guys')
    if bad_gays:
        bad_gays_arg = ''
        for bad_gay in bad_gays:
            bad_gays_arg += f',{bad_gay}'
        bad_gays_arg = bad_gays_arg.strip(',')
        playbook['tasks'].append({
            'name': 'Run files',
            'command': [
                'python3 /tmp/exploit.py',
                f'python3 /tmp/consumer.py -e {bad_gays_arg}'
            ]
        })
    return playbook


if __name__ == '__main__':
    main()
