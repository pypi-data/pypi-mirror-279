import argparse
import yaml
import os
import shutil
import warnings







# Suppress all warnings
warnings.filterwarnings('ignore')






import os

def update_ipython_config():
    ipython_config_dir = os.path.expanduser('~/.ipython/profile_default/')
    ipython_config_path = os.path.join(ipython_config_dir, 'ipython_config.py')
    
    # Ensure the IPython config directory exists
    os.makedirs(ipython_config_dir, exist_ok=True)
    
    # Prepare the content to be added

    new_content = [
        "'if \"apis\" in globals():',",
        "'    apis = apis',",
        "'if \"lm\" in globals():',",
        "'    lm = lm',",
        "'if \"lu\" in globals():',",
        "'    lu = lu',",
        "'if \"lumi\" in globals():',",
        # "'    from lumipy.client import Client as __Client',",
        # "'    lumi = __Client(api_secrets_filename=__os.environ.get('FBN_SECRETS_PATH', None))',",
        "'    lumi = lumi',",        
        
        
        
                
        
    ]


    
    config_content = []
    if os.path.exists(ipython_config_path):
        with open(ipython_config_path, 'r') as file:
            config_content = file.readlines()
    
    # Convert list of lines to a set for easy checking
    config_set = set(line.strip() for line in config_content if not line.strip().startswith('#'))

    exec_lines_index = None
    for i, line in enumerate(config_content):
        if "InteractiveShellApp.exec_lines" in line and not line.strip().startswith('#'):
            exec_lines_index = i
            break

    
    if exec_lines_index is not None:
        # Insert new content into existing exec_lines list if not already present
        insertion_point = exec_lines_index + 1
        for line in new_content:
            full_line = '    ' if not line.startswith('if') else "" 
            full_line += line+'\n'
            if all([full_line.strip(),line not in config_set]):
                config_content.insert(insertion_point, full_line )
                insertion_point += 1
    else:
        # No active exec_lines block found, create a new one
        config_content.append('c.InteractiveShellApp.exec_lines = [\n')
        for i in new_content:
            config_content.append(i+'\n')
        config_content.append(']\n')
    
    # Write updated config back to the file
    with open(ipython_config_path, 'w') as file:
        file.writelines(config_content)
        
        
def update_config(args):
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {'features': []}

    enabled_features = set(config.get('features', []))
    if args.enable:
        diff = set(args.enable) - enabled_features
        enabled_features.update(args.enable)
        if 'vars' in args.enable:
            update_ipython_config()

    if args.disable:
        diff = set(args.disable) - enabled_features
        for feature in args.disable:
            if feature in enabled_features:
                enabled_features.difference_update(args.disable)

    config['features'] = list(enabled_features)
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f)



def parse_args():

    parser = argparse.ArgumentParser(description="Configure lusid_express settings.")
    parser.add_argument('-e','--enable', nargs='+', type=str, choices=['vars', 'magic','format', 'all'], help='Enable feature(s).')
    parser.add_argument('-d','--disable', nargs='+', type=str, choices=['vars', 'magic','format', 'all'], help='Disable feature(s).')
    
    return parser.parse_args()

def update_config(args):
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {'features': []}

    enabled_features = set(config.get('features', []))
    show_msg = False
    change_msg = "Configuration updated successfully! Changes will be applied after kernel restart."
    if args.enable:
        if 'all' in args.enable:
            enabled_features.update(['vars', 'magic', 'format'])
        diff = set(args.enable) - enabled_features
        enabled_features.update(args.enable)
        if 'all' in enabled_features:
            enabled_features.remove('all') 
        if 'vars' in enabled_features:
            update_ipython_config()
        if diff:
            print(f"Enabling features: {', '.join(diff)}")
            print(change_msg)

    if args.disable:
        diff = set(args.disable) - enabled_features

        for feature in args.disable:
            if feature in enabled_features:
                show_msg = True
        disabled_features = args.disable
        if 'all' in disabled_features:
            enabled_features.difference_update(['vars', 'magic', 'format'])
        else:
            enabled_features.difference_update(args.disable)
        if show_msg:
            print(f"Disabling features: {', '.join(args.disable)}")
            print(change_msg)

    config['features'] = list(enabled_features)

    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f)
    
    


def copy_startup_file():
    ipython_startup_dir = os.path.expanduser('~/.ipython/profile_default/startup/')
    target_file = os.path.join(ipython_startup_dir, '00-load_lusid_express.py')
    source_file = os.path.join(os.path.dirname(__file__), 'load.le')

    # Ensure the IPython startup directory exists
    os.makedirs(ipython_startup_dir, exist_ok=True)

    # Copy the load.py file if it does not already exist
    shutil.copy(source_file, target_file)
        
        
        
        
def main():
    args = parse_args()
    update_config(args)
    copy_startup_file()
    

if __name__ == "__main__":
    main()
