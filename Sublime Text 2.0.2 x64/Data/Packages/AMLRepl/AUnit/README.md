# AUnit

Sublime Text 2 plugin to run an AUnit in Sublime Text 2.

## Installation

The following additions have to be made in your logical.pth file (located in the AML system folder):

```
:aunit                "C:\Users\Simen\Documents\GitHub\ST--PW\Sublime Text 2.0.2 x64\Data\Packages\AMLRepl\AUnit\src\"
:aunit-main-system    :aunit main\
:aunit-core-system    :aunit core\
:aunit-print-system   :aunit print\
:aunit-gui-system     :aunit gui\
```

## Usage

Compile and load the system with: 
```
(compile-system :aunit-core-system)
(compile-system :aunit-print-system)
(compile-system :aunit-gui-system)
(compile-system :aunit-main-system)
```

Run the AUnit GUI with `(aunit)`