Python XML Config Loader
===========

##About
A simple implementation of a config loader, which reads a xml file and parse into a dinamic structure

##Dependeces
Tested in python 2.7
*    lxml

##Installing
```
python setup.py install
```

##How to use
Make a config file like this:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <sample>
        <atemplate template="true">{TEMPLATE_VAR} is a template value</atemplate>

        <integervalue type="int">0</integervalue>

        <winsize type="tuple(int)">"1024", "768"</winsize>

        <otherparams type="list(str)">
            "Hello",
            "beautifully",
            "world!"
        </otherparams>

        <set>
            <one>And it goes...</one>
            <two>...more deep</two>
        </set>
    </sample>
</config>
```
All values are interpreted as strings, unless if is declared the type:
*   int
*   float
*   bool
*   tuple(type)
*   list(type)

You load the file with your config instance
```python
from configloader.config import Config
conf = Config("myconfig.xml", templates={"TEMPLATE_VAR": "This value"})

print conf.attr.atemplate #This value is from a template
print conf.attr.set.one #And it goes...
print conf.attr.set.two #...more deep

```
You can change the values too
```python
conf.attr.integervalue = 42

#Beware, the value don't respect the initial configuration xml file
conf.attr.integervalue = "Hello world!"
```

***

Important! The config is a singleton, this means there's only one instance accessible.
The constructor is called only once, in the first time this is called and no more.
If you change the config file you can use the method 'reload' and if you just want to reset to the last config state
use the reset method.

#Author
Rubens Pinheiro Gonçalves Cavalcante
email: [rubenspgcavalcante@gmail.com](mailto:rubenspgcavalcante@gmail.com)

##License & Rights
*Using GNU GENERAL PUBLIC LICENSE *Version 3, 29 June 2007*
[gnu.org](http://www.gnu.org/copyleft/gpl.html,"GPLv3")
