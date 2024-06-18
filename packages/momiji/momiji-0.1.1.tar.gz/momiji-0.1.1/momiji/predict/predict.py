import anndata
import numpy as np
import torch
import torch.nn as nn
from anndata.experimental.pytorch import AnnLoader


class Predictor(nn.Module):
    def __init__(self, adata: anndata.AnnData, model, batch_size: int = 1024):
        """
        Args:
            input_dim (int): Number of input features.
        """
        super(Predictor, self).__init__()
        self.adata = adata
        self.batch_size = batch_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = model.to(self.device)
        self.dataloader = AnnLoader(
            adata, batch_size=batch_size, use_cuda=self.device == "cuda"
        )

    def check_features_in_adata(
        self,
        adata: anndata.AnnData,
        model: nn.Module,
    ) -> anndata.AnnData:
        # Preallocate the data matrix
        X_model = np.empty((adata.n_obs, len(model.features)), order="F")

        # Find indices of matching features in adata.var_names
        feature_indices = {
            feature: i for i, feature in enumerate(adata.var_names)
        }
        model_feature_indices = np.array(
            [feature_indices.get(feature, -1) for feature in model.features]
        )

        # Identify missing features
        missing_features_mask = model_feature_indices == -1
        missing_features = np.array(model.features)[
            missing_features_mask
        ].tolist()

        # Assign values for existing features
        existing_features_mask = ~missing_features_mask
        existing_features_indices = model_feature_indices[
            existing_features_mask
        ]
        X_model[:, existing_features_mask] = np.asfortranarray(adata.X)[
            :, existing_features_indices
        ]

        # Handle missing features
        """
        if model.reference_values is not None:
            X_model[:, missing_features_mask] = np.array(
                model.reference_values
            )[missing_features_mask]
        else:
            X_model[:, missing_features_mask] = 0
        """

        # Calculate missing features statistics
        num_missing_features = len(missing_features)
        percent_missing = 100 * num_missing_features / len(model.features)

        # Add missing features and percent missing values to the clock
        adata.uns[f"{model.metadata['clock_name']}_percent_na"] = percent_missing
        adata.uns[f"{model.metadata['clock_name']}_missing_features"] = missing_features

        # Add matrix to obsm
        adata.obsm[f"X_{model.metadata['clock_name']}"] = X_model

        return adata

    def forward(self, adata: anndata.AnnData):
        adata = self.check_features_in_adata(adata, self.model)
        dataloader = AnnLoader(
            adata, batch_size=self.batch_size, use_cuda=self.device == "cuda"
        )
        predictions = []
        with torch.no_grad():
            for batch in dataloader:
                inputs = batch.obsm[f"X_{self.model.metadata['clock_name']}"].to(
                    torch.float32
                )

                batch_pred = self.model(inputs)
                predictions.append(batch_pred)
        # Concatenate all batch predictions
        predictions = torch.cat(predictions)
        return predictions
