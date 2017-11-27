watch:
	./bin/watch.sh $(file)

open:
	export PYTHONPATH="${PYTHONPATH}:./utilities"; python $(homework)/view.py
