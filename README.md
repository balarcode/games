# games

Practical implementation of few of the interesting games that can be played after compiling the standalone source code files.

## Installation

Steps to install Python interface to Tcl-Tk GUI toolkit on Mac OS (Apple Silicon).

#### Install tcl-tk toolkit via BREW
```
brew install tcl-tk
```

#### Install pyenv via brew
```
brew install pyenv
```

#### Include the following lines in .bash_profile (assuming that the shell is set to BASH)
NOTE: 8.6.15 is the version of installed tcl-tk toolkit.
```
export PYENV_ROOT="$HOME/.pyenv"
```
```
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
```
```
eval "$(pyenv init --path)"
```
```
export PATH="/opt/homebrew/Cellar/tcl-tk/8.6.15/bin/:$PATH"
```
```
LDFLAGS="-L/opt/homebrew/Cellar/tcl-tk/8.6.15/lib"
```
```
CPPFLAGS="-I/opt/homebrew/Cellar/tcl-tk/8.6.15/include"
```
```
PKG_CONFIG_PATH="/opt/homebrew/Cellar/tcl-tk/8.6.15/lib/pkgconfig"
```

#### Then source .bash_profile
```
source <absolute_path>/.bash_profile
```

#### Install Python after configuring the options for tcl-tk toolkit
```
PYTHON_CONFIGURE_OPTS="--enable-framework --with-tcltk-includes='-I/opt/homebrew/Cellar/tcl-tk/8.6.15/include' --with-tcltk-libs='-L/opt/homebrew/Cellar/tcl-tk/8.6.15/lib -ltcl8.6.15 -ltk8.6.15'" pyenv install <python_version>
```
```
pyenv global <python_version>
```

#### Install Python tkinter package for handling Python graphics like Turtle library
```
brew install python-tk
```
```
python -m pip install tk
```

#### Use the following command to test if tkinter has been installed correctly and Python is configured to work with tcl-tk toolkit
NOTE: If the installation was successful, the command will open a new GUI window with 'tk' as the title and display the tck-tk version.
```
python -m tkinter -c "tkinter._test()"
```

## Citation

Please note that the code and technical details made available are for educational purposes only. The repo is not open for collaboration.

If you happen to use the code from this repo, please cite my user name along with link to my profile: https://github.com/balarcode. Thank you!
