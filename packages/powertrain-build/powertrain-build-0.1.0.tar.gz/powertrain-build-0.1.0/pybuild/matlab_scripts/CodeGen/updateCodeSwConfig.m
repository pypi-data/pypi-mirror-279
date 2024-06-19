% Copyright 2024 Volvo Car Corporation
% Licensed under Apache 2.0.

function updateCodeSwConfig(RootFolder, model_path)
    % updateCodeSwConfig(RootFolder, model_path)
    %
    % Executes 'py -3.6 -m pybuild.config models' for the model.
    % This script reads the .json, .c and .h-files and looks for configs for
    % the variables that already have a config in the json.
    %
    % Arguments:
    % RootFolder: Pull path to pt_pcc
    % model_path: Path to the model to regenerate config for.
    old_pythonpath = getenv('PYTHONPATH');

    if ~isempty(getenv('PYBUILD_ACTIVATE'))
        % Repo using venv in Zuul/Jenkins.
        % Installs pytools python package and dependencies, see Script/PyTools/setup_pytools.*.
        [~, out]=system(['CALL %PYBUILD_ACTIVATE% & python -m pybuild.config models "' model_path '"']);
    elseif ~isempty(getenv('VENV_FOLDER'))
        % Legacy, repo using venv in Zuul/Jenkins.
        % Repo using pytools folder but it's dependencies in a venv.
        [~, out]=system(['CALL %VENV_FOLDER%\Scripts\activate.bat & python -m pybuild.config models "' model_path '"']);
    elseif ~isempty(getenv('CALLING_PYTHON'))
        % Local run using calling python version
        fprintf('\nUsing calling python: %s\n', getenv('CALLING_PYTHON'));
        setenv('PYTHONPATH', RootFolder)
        [~, out]=system(['%CALLING_PYTHON% -m pybuild.config models "' model_path '"']);
    else
        % Local run
        fprintf('\nUsing python version 3.6\n');
        setenv('PYTHONPATH', RootFolder)
        [~, out]=system(['py -3.6 -m pybuild.config models "' model_path '"']);
    end

    disp(out)
    setenv('PYTHONPATH', old_pythonpath)
end
