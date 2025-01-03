import pickle
import os
import logging
import sys
from pathlib import Path
from typing import Tuple, Any, List, Union
import numpy as np
from sklearn.preprocessing import StandardScaler

class AllostericSitePredictor:
    def __init__(self, model_path: str, labels_path: str, features_path: str):
        self.logger = self._setup_logger()
        self.weights = self._load_pickle(model_path, "model weights")
        self.labels = self._load_pickle(labels_path, "labels")
        self.features = self._load_pickle(features_path, "features")
        self.scaler = StandardScaler()
        
        # Process weights to get mean weight vector
        self._process_weights()
        
        if isinstance(self.features, np.ndarray):
            self.scaler.fit(self.features)
            self.logger.info(f"Scaler fitted with training features of shape {self.features.shape}")

    def _process_weights(self):
        """Process the weights to create a mean weight vector for scoring."""
        if not isinstance(self.weights, np.ndarray):
            self.weights = np.array(self.weights)
            
        self.logger.info(f"Original weights shape: {self.weights.shape}")
        
        # Calculate mean weights across samples
        self.weights = np.mean(self.weights, axis=0)
        self.logger.info(f"Computed mean weight vector of shape: {self.weights.shape}")

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('AllostericSitePredictor')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_pickle(self, file_path: str, file_type: str) -> Any:
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"{file_type} file not found at {file_path}")
            
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                self.logger.info(f"Loaded {file_type} with type {type(data)}")
                if isinstance(data, np.ndarray):
                    self.logger.info(f"{file_type} shape: {data.shape}")
                elif isinstance(data, list):
                    self.logger.info(f"{file_type} length: {len(data)}")
                return data
        except Exception as e:
            self.logger.error(f"Error loading {file_type} file: {str(e)}")
            raise

    def run_fpocket(self, pdb_file: str) -> str:
        pdb_path = Path(pdb_file)
        if not pdb_path.exists():
            raise FileNotFoundError(f"PDB file not found at {pdb_path}")
        
        base_name = pdb_path.stem
        output_dir = f"{base_name}_out"
        
        self.logger.info(f"Running fpocket on {pdb_file}")
        exit_code = os.system(f"fpocket -f {pdb_file}")
        if exit_code != 0:
            raise RuntimeError(f"fpocket failed with exit code {exit_code}")
            
        self.logger.info("fpocket completed successfully")
        return output_dir

    def _convert_to_numpy(self, features: Union[List, np.ndarray]) -> np.ndarray:
        if isinstance(features, list):
            self.logger.info(f"Converting list of {len(features)} features to numpy array")
            features = np.array(features)
            
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
            self.logger.info(f"Reshaped features to {features.shape}")
            
        return features

    def extract_pocket_features(self, info_file: str) -> np.ndarray:
        try:
            from utils.pocket_feature import pocket_feature
            features = pocket_feature(info_file)
            
            features = self._convert_to_numpy(features)
            self.logger.info(f"Extracted features with shape: {features.shape}")
            
            scaled_features = self.scaler.transform(features)
            self.logger.info(f"Scaled features with shape: {scaled_features.shape}")
            
            return scaled_features
            
        except Exception as e:
            self.logger.error(f"Error extracting pocket features: {str(e)}")
            raise

    def compute_scores(self, features: np.ndarray) -> np.ndarray:
        """Compute scores for each pocket using the mean weight vector."""
        self.logger.info(f"Computing scores for features of shape {features.shape}")
        self.logger.info(f"Using weight vector of shape {self.weights.shape}")
        
        # Compute scores using dot product with mean weight vector
        scores = features @ self.weights
        
        # Convert to probabilities using softmax
        exp_scores = np.exp(scores - np.max(scores))
        probabilities = exp_scores / exp_scores.sum()
        
        return probabilities

    def predict(self, pdb_file: str) -> Tuple[int, float]:
        try:
            output_dir = self.run_fpocket(pdb_file)
            info_file = Path(output_dir) / f"{Path(pdb_file).stem}_info.txt"
            
            pocket_features = self.extract_pocket_features(str(info_file))
            probabilities = self.compute_scores(pocket_features)
            
            # Get the pocket with the highest probability
            max_index = np.argmax(probabilities)
            max_probability = probabilities[max_index]
            
            return max_index + 1, max_probability
            
        except Exception as e:
            self.logger.error(f"Prediction failed: {str(e)}")
            raise

def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python 7-predict.py <pdb_file>")
            sys.exit(1)
        
        pdb_file = sys.argv[1]
        
        predictor = AllostericSitePredictor(
            model_path="new_features.pkl",
            labels_path="data/labels.pkl",
            features_path="data/2023new_features.pkl"
        )
        
        pocket_index, probability = predictor.predict(pdb_file)
        
        print("\nPrediction Results:")
        print(f"Most likely allosteric binding site: Pocket {pocket_index}")
        print(f"Confidence score: {probability:.4f}")
        
    except Exception as e:
        logging.error(f"Program failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
