from typing import Dict, List
import os as __os

def load()->Dict[str,List[str]]:
    import yaml as __yaml
    dirname = __os.path.dirname(__file__)
    config_path = __os.path.join(dirname, '../config.yaml')
    if not __os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:
        return __yaml.safe_load(f) or {}


__all__ = ['load']