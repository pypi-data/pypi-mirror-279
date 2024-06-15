#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Iterable
import numpy


class JonesVector:
    """
    Represents a Jones vector for describing the polarization state of light.
    """

    def __init__(self, values: Iterable) -> None:
        """
        Initialize the Jones vector.

        Parameters:
            - jones_vector: Iterable, a collection that represents the Jones vector components.
        """
        self.values = numpy.atleast_2d(values).astype(complex)

    def __repr__(self) -> str:
        return f"JonesVector({self.values})"

    def __add__(self, other) -> 'JonesVector':
        """
        Add another Jones vector to this Jones vector, combining their polarization states.

        Parameters:
            - other: JonesVector, another Jones vector to add.

        Returns:
            - JonesVector, the combined Jones vector.
        """
        return JonesVector(numpy.vstack((self.values, other.values)))


class RightCircular(JonesVector):
    """
    Represents right circular polarization.
    """

    def __init__(self) -> None:
        super().__init__([1, 1j])


class LeftCircular(JonesVector):
    """
    Represents left circular polarization.
    """

    def __init__(self) -> None:
        super().__init__([1, -1j])


class Linear(JonesVector):
    """
    Represents linear polarization for a given angle or angles.
    """

    def __init__(self, *angles: float) -> None:
        """
        Initialize linear polarization with one or more angles.

        Parameters:
            - angles: float, the angle(s) of polarization in degrees.
        """
        self.angles = numpy.array(angles, dtype=float)
        if numpy.isnan(self.angles).any():
            raise ValueError("Unpolarized light source is not implemented yet.")

        jones_vector = numpy.array([numpy.cos(self.angles * numpy.pi / 180), numpy.sin(self.angles * numpy.pi / 180)])
        super().__init__(jones_vector)
