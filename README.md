AutoSaveBuildLatex
===============
A [Sublime Text](http://www.sublimetext.com/) plugin that **automatically saves and build the current TEX file after every modification**.

- [Synopsis](#synopsis)
- [Installation](#installation)
- [Usage](#usage)
- [Author](#author)

Synopsis
-------
AutoSaveBuild is a  Sublime Text package to automatically save or build the current .TEX file after
each change.


Installation
-------
AutoSaveBuildLatex requires [LaTeXTools](https://github.com/SublimeText/LaTeXTools) package installation.

#### From Github
Alternatively, you may install via GitHub by cloning this repository into the `Packages`
directory under Sublime Text's data directory:

On Mac:

```
cd ~/Library/Application Support/Sublime Text 3/Packages
git clone https://github.com/jgonzalezr/auto-save-build-latex.git
```

Usage
-------
**By default, AutoSaveBuildLatex is disabled** because it is a fairly invasive plugin.
To enable it, you must first bind the command to turn the plugin save and build
on or off. Open "Preferences / Key Bindings - User" and add:

```js
{ "keys": ["ctrl+shift+s"], "command": "auto_save_latex" }
```
```js
{ "keys": ["ctrl+shift+s"], "command": "auto_build_latex" }
```

This key bindings file takes an array of key bindings so please ensure that this key binding, along with any existing ones, are properly wrapped in `[]`.

With these setting, pressing <kbd>Ctrl + Shift + S</kbd> will turn the auto_save_latex plugin
on or off. 
Pressing <kbd>Ctrl + Shift + B</kbd> will turn the auto_build_latex plugin
on or off. 
**If you do not want to compile the .TEX file after each change leave the auto_build_latex 
plugin disabled.**
A status message will be displayed in the Sublime Status Bar each
time a plugin is turned on or off.

By default, auto-save-build-latex debounces "save" and "build" events by 1 second. 

Author
-------
AutoSaveBuild was created by Jorge Gonzalez based on [auto-save](https://packagecontrol.io/packages/auto-save) by James Zhang.
