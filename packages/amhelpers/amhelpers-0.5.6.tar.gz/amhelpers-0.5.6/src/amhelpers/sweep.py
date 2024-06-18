import os
import re
import glob
import copy
import warnings
from os.path import join, isfile
from subprocess import check_output
from pathlib import Path

import git
import pandas as pd
import numpy as np

from amhelpers.amhelpers import save_yaml
from amhelpers.amhelpers import seed_hash
from amhelpers.amhelpers import create_results_dir_from_config


def _extract_jobid(output):
    output = output.decode('utf-8')
    jobid = int(output.split('job')[1])
    return jobid


def update_nested_dict(nested_dict, key_string, value):
    """Update a nested dictionary with a value.
    
    Parameters
    ----------
    nested_dict : dict
        The nested dictionary.
    key_string : str
        A string of keys separated by '::'.
    value : any
        The value to be inserted into the dictionary.

    Examples
    --------
    >>> d = {'a': {'b': {'c': 1}}}
    >>> update_nested_dict(d, 'a::b::c', 2)
    >>> d
    {'a': {'b': {'c': 2}}}
    """
    keys = key_string.split('::')
    current = nested_dict
    for key in keys[:-1]:
        current = current.setdefault(key, {})
    current[keys[-1]] = value


def create_jobscript_from_template(
    template, experiment, experiment_path, estimator, jobname, jobdir=None,
    options={}
):
    with open(template, 'r') as f:
        text = f.read()
    
    text = text.replace('<EXPERIMENT>', experiment)
    text = text.replace('<EXPERIMENT_PATH>', experiment_path)
    text = text.replace('<ESTIMATOR>', estimator)
    
    for key, value in options.items():
        text = text.replace('<%s>' % key.upper(), value)
    
    if jobdir is None:
        jobdir = experiment_path
    
    jobscript_path = join(jobdir, jobname)
    with open(jobscript_path, 'w') as f:
        f.write(text)
    
    return jobscript_path


