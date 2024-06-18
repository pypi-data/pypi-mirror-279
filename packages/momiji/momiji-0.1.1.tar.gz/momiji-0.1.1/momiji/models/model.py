from abc import ABC, abstractmethod

import torch
import torch.nn as nn


class MyModel(nn.Module):
    def __init__(self, in_dim, out_dim, clock_name, features):
        """
        Parameters
        ----------
        input_dim : int
            Number of input features.
        """
        super(MyModel, self).__init__()

        self.linear = nn.Linear(in_dim, out_dim)
        self.features = features
        self.metadata = {"clock_name": clock_name}

    def forward(self, x):
        return self.linear(x)


class ATACmodel(nn.Module):
    def __init__(self, in_dim, out_dim):
        """
        Args:
        input_dim (int): Number of input features.
        """
        super(ATACmodel, self).__init__()

        self.fc = nn.Linear(in_dim, out_dim)

    def forward(self, x):
        return self.fc(x)


class pyagingModel(nn.Module, ABC):
    def __init__(self):
        super().__init__()

        self.metadata = {
            "clock_name": None,
            "data_type": None,
            "species": None,
            "year": None,
            "approved_by_author": None,
            "citation": None,
            "doi": None,
            "notes": None,
            "research_only": None,
            "version": None,
        }

        self.reference_values = None

        self.preprocess_name = None
        self.preprocess_dependencies = None

        self.postprocess_name = None
        self.postprocess_dependencies = None

        self.features = None
        self.base_model_features = self.features

        self.base_model = None

    def forward(self, x):
        x = self.preprocess(x)
        x = self.base_model(x)
        x = self.postprocess(x)
        return x

    @abstractmethod
    def preprocess(self, x):
        """
        Preprocess the input data. This method should be implemented by all subclasses.
        """
        pass

    @abstractmethod
    def postprocess(self, x):
        """
        Postprocess the model output. This method should be implemented by all subclasses.
        """
        pass


class OcampoATAC1(pyagingModel):
    def __init__(self):
        super().__init__()

    def preprocess(self, x):
        """
        Normalize a PyTorch tensor of counts to TPM (Transcripts Per Million) then
        transforms with log1p.
        """

        lengths = torch.tensor(
            self.preprocess_dependencies[0], device=x.device, dtype=x.dtype
        )

        # Normalize by length
        tpm = 1000 * (x / lengths.unsqueeze(0))

        # Scale to TPM (Transcripts Per Million)
        tpm = 1e6 * (tpm / tpm.sum(dim=1, keepdim=True))

        # Apply log1p transformation
        tpm_log1p = torch.log1p(tpm)

        return tpm_log1p[:, self.preprocess_dependencies[1]]

    def postprocess(self, x):
        return x


class OcampoATAC2(pyagingModel):
    def __init__(self):
        super().__init__()

    def preprocess(self, x):
        """
        Normalize a PyTorch tensor of counts to TPM (Transcripts Per Million) then
        transforms with log1p.
        """
        lengths = torch.tensor(
            self.preprocess_dependencies[0], device=x.device, dtype=x.dtype
        )

        # Normalize by length
        tpm = 1000 * (x / lengths.unsqueeze(0))

        # Scale to TPM (Transcripts Per Million)
        tpm = 1e6 * (tpm / tpm.sum(dim=1, keepdim=True))

        # Apply log1p transformation
        tpm_log1p = torch.log1p(tpm)

        return tpm_log1p[:, self.preprocess_dependencies[1]]

    def postprocess(self, x):
        return x



__all__ = ["MyModel", "ATACmodel", "pyagingModel", "OcampoATAC1", "OcampoATAC2"]