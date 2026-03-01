"""
Weights System - Implements feature weighting for importance in recommendation.

Weight Strategy - ORIGINAL FEATURES (indices 0-39):
- Cognitive & Problem Solving (Q1-Q5): HIGH weight (1.2x)
- Creativity & Innovation (Q6-Q10): MEDIUM weight (1.0x)
- Communication & Leadership (Q11-Q15): HIGH weight (1.1x)
- Academic & Technical (Q16-Q20): HIGH weight (1.2x)
- Choice Questions (Q21-Q25): VERY HIGH weight (1.5x - forced choices are explicit)

Weight Strategy - NEW FEATURES (indices 40-49):
- Interest Profile (Q26-Q33): LOW-MEDIUM weight (0.6x)
  WHY: These are refiners, not core determinants. They help differentiate between
  similar careers but should not override core abilities (cognitive, technical, etc.)
  
- Work Style Preferences (Q34-Q35): LOW weight (0.4x)
  WHY: Work style is secondary to capabilities. A person may prefer autonomy but 
  still succeed in structured roles if they're highly skilled. Even lower weight
  ensures we don't suggest unsuitable careers based on style preference alone.

Backward Compatibility:
- Old feature weights UNCHANGED (1.2x, 1.0x, 1.1x, 1.2x, 1.5x)
- New features added to indices 40-49 with lower weights
- System with only Q1-Q25 answers still works (new indices default to 0.5, then weighted)

Apply weights BEFORE cosine similarity to emphasize important dimensions.
"""

import numpy as np


