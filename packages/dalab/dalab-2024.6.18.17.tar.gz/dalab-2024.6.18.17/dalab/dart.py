''' An interface to DART
'''
from . import utils
import subprocess
import os
import f90nml
import x4c
import ipywidgets as wgts
from IPython.display import display

import matplotlib.pyplot as plt

class DART:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        utils.p_header(f'>>> DART.root_dir: {self.root_dir}')


    def compile_model(self, model_name, build_mode='nompi'):
        work_dir = os.path.join(self.root_dir, f'models/{model_name}/work')
        cmd = f'cd {work_dir} && ./quickbuild.sh {build_mode}'
        utils.run_shell(cmd)

    def init_model(self, model_name):
        work_dir = os.path.join(self.root_dir, f'models/{model_name}/work')
        supported_models = {
            'lorenz_63': Lorenz63,
            'forced_lorenz_96': ForcedLorenz96,
        }

        if model_name in supported_models:
            return supported_models[model_name](work_dir)
        else:
            return Model(work_dir)

class Model:
    def __init__(self, work_dir, nml_path=None):
        self.work_dir = work_dir
        utils.p_header(f'>>> Model.work_dir: {self.work_dir}')

        if nml_path is None:
            self.nml_path = os.path.join(self.work_dir, 'input.nml')
        else:
            self.nml_path = nml_path
        utils.p_header(f'>>> Model.nml_path: {self.nml_path}')

        self.params = f90nml.read(self.nml_path)
        utils.p_success(f'>>> Model.params created')

    def update_params(self):
        self.params.write(self.nml_path, force=True)

    def perfect_model_obs(self):
        cmd = f'cd {self.work_dir} && ./perfect_model_obs'
        utils.run_shell(cmd)

    def filter(self):
        cmd = f'cd {self.work_dir} && ./filter'
        utils.run_shell(cmd)

    @property
    def input(self):
        fpath = self.params['perfect_model_obs_nml']['input_state_files']
        ds = x4c.open_dataset(os.path.join(self.work_dir, fpath))
        return ds

    @property
    def output(self):
        fpath = self.params['perfect_model_obs_nml']['output_state_files']
        ds = x4c.open_dataset(os.path.join(self.work_dir, fpath))
        return ds

    @property
    def preassim(self):
        ds = x4c.open_dataset(os.path.join(self.work_dir, 'preassim.nc'))
        return ds

    @property
    def analysis(self):
        ds = x4c.open_dataset(os.path.join(self.work_dir, 'analysis.nc'))
        return ds

    @property
    def filter_input(self):
        ds = x4c.open_dataset(os.path.join(self.work_dir, 'filter_input.nc'))
        return ds

    @property
    def filter_output(self):
        ds = x4c.open_dataset(os.path.join(self.work_dir, 'filter_output.nc'))
        return ds

    @property
    def perfect_input(self):
        ds = x4c.open_dataset(os.path.join(self.work_dir, 'perfect_input.nc'))
        return ds

    @property
    def perfect_output(self):
        ds = x4c.open_dataset(os.path.join(self.work_dir, 'perfect_output.nc'))
        return ds

    @property
    def true_state(self):
        ds = x4c.open_dataset(os.path.join(self.work_dir, 'true_state.nc'))
        return ds
class Lorenz63(Model):
    def __init__(self, work_dir):
        super().__init__(work_dir)

    def plot_it(self, it):
        x4c.set_style('journal', font_scale=1.2)
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(projection='3d')
        sm = self.preassim.state_mean
        ax.plot(sm[:it+1,0], sm[:it+1,1], sm[:it+1,2], color='tab:cyan')
        ax.scatter(sm[it,0], sm[it,1], sm[it,2], color='tab:cyan', s=100, label='preassim')
        sm = self.analysis.state_mean
        ax.plot(sm[:it+1,0], sm[:it+1,1], sm[:it+1,2], color='tab:orange')
        ax.scatter(sm[it,0], sm[it,1], sm[it,2], color='tab:orange', s=100, label='analysis')
        ax.set_title('Lorenz 63', fontweight='bold')
        ax.set_title(f'Step: {it:04d}', loc='right')
        ax.set_xlabel('x', fontweight='bold')
        ax.set_ylabel('y', fontweight='bold')
        ax.set_zlabel('z', fontweight='bold')
        ax.set_xlim(-30, 30)
        ax.set_ylim(-30, 30)
        ax.set_zlim(0, 50)
        ax.legend(frameon=False)
        ax.set_box_aspect(aspect=None, zoom=0.8)
        plt.show(fig)

    def plot(self, min=0, max=None, step=1, style='play'):
        if max is None:
            max = len(self.preassim.time)-1

        if style == 'slider':
            slider = wgts.IntSlider(min=min, max=max, step=step, description='Step')
            wgts.interact(self.plot_it, it=slider)
        elif style == 'play':
            play = wgts.Play(min=min, max=max, step=step)
            wgts.interact(self.plot_it, it=play)




class ForcedLorenz96(Model):
    def __init__(self, work_dir):
        super().__init__(work_dir)

        