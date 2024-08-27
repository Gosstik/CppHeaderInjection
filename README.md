```bash
poetry run header_injection init -p "<path/to/project/root>" 
poetry run header_injection config -a "<path/to/include>"
poetry run header_injection run -s "<path/to/source/file>" "out_filename" 
```

Note: include path might be absolute or relative to `project_root`.


To run test go to `project_root` and run:
```bash
poetry run header_injection init -p "$(pwd)"
poetry run header_injection config -a "tests/data/include"
poetry run header_injection config -a "tests/data/other_dir/include"
# -s to put output.cpp in the same dir
poetry run header_injection run -s "tests/data/main.cpp" output.cpp
# -l to lint
poetry run header_injection run -sl "tests/data/main.cpp" output.cpp
```