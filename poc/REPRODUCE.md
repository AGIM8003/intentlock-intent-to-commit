# Reproduce IntentLock v6.0.0 evidence

```bash
cd poc
python intentlock_poc.py
python intentlock_gate.py
python intentlock_benchmark.py
python intentlock_alt_impl.py
python intentlock_mutation_test.py
python intentlock_stress.py
python intentlock_realworld.py
python intentlock_integration_test.py
python intentlock_quickstart.py
```

All scripts are stdlib-only. Expected: every script exits 0; Reality Gate 8/8; mutation kill rate ≥ 90%.
