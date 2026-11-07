all: demo test

demo:
	python demo_counter.py
	python demo_cache.py

test:
	python -m unittest discover -s tests -v