class Sweep:
    def __init__(
        self, config, estimators, job_template_training, 
        job_template_preprocessing, job_template_postprocessing,
        sweep_param=None, sweep_param_values=None, sweep_param_str=None,
        n_trials=5, n_hparams=10, include_default_hparams=True,
        options={'gpu': 'A40'}
    ):
        self.path, self.config = create_results_dir_from_config(
            config, suffix='sweep', update_config=True
        )
        
        self.estimators = estimators
        
        self.job_template_training = job_template_training
        self.job_template_preprocessing = job_template_preprocessing
        self.job_template_postprocessing = job_template_postprocessing
        
        self.sweep_param = sweep_param
        self.sweep_param_values = sweep_param_values
        self.sweep_param_str = sweep_param_str if sweep_param_str is not None \
            else sweep_param

        self.n_trials = n_trials
        self.n_hparams = n_hparams
        self.include_default_hparams = include_default_hparams
        
        self.options = options
    
    def _create_job_configs(self, default_config, sweep_dir_name='sweep'):
        trials_range = range(1, self.n_trials+1)
        hparams_range = range(self.n_hparams) if self.include_default_hparams \
            else range(1, self.n_hparams+1)

        for estimator in self.estimators:
            config_dir = join(self.path, 'configs', estimator)
            Path(config_dir).mkdir(parents=True, exist_ok=True)

            num_configs = len(os.listdir(config_dir))
            i_config = num_configs + 1

            for trial_seed in trials_range:
                for hparams_seed in hparams_range:
                    config = copy.deepcopy(default_config)
                    
                    config['data']['seed'] = trial_seed
                    config['hparams']['seed'] = hparams_seed
                    config['estimators']['seed'] = seed_hash(
                        config['experiment'], estimator, trial_seed,
                        hparams_seed
                    )
                    
                    results_path = join(
                        self.path, sweep_dir_name, f'trial_{trial_seed:02d}',
                        f'{estimator}_{hparams_seed:02d}'
                    )
                    config['results']['path'] = results_path
                    
                    Path(results_path).mkdir(parents=True)
                    save_yaml(config, results_path, 'config')

                    save_yaml(config, config_dir, f'config{i_config:03d}')
                    i_config += 1

    def prepare(self):
        # =====================================================================
        # Create a directory for log files and save Git info.
        # =====================================================================

        logs_dir = join(self.path, 'logs')
        Path(logs_dir).mkdir()

        try:
            repo = git.Repo(search_parent_directories=True)
            with open(join(self.path, 'repo.tar'), 'wb') as f:
                repo.archive(f)
            git_info = {
                'branch': repo.active_branch, 'hash': repo.head.object.hexsha
            }
            with open(join(self.path, 'gitinfo.txt'), 'w') as f:
                print(git_info, file=f)
        except Exception as e:
            warnings.warn(f"Getting Git info failed: {e}.")

        # =====================================================================
        # Create a config file for each job.
        # =====================================================================
        
        save_yaml(self.config, self.path, 'default_config')

        if self.sweep_param is not None:
            assert self.sweep_param_values is not None
            for value in self.sweep_param_values:
                config = copy.deepcopy(self.config)
                update_nested_dict(config, self.sweep_param, value)
                dir_name = f'sweep_{self.sweep_param_str}_{value}'
                self._create_job_configs(config, dir_name)
            self._n_jobs = len(self.sweep_param_values) * self.n_trials * self.n_hparams
        else:
            self._create_job_configs(self.config)
            self._n_jobs = self.n_trials * self.n_hparams
    
        # =====================================================================
        # Create jobscripts.
        # =====================================================================

        jobscripts_dir = join(self.path, 'jobscripts')
        Path(jobscripts_dir).mkdir()

        self.jobsripcts = {'pre': None, 'main': {}, 'post': None}

        experiment = self.config['experiment']
        kwargs = {
            'experiment': experiment, 'experiment_path': self.path,
            'jobdir': jobscripts_dir, 'options': self.options
        }
        
        jobscript_path = create_jobscript_from_template(
            template=self.job_template_preprocessing, estimator='',
            jobname='job_pre', **kwargs
        )
        self.jobsripcts['pre'] = jobscript_path

        for estimator in self.estimators:
            jobname = f'job_{estimator}'
            jobscript_path = create_jobscript_from_template(
                template=self.job_template_training, estimator=estimator,
                jobname=jobname, **kwargs
            )
            self.jobsripcts['main'][estimator] = jobscript_path

        jobscript_path = create_jobscript_from_template(
            template=self.job_template_postprocessing, estimator='',
            jobname='job_post', **kwargs
        )
        self.jobsripcts['post'] = jobscript_path
    
    def launch(self):
        main_dependencies = [self._submit_job(self.jobsripcts['pre'])]
        
        post_dependencies = []
        for estimator in self.estimators:
            jobid = self._submit_job(
                self.jobsripcts['main'][estimator], main_dependencies,
                self._n_jobs
            )
            post_dependencies.append(jobid)
        
        self._submit_job(self.jobsripcts['post'], post_dependencies)

    def _submit_job(self, jobscript_path, dependencies=None, n_jobs=1):
        command = ['sbatch']
        if dependencies is not None:
            dependencies = [str(d) for d in dependencies]
            dependencies = ':'.join(dependencies)
            command.append(f'--dependency=afterok:{dependencies}')
        if n_jobs > 1:
            command.append(f'--array=1-{n_jobs}')
        command.append(jobscript_path)
        return _extract_jobid(check_output(command))


