.PHONY: setup run build clean

setup:
	pip install pillow pygame

run:
	python color_hit.py

build:
	pyinstaller -noconfirm pack.spec

clean:
	rm -rf build
	rm -rf dist/color_hit
