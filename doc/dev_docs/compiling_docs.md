# How to Compile Sphinx Docs for Dummies

You need to have `sphinx-build` installed:
```
python -m pip install sphinx-build
```

## Windows

From project root:
```
cd .\doc
.\make.bat html
explorer.exe .\build\html\index.html
```


## Linux

From project root:
```
cd ./doc
make
xdg-open ./build/html/index.html
```
