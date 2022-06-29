.PHONY: setup run clean

setup:
	pip install pillow pygame

run:
	python color_hit.py

clean:
	rm -rf build
	rm -rf dist/color_hit
