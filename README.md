# Project Mockingbird

## 🔍 Overview
Project Mockingbird is an accelerated, machine learning initiative to enhance Cyber Defence testing capabilities. It addresses the risk of using real production data to test SIEM (Microsoft Sentinel) detection rules, which can expose Personally Identifiable Information (PII) and violate data privacy policies.

## Approach
A Tabular Generative Adversarial Network (CTGAN) ingests a sanitized sample of real security logs and generates thousands of realistic, purely synthetic logs. This gives the SOC team a mathematically accurate, zero-risk environment for continuous testing and validation of detection logic.

## Disclaimer
Just as other birds are fooled by a mockingbird's call, the SIEM (Microsoft Sentinel) and security detection rules will be "fooled" into triggering alerts by the synthetic logs — proving the accuracy of the mimicry.

## ✅ Success Metrics

| Category | Measurement of Success |
|---|---|
| **Data Fidelity** | Synthetic data achieves a minimum Quality Score of 80% using the SDMetrics evaluation suite (comparing column shapes and pair trends against real data). |
| **Formatting** | 100% of generated IP addresses, timestamps, and usernames match the structural format of the original dataset. |
| **Integration** | The synthetic .csv is successfully ingested into a Microsoft Sentinel Custom Log workspace (`_CL`) without parsing errors. |
| **Validation** | The SOC team successfully triggers at least one existing SIEM analytic rule using the synthetic log data. |


# ➡️ Project Workflow 
<img width="5495" height="7268" alt="Data Ingestion and-2026-10-12-055624" src="https://github.com/user-attachments/assets/3fb397ec-5883-48ac-ab3b-ecc4b4fce576" />

## 📄 Full Project Write-Up

The complete report is available here: **[Project Mockingbird – Write-Up (PDF)](docs/Project_Mockingbird_Report.pdf)**


## 🖥️ Tech Stack
 
| Category | Technology |
|---|---|
| **Language** | Python |
| **ML Model** | CTGAN (Conditional Tabular GAN) |
| **Evaluation** | SDMetrics |
| **SIEM** | Microsoft Sentinel |
| **Query Language** | KQL (Kusto Query Language) |
| **Log Storage** | Azure Log Analytics Workspace (Custom Log table `_CL`) |
| **Ingestion** | Logs Ingestion API, Data Collection Rule (DCR) |
| **Data Transfer** | Azure Storage Account over SFTP |
| **Environment** | Ubuntu VM on VMware |

 
## 📊 Sample Data
 
Windows `SecurityEvent` logs (sanitized; tenant ID shortened here).
 
| TenantId | TimeGenerated | Account | AccountType | Computer | EventSourceName | Channel | Task | EventID | Activity |
|---|---|---|---|---|---|---|---|---|---|
| 6618e8e6-… | 2026-09-15T13:02:59Z | Account16 | Machine | 10.168.5.31 | Microsoft-Windows-Security-Auditing | Security | 12544 | 4624 | 4624 - An account was successfully logged on. |
| 6618e8e6-… | 2026-09-15T12:05:16Z | Account31 | User | 10.168.5.46 | Microsoft-Windows-Security-Auditing | Security | 12544 | 4625 | 4625 - An account failed to log on. |
 
## My Role
 
I designed and built an end-to-end pipeline that trains a CTGAN model on sanitized Windows security events and generates realistic synthetic logs. I then ingested those logs into Microsoft Sentinel to test and validate detection rules without exposing real data.
 
## ⚠️ Limitations
 
- The CTGAN model is built only for Windows `SecurityEvent` logs and does not work with other log types.
- It requires pre-processing of the input data and post-processing of the generated output.
  
## Future Work
 
I plan to extend the model to accept other Microsoft Sentinel log types, such as `SigninLogs` and `DeviceEvents`.