class FeatureWeights:
    """
    Implements weighted feature system for career recommendation.
    
    Vector size: 50 (extended from 40)
    - Weights for 0-39 kept IDENTICAL to original system
    - Weights for 40-49 apply differential weighting to new features
    """
    
    # Weights for each dimension (extended to 50)
    DIMENSION_WEIGHTS = np.array([
        # INDICES 0-39: ORIGINAL FEATURES (UNCHANGED for backward compatibility)
        
        # Q1-Q5: Cognitive & Problem Solving (1.2x weight)
        1.2, 1.2, 1.2, 1.2, 1.2,
        
        # Q6-Q10: Creativity & Innovation (1.0x weight)
        1.0, 1.0, 1.0, 1.0, 1.0,
        
        # Q11-Q15: Communication & Leadership (1.1x weight)
        1.1, 1.1, 1.1, 1.1, 1.1,
        
        # Q16-Q20: Academic & Technical (1.2x weight)
        1.2, 1.2, 1.2, 1.2, 1.2,
        
        # Q21-Q25: Forced Choice Questions (1.5x weight each dimension, 20 total)
        1.5, 1.5, 1.5, 1.5,  # Q21: Work environment
        1.5, 1.5, 1.5, 1.5,  # Q22: Problem type
        1.5, 1.5, 1.5, 1.5,  # Q23: Career values
        1.5, 1.5, 1.5, 1.5,  # Q24: Work style
        1.5, 1.5, 1.5, 1.5,  # Q25: Success measure
        
        # INDICES 40-49: NEW FEATURES (extension block)
        
        # Q26-Q33: Interest Profile (0.6x weight - REFINERS, not dominators)
        # These help differentiate between similar careers but don't override
        # core capabilities. Lower weight prevents interest from dominating ability.
        0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6,  # 8 dimensions
        
        # Q34-Q35: Work Style Preferences (0.4x weight - SECONDARY)
        # Work style is a preference, not a requirement. Low weight ensures
        # we don't suggest unsuitable careers based on style alone.
        0.4, 0.4  # 2 dimensions
    ])
    
    @staticmethod
    def apply_weights(user_vector):
        """
        Apply feature weights to user vector.
        
        Backward Compatibility:
        - Works with both 40-dim and 50-dim vectors
        - If vector is 40-dim, only applies original weights
        - If vector is 50-dim, applies full weighting including new features
        
        Args:
            user_vector (np.ndarray): 40-dim or 50-dim user vector
        
        Returns:
            np.ndarray: Weighted user vector (same size as input)
        """
        # Handle both old and new vector sizes
        if len(user_vector) == 40:
            # Old system: use only first 40 weights
            return user_vector * FeatureWeights.DIMENSION_WEIGHTS[:40]
        elif len(user_vector) == 50:
            # New system: use all 50 weights
            return user_vector * FeatureWeights.DIMENSION_WEIGHTS
        else:
            # Fallback: apply element-wise up to vector length
            weights = FeatureWeights.DIMENSION_WEIGHTS[:len(user_vector)]
            return user_vector * weights
    
    @staticmethod
    def apply_weights_to_career(career_vector):
        """
        Apply same weights to career vector for fair comparison.
        
        CRITICAL: Use identical weights for user and career vectors
        so cosine similarity is computed fairly.
        
        Args:
            career_vector (np.ndarray): 40-dim or 50-dim career vector
        
        Returns:
            np.ndarray: Weighted career vector
        """
        if len(career_vector) == 40:
            return career_vector * FeatureWeights.DIMENSION_WEIGHTS[:40]
        elif len(career_vector) == 50:
            return career_vector * FeatureWeights.DIMENSION_WEIGHTS
        else:
            weights = FeatureWeights.DIMENSION_WEIGHTS[:len(career_vector)]
            return career_vector * weights
    
    @staticmethod
    def get_weight_for_dimension(dim_idx):
        """Get weight for a specific dimension."""
        if dim_idx < len(FeatureWeights.DIMENSION_WEIGHTS):
            return FeatureWeights.DIMENSION_WEIGHTS[dim_idx]
        return 1.0  # Default weight
    
    @staticmethod
    def get_weight_profile():
        """
        Get human-readable weight profile showing which dimensions matter most.
        
        Returns:
            dict: Weight information by category
        """
        return {
            "cognitive_problem_solving": {
                "dimensions": "Q1-Q5 (indices 0-4)",
                "weight": 1.2,
                "description": "Problem solving, analysis, debugging, logical thinking"
            },
            "creativity_innovation": {
                "dimensions": "Q6-Q10 (indices 5-9)",
                "weight": 1.0,
                "description": "Creative thinking, design, ideation, innovation"
            },
            "communication_leadership": {
                "dimensions": "Q11-Q15 (indices 10-14)",
                "weight": 1.1,
                "description": "Communication, presentation, mentoring, leadership"
            },
            "academic_technical": {
                "dimensions": "Q16-Q20 (indices 15-19)",
                "weight": 1.2,
                "description": "Mathematics, research, programming, learning"
            },
            "forced_choices": {
                "dimensions": "Q21-Q25 (indices 20-39)",
                "weight": 1.5,
                "description": "Work environment, problem type, values, style, success measure - explicit preferences"
            }
        }
    
    @staticmethod
    def normalize_weights():
        """
        Normalize weights so they sum to the vector size (40).
        Used for interpretation but not for actual calculations.
        
        Returns:
            np.ndarray: Normalized weights
        """
        total = np.sum(FeatureWeights.DIMENSION_WEIGHTS)
        return (FeatureWeights.DIMENSION_WEIGHTS / total) * 40
    
    @staticmethod
    def explain_weights():
        """
        Generate human-readable explanation of weight system.
        
        Returns:
            str: Detailed explanation
        """
        explanation = """
FEATURE WEIGHT SYSTEM
====================

Purpose: Emphasize important dimensions in recommendation

Weight Distribution:
- Cognitive & Problem Solving (Q1-Q5): 1.2x importance
  * Problem solving, analysis, logical thinking, debugging, pattern recognition
  * Critical for technical roles
  
- Creativity & Innovation (Q6-Q10): 1.0x importance (baseline)
  * Creative ideation, design, visual thinking, ambiguity handling, innovation
  * Varies by role
  
- Communication & Leadership (Q11-Q15): 1.1x importance
  * Communication skills, presentation, mentoring, leadership, negotiation
  * Important for many roles
  
- Academic & Technical (Q16-Q20): 1.2x importance
  * Mathematics, research, programming, continuous learning
  * Critical for technical/scientific roles
  
- Forced Choices (Q21-Q25): 1.5x importance (HIGHEST)
  * Explicit preferences about work environment, problem types, values, style, success
  * These are the user's direct choices - weighted heavily
  
Implication:
User's explicit choices in Q21-Q25 have ~25% more influence than cognitive traits.
This ensures recommendations align with what user WANTS, not just what they're good at.
        """
        return explanation
