"""
ML-based risk prediction model using DecisionTreeClassifier or LogisticRegression
"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import logging
from backend.config import settings, RISK_LABELS, WEATHER_ENCODING

logger = logging.getLogger(__name__)


class RiskPredictionModel:
    """ML model for railway risk prediction"""
    
    def __init__(self, model_type: str = "decision_tree"):
        """
        Initialize the risk prediction model.
        
        Args:
            model_type: "decision_tree" or "logistic_regression"
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance_ = None
        
        if model_type == "decision_tree":
            self.model = DecisionTreeClassifier(
                max_depth=5,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42
            )
        elif model_type == "logistic_regression":
            self.model = LogisticRegression(
                max_iter=1000,
                random_state=42,
                multi_class='multinomial',
                solver='lbfgs'
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def _generate_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic training data based on domain knowledge.
        In production, this would load from a real dataset.
        """
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic data
        visibility = np.random.uniform(0, 10000, n_samples)
        speed = np.random.uniform(0, 500, n_samples)
        weather_encoded = np.random.choice([0, 1, 2], n_samples)  # Clear, Rain, Fog
        
        # Create features
        X = np.column_stack([
            visibility / settings.VISIBILITY_SCALE_FACTOR,  # Normalized
            speed / settings.SPEED_SCALE_FACTOR,  # Normalized
            weather_encoded
        ])
        
        # Generate labels based on risk rules (domain knowledge)
        y = []
        for i in range(n_samples):
            vis = visibility[i]
            spd = speed[i]
            wth = weather_encoded[i]
            
            risk_score = 0.0
            
            # Visibility factor
            if vis < 100:
                risk_score += 40
            elif vis < 500:
                risk_score += 30
            elif vis < 1000:
                risk_score += 20
            elif vis < 2000:
                risk_score += 10
            
            # Speed factor
            if spd > 150:
                risk_score += 30
            elif spd > 120:
                risk_score += 20
            elif spd > 80:
                risk_score += 10
            
            # Weather factor
            risk_score += wth * 15
            
            # Combined multipliers
            if wth == 2 and vis < 200:  # Fog + low visibility
                risk_score *= 1.3
            if spd > 120 and vis < 500:  # High speed + low visibility
                risk_score *= 1.2
            
            risk_score = min(risk_score, 100.0)
            
            # Classify
            if risk_score < settings.RISK_THRESHOLD_LOW:
                y.append(0)  # Low
            elif risk_score < settings.RISK_THRESHOLD_MEDIUM:
                y.append(1)  # Medium
            else:
                y.append(2)  # High
        
        return X, np.array(y)
    
    def train_model(self) -> None:
        """Train the model on synthetic data"""
        try:
            logger.info(f"Training {self.model_type} model...")
            
            X, y = self._generate_training_data()
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled, y)
            
            # Store feature importance if available
            if hasattr(self.model, 'feature_importances_'):
                self.feature_importance_ = self.model.feature_importances_
            elif hasattr(self.model, 'coef_'):
                # For logistic regression, use absolute coefficients as importance
                self.feature_importance_ = np.abs(self.model.coef_[0])
            
            self.is_trained = True
            logger.info(f"Model trained successfully. Accuracy: {self.model.score(X_scaled, y):.3f}")
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def predict_risk(
        self, 
        visibility: float, 
        speed: float, 
        weather: str
    ) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict risk level and return explainability information.
        
        Args:
            visibility: Visibility in meters
            speed: Speed in km/h
            weather: Weather condition ("Clear", "Rain", or "Fog")
        
        Returns:
            Tuple of (risk_level, confidence, contributing_factors)
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train_model() first.")
        
        # Encode weather
        weather_encoded = WEATHER_ENCODING.get(weather, 0)
        
        # Prepare features (normalized)
        features = np.array([[
            visibility / settings.VISIBILITY_SCALE_FACTOR,
            speed / settings.SPEED_SCALE_FACTOR,
            weather_encoded
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        risk_level = RISK_LABELS[prediction]
        confidence = float(probabilities[prediction])
        
        # Calculate contributing factors for explainability
        contributing_factors = self._calculate_contributing_factors(
            visibility, speed, weather, features_scaled[0]
        )
        
        return risk_level, confidence, contributing_factors
    
    def _calculate_contributing_factors(
        self, 
        visibility: float, 
        speed: float, 
        weather: str,
        features_scaled: np.ndarray
    ) -> Dict[str, float]:
        """
        Calculate contributing factors for explainability.
        
        Returns:
            Dictionary with factor contributions
        """
        factors = {
            "visibility_contribution": 0.0,
            "speed_contribution": 0.0,
            "weather_contribution": 0.0
        }
        
        if self.feature_importance_ is not None:
            # Use feature importance to weight contributions
            factors["visibility_contribution"] = float(
                self.feature_importance_[0] * abs(features_scaled[0])
            )
            factors["speed_contribution"] = float(
                self.feature_importance_[1] * abs(features_scaled[1])
            )
            factors["weather_contribution"] = float(
                self.feature_importance_[2] * abs(features_scaled[2])
            )
        else:
            # Fallback: simple heuristic-based contributions
            if visibility < 500:
                factors["visibility_contribution"] = 0.4
            elif visibility < 2000:
                factors["visibility_contribution"] = 0.2
            
            if speed > 120:
                factors["speed_contribution"] = 0.3
            elif speed > 80:
                factors["speed_contribution"] = 0.15
            
            if weather == "Fog":
                factors["weather_contribution"] = 0.3
            elif weather == "Rain":
                factors["weather_contribution"] = 0.15
        
        return factors


# Global model instance (singleton pattern)
_model_instance: Optional[RiskPredictionModel] = None


def get_model() -> RiskPredictionModel:
    """Get or create the global model instance"""
    global _model_instance
    
    if _model_instance is None:
        _model_instance = RiskPredictionModel(model_type=settings.MODEL_TYPE)
        if settings.MODEL_TRAIN_ON_STARTUP:
            _model_instance.train_model()
    
    return _model_instance
