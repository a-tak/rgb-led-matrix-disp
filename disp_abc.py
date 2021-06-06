#!/usr/bin/env python3
# coding: UTF-8
# Display a runtext with double-buffering.
from abc import ABCMeta, abstractmethod
from matrix import Matrix

class DispAbc(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, matrix: Matrix):
        pass
    @abstractmethod
    def execute(self):
        pass

