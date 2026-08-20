# Trace the Ace — Competition Contract

Source of record: https://platform.k12-ai-infrastructure.org/competitions/3/tutoring-outcomes/

Verified against the official competition site on **2026-08-20**.

This file records external constraints. Changes in the competition website should update this contract before they affect experiments.

## Task

Given a tutoring-session transcript and a short learning-objective description, predict the probability that the student answers the next assessment question on the same topic correctly.

The target is a downstream tutoring outcome, not a tutor-quality label and not transcript similarity.

## Data Shape

Training metadata includes:

```text
response_id
session_id
learning_objective
```

Each `session_id` maps to a transcript containing ordered tutor/student utterances with content and timestamps.

Training labels are binary:

```text
correct = 0.0 | 1.0
```

A single tutoring session may correspond to multiple response samples when multiple learning objectives were completed.

### Validation consequence

Because multiple samples can share the same transcript, ordinary response-level random splitting can leak session information across train and validation.

The default CEA validation contract is therefore:

```text
train_session_ids ∩ validation_session_ids = ∅
```

Use grouped splitting by `session_id` unless a later experiment explicitly justifies another split.

## Official Metric

Primary ranking metric:

```text
LogLoss = -(y log(p) + (1-y) log(1-p))
```

Lower is better.

ROC AUC may be displayed for reference but does not determine leaderboard position.

Consequences:

- predictions must be probabilities, not hard labels;
- calibration is part of performance;
- confident errors receive large penalties.

## Submission Contract

This is a code-execution competition.

Submissions package the trained model and inference code for containerized evaluation. Inference-time internet access is unavailable.

Unless otherwise specified by the organizers:

```text
one test sample must be processed independently of other test samples
```

The rules prohibit using information gathered across test cases as feature inputs or target labels for training, including pseudo-labeling or unsupervised learning on the test set.

Eligible models must run automatically on new test data without retraining.

For CEA this creates a useful firewall:

```text
development-time corrective learning ≠ held-out test-time adaptation
```

## External Data / Models

External datasets and pretrained models are allowed subject to the competition's licensing rules.

For prize eligibility, resources used to train or run the submitted solution must permit the required broad/commercial use. Finalists must declare external data and pretrained models used.

Winning solutions must be released under the MIT License under the stated competition rules.

All candidate external resources must therefore enter the CEA ledger with an explicit license/provenance record before use in a prize-eligible submission.

## Timeline

```text
Model submissions close: 2026-08-27 23:59 UTC
Top-15 write-up window:   2026-08-27 → 2026-09-15
Write-ups close:          2026-09-15
```

The competition awards are not based on leaderboard rank alone: the top 15 are invited to a write-up phase, and final prizes combine predictive performance with write-up quality.

## Scientific Boundary

Official leaderboard adjudication can establish external predictive performance under the competition protocol.

It cannot, by itself, establish:

```text
CLPR mechanism
AIEC mechanism
persistent-learning mechanism
Issue #44 necessity
CEA compositional synergy
open-ended improvement
```

Those require separate discriminating experiments recorded in this directory.
