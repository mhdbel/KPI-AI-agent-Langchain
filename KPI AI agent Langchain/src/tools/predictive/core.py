"""Core predictive analysis functionality"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import json
from typing import Dict, Any, Tuple

class PredictiveAnalyzer:
    """Perform predictive analysis on KPI data"""
    
    @staticmethod
    def prepare_data(df: pd.DataFrame, target_column: str, 
                    feature_columns: list = None) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare data for predictive modeling"""
        # Select numeric columns if features not specified
        if feature_columns is None:
            feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if target_column in feature_columns:
                feature_columns.remove(target_column)
        
        # Remove rows with missing target values
        df_clean = df.dropna(subset=[target_column])
        
        # Prepare features and target
        X = df_clean[feature_columns].fillna(0)  # Fill missing values
        y = df_clean[target_column]
        
        return X, y
    
    @staticmethod
    def train_forecast_model(X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """Train predictive model and return results"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = dict(zip(X.columns, model.feature_importances_))
        
        return {
            'model_performance': {
                'mse': float(mse),
                'rmse': float(np.sqrt(mse)),
                'r2_score': float(r2)
            },
            'feature_importance': feature_importance,
            'predictions': {
                'actual': y_test.tolist(),
                'predicted': y_pred.tolist()
            }
        }
    
    @staticmethod
    def forecast_future(df: pd.DataFrame, target_column: str, 
                       periods: int = 12) -> Dict[str, Any]:
        """Generate future forecasts"""
        # This is a simplified forecasting approach
        # In practice, you'd use more sophisticated time series methods
        
        if target_column not in df.columns:
            raise ValueError(f"Target column {target_column} not found in data")
        
        # Simple trend-based forecasting
        target_data = df[target_column].dropna()
        if len(target_data) < 2:
            raise ValueError("Insufficient data for forecasting")
        
        # Calculate trend
        trend = (target_data.iloc[-1] - target_data.iloc[0]) / len(target_data)
        
        # Generate forecasts
        last_value = target_data.iloc[-1]
        forecasts = [last_value + (i + 1) * trend for i in range(periods)]
        
        return {
            'forecasts': forecasts,
            'periods': periods,
            'trend': float(trend),
            'confidence_intervals': []  # Simplified - would include actual CIs
        }