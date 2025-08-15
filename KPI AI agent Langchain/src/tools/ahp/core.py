"""Core AHP implementation"""
import json
import ahpy
from typing import Dict, Any, Optional
from dataclasses import dataclass

class AHPConfigError(Exception):
    """Raised for invalid AHP configuration errors."""
    pass

@dataclass
class AHPResult:
    weights: Dict[str, float]
    consistency_ratios: Dict[str, float]
    report: str

class AHPCalculator:
    """Handles the mathematical execution of AHP using ahpy"""
    
    @staticmethod
    def validate_consistency(criteria_cr: float, alternatives_cr: Dict[str, float]) -> bool:
        """Check if all consistency ratios are acceptable"""
        if criteria_cr > 0.1:
            return False
        return all(cr <= 0.1 for cr in alternatives_cr.values())
    
    @staticmethod
    def execute_ahp(criteria_comparisons: Dict, 
                   alternative_comparisons: list) -> AHPResult:
        """Execute AHP calculation and return results"""
        # Create criteria comparison
        criteria = ahpy.Compare(
            name='Criteria',
            comparisons=criteria_comparisons,
            precision=3,
            random_index="saaty"
        )
        
        # Create alternative comparisons
        alternatives_dict = {}
        for alt_comp in alternative_comparisons:
            criterion_name = alt_comp['criterion']
            alternatives_dict[criterion_name] = ahpy.Compare(
                name=f'Alternatives_for_{criterion_name}',
                comparisons=alt_comp['comparisons'],
                precision=3,
                random_index="saaty"
            )
        
        # Build hierarchy
        hierarchy = ahpy.Hierarchy(name="Root")
        hierarchy.add(criteria)
        
        # Add alternatives to criteria
        for criterion in criteria.elements:
            if criterion in alternatives_dict:
                criterion_node = criteria.elements[criterion]
                hierarchy.add_child(
                    parent=criteria,
                    child=criterion_node,
                    comparison=alternatives_dict[criterion]
                )
        
        # Get results
        weights = hierarchy.get_priority_vector()
        consistency = {
            'criteria_cr': criteria.consistency_ratio,
            'alternatives_cr': {name: alt.consistency_ratio for name, alt in alternatives_dict.items()}
        }
        
        # Validate consistency
        if not AHPCalculator.validate_consistency(
            criteria.consistency_ratio,
            {name: alt.consistency_ratio for name, alt in alternatives_dict.items()}
        ):
            raise ValueError("AHP consistency check failed")
        
        return AHPResult(
            weights=weights,
            consistency_ratios=consistency,
            report=hierarchy.report()
        )