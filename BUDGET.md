# Budget Note — Cloud Services

All frameworks in this repo run on **local simulators** by default. Cloud
access is optional and only needed to run on real quantum hardware.

| Service | Free tier | Pay-as-you-go |
|---|---|---|
| **IBM Quantum** | 10 min/month on real QPU, unlimited simulator | Free for small usage |
| **AWS Braket** | 1 hr/month SV1/DM1/TN1 simulators free | QPU: ~$0.30/task + $0.01/shot |
| **D-Wave Leap** | 1 min/month QPU + hybrid solver free credits | Very cheap for small problems |
| **Rigetti QCS** | Free QVM simulator | QPU on request |
| **Azure Quantum** | Credits for new accounts | Varies by provider |

## Tips

- Start with local simulators — they are free and sufficient for learning.
- IBM Quantum has the most generous free tier for real QPU time.
- AWS Braket charges per task + per shot; keep shots low during experiments.
- D-Wave Leap free credits expire monthly; use them or lose them.
- Azure Quantum offers credits for new subscribers; check current offers.