class Postprocessing:
    def __init__(self, exp_path):
        self.exp_path = exp_path
        config_dir = join(exp_path, 'configs')
        self.estimators = os.listdir(config_dir)
    
    def _get_sweep_dirs(self):
        sweep_dirs = [
            join(self.exp_path, x) for x in os.listdir(self.exp_path)
            if x.startswith('sweep')
        ]
        return sorted(sweep_dirs)
    
    def _get_trial_dirs(self, sweep_dir):
        trial_dirs = [
            join(sweep_dir, x) for x in os.listdir(sweep_dir)
            if 'trial' in x
        ]
        return sorted(trial_dirs)

    def _sort_scores(self, path, sorter):
        all_sorted_scores = {}
        
        for estimator in self.estimators:
            experiments = [
                x for x in os.listdir(path) if x.startswith(estimator)
            ]

            csvs, scores = [], []
            
            for e in experiments:
                p = join(path, e, 'scores.csv')
                if not isfile(p):
                    print(f"File {p} not found.")
                    continue
                
                csv = pd.read_csv(p)
                if not 'subset' in csv.columns:
                    raise ValueError(f"Column 'subset' not found in {p}.")
                csv.insert(0, 'exp', e)
                csvs.append(csv)

                score = sorter(csv)
                if not isinstance(score, float):
                    raise TypeError(
                        "The output of the score sorting function must "
                        f"be a float, but got type {type(score).__name__}."
                    )
                scores.append(score)
            
            if len(csvs) > 0:
                scores = np.array(scores)
                if np.isnan(scores).any():
                    scores[np.isnan(scores)] = -np.inf
                csvs = [csvs[i] for i in np.argsort(scores)[::-1]]
                sorted_scores = pd.concat(csvs, ignore_index=True)
                all_sorted_scores[estimator] = sorted_scores
        
        return all_sorted_scores

    def _collect_best_scores(self, sorted_scores):
        best_scores_list = []

        for i_trial in range(len(sorted_scores)):
            for _estimator, scores in sorted_scores[i_trial].items():
                best_exp = scores.exp.iloc[0]
                best_score = scores.groupby('exp').get_group(best_exp)
                trial = pd.DataFrame({'trial': len(best_score) * [i_trial+1]})
                best_score = pd.concat((trial, best_score), axis=1)
                best_scores_list.append(best_score)
 
        return best_scores_list

    def _concat_scores(self, sorted_scores):
        best_scores = self._collect_best_scores(sorted_scores)
        scores = pd.concat(best_scores, ignore_index=True)
        return scores

    def collect_results(self, score_sorter=None):
        if score_sorter is None:
            score_sorter = lambda csv: csv[csv.subset=='valid']['auc'].item()

        scores = []
        for sweep_dir in self._get_sweep_dirs():
            sorted_scores = []
            for trial_dir in self._get_trial_dirs(sweep_dir):
                sorted_scores += [self._sort_scores(trial_dir, score_sorter)]
            
            sweep_scores = self._concat_scores(sorted_scores)
            
            sweep_dir_name = sweep_dir.split('/')[-1]
            if sweep_dir_name != 'sweep':
                sweep_param_value = sweep_dir_name.split('_')[-1]
                pattern = r'sweep_(.*?)_' + re.escape(sweep_param_value)
                match = re.search(pattern, sweep_dir_name)
                sweep_param = match.group(1)
                sweep_scores.insert(0, sweep_param, sweep_param_value)
            
            scores.append(sweep_scores)
        
        scores = pd.concat(scores, ignore_index=True)
        scores.to_csv(join(self.exp_path, 'scores.csv'), index=False)
    
    def remove_files(self):
        scores_path = join(self.exp_path, 'scores.csv')
        if not isfile(scores_path):
            raise FileNotFoundError(
                f"File {scores_path} is required but was not found."
            )
        scores = pd.read_csv(scores_path)

        dirs_to_keep = []
        if scores.columns[0] != 'trial':
            assert scores.columns[1:3].tolist() == ['trial', 'exp']
            sweep_param = scores.columns[0]
            for sweep_param_value, trial, exp in scores.iloc[:, :3].values:
                sweep = f'sweep_{sweep_param}_{sweep_param_value}'
                dirs_to_keep += [
                    join(self.exp_path, sweep, f'trial_{trial:02d}', exp)
                ]
        else:
            assert scores.columns[:2].tolist() == ['trial', 'exp']
            dirs_to_keep = [
                join(self.exp_path, 'sweep', f'trial_{trial:02d}', exp)
                for trial, exp in scores.iloc[:, :2].values
            ]

        all_dirs = []
        for sweep_dir in self._get_sweep_dirs():
            for trial_dir in self._get_trial_dirs(sweep_dir):
                for x in os.listdir(trial_dir):
                    all_dirs.append(join(trial_dir, x))

        dirs_to_delete = set(all_dirs) - set(dirs_to_keep)

        for d in dirs_to_delete:
            for f in glob.glob(join(d, '*.pt')):
                os.remove(f)
            for f in glob.glob(join(d, '*.pkl')):
                os.remove(f)
            for f in glob.glob(join(d, '*.json')):
                os.remove(f)
