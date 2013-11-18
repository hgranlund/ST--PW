# AML Repl

Sublime Text 2 plugin to run an AML interpreter (REPL) inside a Sublime Text 2 view/tab. This document describes usage of the AMLRepl-plugin. For an introduction to the Sublime Text 2 editor, please refer to ["improve workflow in sublime text 2"](https://tutsplus.com/course/improve-workflow-in-sublime-text-2/) by Jeffrey Way.

## Installation

The AML Repl plugin is already installed on this portable version of Sublime Text 2. You only have to configure the plugin with the paths to the AML resources. This configuration is done from `Preferences -> Package Settings -> AMLRepl -> Settings`.

Please refer to AUnit\README.md for installation of the AUnit test framework.

## Usage

All features can be found in the `Tools -> AMLRepl` menu. They can also be accessed through the command palette.

To open a new instance of the AMLRepl, simply open a new buffer and press `Ctrl + Alt + x`.

Pressing `Ctrl + Return` will send the last valid s-expression, or the currently marked region, to the AML interpreter.

## Bundled Plugins

Along with AMLRepl, we have bundeled the ["find function definition"](https://github.com/timdouglas/sublime-find-function-definition) package. 

You use this by highlighting a function and either hit F8 or right click and go to Find Function Definition. The plugin will search your project for the function and open a file up to it, or if multiple instances found display a list of files to open.