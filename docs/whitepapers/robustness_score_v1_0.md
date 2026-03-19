# Technical Specification
## Robustness Score — Version 1.0

Date: 24 February 2026  
Status: Active Conceptual Framework  
Applies to: Standard Build (Community), Journey Edition, Enterprise Edition  

---

## 1. Purpose

The Robustness Score (RS) is a composite metric designed to rank machine learning models based on performance stability under uncertainty rather than isolated peak performance.

It replaces single-metric ranking (e.g., highest accuracy) with a stability-aware decision framework.

---

## 2. Core Principle

A model is not superior because it achieves the highest metric.

A model is superior because it sustains performance across variations in data sampling and perturbation.

---

## 3. Conceptual Formula

RS = M - (k₁ × σ_seed) - (k₂ × Gap_penalty) - (k₃ × Leak_penalty) - (k₄ × Instability_penalty)

Where:

- M = Mean validation metric (e.g., AUC, F1, Accuracy, RMSE)
- σ_seed = Standard deviation across multiple random seeds
- Gap_penalty = Penalty for train vs validation discrepancy
- Leak_penalty = Penalty for suspected data leakage indicators
- Instability_penalty = Penalty from stress testing (if applicable)
- k₁..k₄ = Risk profile coefficients

---

## 4. Components

### 4.1 Mean Validation Metric (M)

Primary evaluation metric derived from cross-validation.

For classification:
- AUC (default)
- F1 (if imbalance critical)
- Accuracy (fallback)

For regression:
- RMSE (primary)
- R² (secondary reference)

---

### 4.2 Multi-Seed Variance (σ_seed)

Procedure:
- Run training with N different random seeds (default N=5 Community, N=7–15 Enterprise).
- Compute standard deviation of validation metric.

Interpretation:
- Low σ → Stable model
- High σ → Order-sensitive model (potential overfitting)

---

### 4.3 Train–Validation Gap

Gap = Train_metric - Validation_metric

If Gap > threshold (default 0.05):
- Apply proportional penalty.

If Gap > critical_threshold (default 0.10):
- Flag as high overfitting risk.

---

### 4.4 Leakage Penalty

Triggered when:

- Feature correlation with target > 0.95
- Extremely high mutual information
- High-cardinality near-unique features strongly predictive
- Post-event features detected (heuristic naming patterns)

Penalty severity:
- Mild (warning)
- Severe (Quality Gate activation)

---

### 4.5 Stress Instability Penalty (Journey/Enterprise)

Applied after perturbation tests:

- Noise injection (±2%)
- Row dropout (5%)
- Feature removal test

If performance drop > stress_threshold:
- Apply penalty or block deployment.

---

## 5. Risk Profiles

### Conservative
- Higher k values
- Strong penalty weighting
- Intended for critical infrastructure

### Balanced (Default)
- Moderate penalties
- Suitable for most enterprise applications

### Aggressive
- Lower penalties
- Allows higher risk tolerance
- Experimental use

---

## 6. Ranking Mechanism

Models are ranked by descending Robustness Score (RS).

The highest RS becomes:

Champion Model — Stability Approved

Not necessarily highest raw metric.

---

## 7. Deployment Rules

Community:
- RS influences ranking
- Alerts displayed
- No automatic block

Journey:
- RS influences ranking
- Stress Test enabled
- Conditional deployment warnings

Enterprise:
- Full RS enforcement
- Stress Test mandatory
- Quality Gate may block deployment

---

## 8. Governance Integration

RS is logged into:

- Run metadata
- Model contract
- PDF report
- Audit trail (Enterprise)

This ensures traceable decision logic.

---

## 9. Strategic Impact

Robustness Score transforms OpenCanvas Pro from:

Metric optimization platform

to

Stability-oriented decision infrastructure.

---

## 10. Intellectual Property Notice

The precise weighting mechanisms, heuristics, and internal calibration logic are proprietary.

This document describes conceptual structure only.

---

© 2026 OpenCanvas Pro  
All rights reserved.
