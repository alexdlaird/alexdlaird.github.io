.PHONY: all start

SHELL := /usr/bin/env bash

all: start

start:
	git submodule update --init --recursive
	hugo server
