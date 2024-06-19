import os
import glob
import numpy as np
import colorama as ca
import subprocess
import f90nml

def p_header(text):
    print(ca.Fore.CYAN + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def p_hint(text):
    print(ca.Fore.LIGHTBLACK_EX + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def p_success(text):
    print(ca.Fore.GREEN + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def p_fail(text):
    print(ca.Fore.RED + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def p_warning(text):
    print(ca.Fore.YELLOW + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def get_env(vns=None):
    envs_list = subprocess.run('env', capture_output=True, text=True).stdout.split('\n')
    env = os.environ.copy()
    for env_str in envs_list:
        try:
            env_name, env_value = env_str.split('=', 1)
            if vns is None:
                env.update({env_name: env_value})
            else:
                if env_name in vns:
                    env.update({env_name: env_value})
        except:
            pass

    return env

def run_shell(cmd, **kws):
    print(f'CMD >>> {cmd}')
    # env = get_env()
    _kws = {
        'shell': True,
        # 'env': env,
    }
    _kws.update(kws)
    subprocess.run(cmd, **_kws)


def replace_str(fpath, d):
    ''' Replace the string in a given text file according to the dictionary `d`
    '''
    with open(fpath, 'r') as f:
        text = f.read()
        for k, v in d.items():
            search_text = k
            replace_text = v
            text = text.replace(search_text, replace_text)

    with open(fpath, 'w') as f:
        f.write(text)

def mod_nml(fpath, params, group=None, rewrite=False):
    nml = f90nml.read(fpath)
    if group is not None:
        for k, v in params.items():
            nml[group][k] = v
    else:
        for k, v in params.items():
            nml[k] = v
        
    if rewrite:
        nml.write(fpath, force=True)
    else:
        return nml

def print_nml(fpath, group=None):
    nml = f90nml.read(fpath)
    if group is not None:
        for k, v in nml[group].items():
            p_hint(f'  {k} = {v}')
    else:
        for k, v in nml.items():
            p_hint(f'  {k} = {v}')