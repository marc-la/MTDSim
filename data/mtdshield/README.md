# MTDShield agent weights

`main_network_epsilon_0.5_decay_0.99__0848c2e2d5b7.h5` is the trained MTDShield
agent Chapter 5 evaluates (Appendix E): Tay's highest-scoring agent
(epsilon 0.5, decay 0.99), run as released.

- **Source:** Joo Kai Tay, commit `f13ed49a` (2024-09-23, "Added models for gamma"),
  file `experiments/AI_model/main_network_epsilon_0.5_decay_0.99.h5`. The copy
  here is byte-identical to it.
- **SHA-256:** `8ab379779679075aff036ace8b34d31e3eeadc0e933dc3b42f7441efe06deb73`
- **Read by:** `experiments/ch5_defended/run_corpus.py` (`AGENT`), through
  `src/mtdnetwork/mtdai/mtd_ai.py`'s released 8/3 input layout.
