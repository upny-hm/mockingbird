# Project Mockingbird 🐦

## Overview
Project Mockingbird is an accelerated, 6-8 week machine learning initiative to enhance Cyber Defence testing capabilities. It addresses the risk of using real production data to test SIEM (Microsoft Sentinel) detection rules, which can expose Personally Identifiable Information (PII) and violate data privacy policies.

## Approach
A Tabular Generative Adversarial Network (CTGAN) ingests a sanitized sample of real security logs and generates thousands of realistic, purely synthetic logs. This gives the SOC team a mathematically accurate, zero-risk environment for continuous testing and validation of detection logic.

## Disclaimer
Just as other birds are fooled by a mockingbird's call, the SIEM (Microsoft Sentinel) and security detection rules will be "fooled" into triggering alerts by the synthetic logs — proving the accuracy of the mimicry.

## Success Metrics

| Category | Measurement of Success |
|---|---|
| **Data Fidelity** | Synthetic data achieves a minimum Quality Score of 80% using the SDMetrics evaluation suite (comparing column shapes and pair trends against real data). |
| **Formatting** | 100% of generated IP addresses, timestamps, and usernames match the structural format of the original dataset. |
| **Integration** | The synthetic .csv is successfully ingested into a Microsoft Sentinel Custom Log workspace (`_CL`) without parsing errors. |
| **Validation** | The SOC team successfully triggers at least one existing SIEM analytic rule using the synthetic log data. |
