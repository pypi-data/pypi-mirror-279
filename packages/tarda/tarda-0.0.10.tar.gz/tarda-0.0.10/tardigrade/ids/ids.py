"""
This module implements the abstract base classes for all IDSs.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import torch
from torch import nn
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class BaseIDS():
    # TODO: Add nn.Module as parent class
    """
    The abstract base class for all IDSs.
    """
    def __init__(self, **kwargs):
        """
        Initialize the IDS.

        Args:
            **kwargs: Additional keyword arguments.
        """
        self._kwargs = kwargs
        self.model = self._define_model()

    def __call__(self, *args, **kwargs):
        """
        Call the IDS.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The IDS output.
        """
        return self.model(*args, **kwargs)

    def __repr__(self):
        """
        Get the string representation of the IDS.

        Returns:
            The string representation.
        """
        return self.__class__.__name__ + '()'

    def _define_model(self) -> nn.Module:
        """
        Define the pytorch/ tensorflow (to be removed) model.

        Returns:
            The model.
        """
        raise NotImplementedError

    def feature_extractor(self, *args, **kwargs) -> torch.Tensor:
        """
        Extract features from the data.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The extracted features.
        """
        raise NotImplementedError

    def train(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Train the IDS.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        raise NotImplementedError
    
    def test(self, *args, **kwargs) -> torch.Tensor:
        """
        Test the IDS.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        raise NotImplementedError
    
    def evaluate(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Evaluate the IDS.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        raise NotImplementedError
