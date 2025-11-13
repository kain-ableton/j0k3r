===============================
Framework Optimization Plan
===============================

This document summarizes actionable optimizations and long-term enhancements for the Jok3r
framework.  It highlights concrete code locations so contributors can jump directly to the
relevant modules.

Execution pipeline and orchestration
====================================

*Parallelize target execution.* ``AttackController.run`` feeds every target sequentially into
:mod:`lib.core.AttackScope` and waits for each ``ServiceChecks.run`` loop to finish before
moving on (see ``lib/controller/AttackController.py`` and ``lib/core/AttackScope.py``).  A
small job-queue (e.g., :mod:`concurrent.futures` with a per-service concurrency cap) would
let I/O-bound commands execute in parallel while keeping long-running exploits isolated.

*Cache recurring reconnaissance.* ``AttackScope.attack`` triggers ``Target.smart_check`` each
pass to refresh DNS, availability, and fingerprint data.  Persisting these results per target
in the database (``lib/db`` models) and tagging their freshness would avoid redundant nmap
and Wappalyzer runs when the same host is attacked repeatedly.

*Add resumable sessions.* Session persistence already stores CLI arguments, but the run-time
state of the progress bars lives only in memory.  Persisting ``self.current_targetid`` and the
last completed check into the mission database would allow ``jok3r.py`` to resume after an
interruption instead of restarting the entire mission.

Check engine and toolbox management
===================================

*Model dependencies explicitly.* ``lib/core/ServiceChecks.py`` currently iterates over every
registered check and relies on ad-hoc context guards inside each check class.  Declaring
required credentials, products, and network conditions inside ``settings/*.conf`` (or per
``lib/core/Check`` instance) would let the engine short-circuit impossible checks up front and
provide better explanations to the operator.

*Expose resource usage hints.* Because the toolbox mixes scanners (e.g., ``davscan``) and
exploit scripts (configured in ``settings/toolbox.conf``), long-running commands can starve the
queue.  Capturing metadata such as expected duration, bandwidth usage, and whether the command
is destructive lets the scheduler throttle or serialize risky modules automatically.

*Containerize auxiliary tooling.* Several scripts (``webshells/``, ``toolbox/`` binaries) rely on
system-wide dependencies.  Shipping lightweight OCI images for groups of tools keeps host
systems clean and prevents dependency drift between Docker and bare-metal installs.

Smart modules and context awareness
===================================

*Centralize pattern updates.* The ``lib/smartmodules/matchstrings`` tree mixes credentials,
products, options, and vulnerability fingerprints.  Consolidating the matchers into a versioned
registry (e.g., JSON/YAML bundles) simplifies external contributions and paves the way for
automatic updates without touching the Python source tree.

*Introduce probabilistic scoring.* SmartModules currently match literal strings.  Adding
weighted scores (tf-idf or Bayesian filters) to each pattern would prioritize high-confidence
fingerprints and reduce false positives that trigger irrelevant checks.

*Leverage passive data sources.* The existing ``ServicesRequester`` flow already merges Nmap,
Shodan, and SmartStart discoveries into the mission database.  Incorporating additional passive
feeds (Censys, Project Sonar) through asynchronous importers would enrich targets before the
first active probe is launched.

CLI, UX, and workflow
=====================

*Improve argument discovery.* ``lib/core/ArgumentsParser.py`` now normalizes CSV inputs and wires
``--custom-cmd`` into ``AttackScope``.  Generating dynamic help text from ``settings/*.conf``
(e.g., showing which services honor ``--users`` or ``--products``) would reduce guesswork for
new operators.

*Surface reverse-shell requirements earlier.* ``ServiceChecks.__run_standard_mode`` annotates the
status bar when a check needs a callback, but the information appears only after the target is
queued.  Grouping all reverse-shell-dependent checks up front per target would let the CLI warn
users when ``--net=host`` or port-forwarding is mandatory.

*Offer dry-run and estimation modes.* A ``--plan`` flag could traverse ``ServiceChecks`` without
launching commands, summarize the estimated runtime (based on metadata above), and list required
credentials/options.  This would be invaluable for mission planning and stakeholder approvals.

Data, reporting, and observability
==================================

*Structured logging.* ``lib/output/Logger`` currently emits human-formatted strings.  Adding a
parallel JSON log (or OpenTelemetry span) per command execution would simplify downstream
analysis, alerting, and SIEM ingestion.

*Central result index.* Outputs are stored in SQLite tables managed by ``ResultsRequester`` and
``ServicesRequester``.  Creating a lightweight ORM repository that exposes consolidated views
(e.g., "all critical vulns across missions") would improve reporting and reduce the need for raw
SQL in custom tooling.

*Artifact management.* Commands often generate loot (e.g., downloaded files, screenshots).  A
standardized artifact directory per target, coupled with manifest files, would make report
assembly deterministic and friendlier to version control.

Testing, CI, and release automation
===================================

*Unit-test critical utilities.* Modules such as ``lib/utils/CommandTemplate.py`` and the CSV
normalizer in ``ArgumentsParser`` are pure functions that can be fuzz-tested quickly.  Building a
``pytest`` suite with fixtures for fake missions would catch regressions before long attack runs.

*Smoke-test docker images.* Every change to ``settings/toolbox.conf`` should trigger a Github
Actions workflow that builds the Docker image, runs ``python -m compileall`` (already used
locally), and executes a handful of representative checks against instrumented services.

*Versioned wordlists and configs.* The ``wordlists/`` directory and ``settings/*.conf`` files
should be validated via schema tests, ensuring new entries include descriptions, categories, and
compatibility metadata.

Security and extensibility
==========================

*Secret management.* ``apikeys.py`` is currently committed to the repo as a template.  Integrating
Hashicorp Vault or environment-based secret injection into ``jok3r.py`` would prevent accidental
key leaks and simplify CI deployments.

*Plugin SDK.* Documenting a stable API layer (``Check``, ``Command``, ``AttackProfile``) and
scaffolding generator would encourage third-party modules without requiring contributors to read
the entire codebase.

*Signed tool downloads.* When running ``update.py`` or ``update.sh``, verify tool archives via
SHA256 or GPG signatures to ensure the toolbox cannot be poisoned via MITM attacks.
