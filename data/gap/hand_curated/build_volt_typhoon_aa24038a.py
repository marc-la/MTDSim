#!/usr/bin/env python3
"""Hand-curated Attack Flow for Volt Typhoon, built from CISA AA24-038A.

Provenance
----------
Sole source: joint Cybersecurity Advisory **AA24-038A**, "PRC State-Sponsored
Actors Compromise and Maintain Persistent Access to U.S. Critical
Infrastructure" (CISA, NSA, FBI, with DOE, EPA, TSA, ASD's ACSC, CCCS,
NCSC-UK, NCSC-NZ), first published 8 Feb 2024. Text read from the ASD's ACSC
republication (cyber.gov.au); cisa.gov returns HTTP 403 to automated retrieval.

This is a *hand-authored* Attack Flow (``source: hand_curated``), NOT a MITRE
CTID corpus flow. It is deliberately kept OUT of the canonical GAP corpus
(``data/gap/_corpus_stix/`` -> ``data/gap/flows/``): wiring it into the L1 build
is a membership ruling reserved for Marc (gap_schema.md Decision 6), not taken
here. It exists as a ch3 evidence/figure artefact per the ratified "Version A"
plan (a hand-curated real-incident flow beside the corpus, never inside it).

Fidelity contract
-----------------
- **Technique set** == the advisory's Appendix C (Tables 5-17): every technique
  the advisory maps is a node, at the sub-technique granularity it is drawn.
  ``tactic_id`` is the tactic of the Appendix table the technique appears under
  (the advisory's own formal mapping), even where ATT&CK lists the technique
  under several tactics.
- **Edges** encode ONLY orderings the advisory states or directly implies. Each
  edge carries a ``basis`` note quoting/paraphrasing the supporting sentence and
  a ``kind``: ``stated`` (the advisory asserts the order) or ``inferred`` (a
  causal dependency the advisory's mechanism entails but does not spell out as a
  sequence). No edge rests on analyst intuition beyond the cited text.
- **No fabricated objective.** The advisory is explicit that Volt Typhoon
  pre-positions and does NOT execute destructive action ("minimal activity ...
  objective is to maintain persistence"). The terminal node is therefore an
  ``attack-condition`` end-state, not an Impact technique.
- Speculative/low-confidence advisory claims (the Azure/cloud branch;
  Pass-the-Hash/Ticket "may be capable") are included but flagged in-node.

ATT&CK version note
-------------------
The advisory maps against ATT&CK v14. The repo pins Enterprise v19.1. Two
deltas are recorded but NOT silently rewritten (the flow is faithful to the
advisory as drawn): T1070.001 (Clear Windows Event Logs) is REVOKED in v19.1
(-> T1685.005); TA0005 was renamed Defense Evasion -> Stealth. Parent-collapse
targets (T1070, T1003, T1090, ...) all resolve in v19.1, so if this flow were
ever admitted to the corpus the Enterprise-scope check would still pass on
parents. Flagged for the reader; not a defect of this artefact.

Run
---
    PYTHONPATH=src python3 data/gap/hand_curated/build_volt_typhoon_aa24038a.py

Emits, in this directory:
    volt_typhoon_aa24038a.json   -- STIX 2.1 Attack Flow bundle (canonical form)
    volt_typhoon_aa24038a.yaml   -- per-flow extract, produced by the repo's own
                                    parser from the bundle (round-trip proof)
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
NS = uuid.uuid5(uuid.NAMESPACE_URL, "mtdsim:hand_curated:volt_typhoon_aa24038a")
AF_EXT = "extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4"

# Tactic external-id -> STIX tactic_ref (from data/gap/_attack/enterprise-attack-19.1.json).
TACTIC_REF = {
    "TA0043": "x-mitre-tactic--daa4cbb1-b4f4-4723-a824-7f1efd6e0592",  # reconnaissance
    "TA0042": "x-mitre-tactic--d679bca2-e57d-4935-8650-8031c87a4400",  # resource-development
    "TA0001": "x-mitre-tactic--ffd5bcee-6e16-4dd2-8eca-7b3beedf33ca",  # initial-access
    "TA0002": "x-mitre-tactic--4ca45d45-df4d-4613-8980-bac22d278fa5",  # execution
    "TA0003": "x-mitre-tactic--5bc1d813-693e-4823-9961-abf9af4b0e92",  # persistence
    "TA0004": "x-mitre-tactic--5e29b093-294e-49e9-a803-dab3d73b77dd",  # privilege-escalation
    "TA0005": "x-mitre-tactic--78b23412-0651-46d7-a540-170a1ce8bd5a",  # defense-evasion / stealth
    "TA0006": "x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263",  # credential-access
    "TA0007": "x-mitre-tactic--c17c5845-175e-4421-9713-829d0573dbc9",  # discovery
    "TA0008": "x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e",  # lateral-movement
    "TA0009": "x-mitre-tactic--d108ce10-2419-4cf9-a774-46161d6c6cfe",  # collection
    "TA0011": "x-mitre-tactic--f72804c5-f15a-449e-a5da-2eecd181f813",  # command-and-control
    "TA0010": "x-mitre-tactic--9a4e74ab-5008-408c-84bf-a10dfbc53462",  # exfiltration
}

# ---------------------------------------------------------------------------
# ACTIONS  key: (technique_id as drawn, tactic_id, name, description)
# The description is the advisory's own use-sentence (paraphrased short), so the
# emitted bundle is self-documenting. "name" is the ATT&CK technique title.
# ---------------------------------------------------------------------------
A = {}
def act(key, tid, tactic, name, desc):
    A[key] = dict(tid=tid, tactic=tactic, name=name, desc=desc)

# -- Reconnaissance (Table 5) ------------------------------------------------
act("recon_org",   "T1591",     "TA0043", "Gather Victim Org Information",
    "Extensive pre-compromise reconnaissance to learn about the target organization.")
act("recon_net",   "T1590",     "TA0043", "Gather Victim Network Information",
    "Pre-compromise reconnaissance to learn the target's network topology and protocols.")
act("recon_staff", "T1589",     "TA0043", "Gather Victim Identity Information",
    "Pre-compromise reconnaissance on staff, especially key network and IT administrators.")
act("recon_host",  "T1592",     "TA0043", "Gather Victim Host Information",
    "Web searches for victim host information.")
act("recon_search","T1593",     "TA0043", "Search Open Websites/Domains",
    "Uses FOFA, Shodan, and Censys to search for exposed infrastructure.")
act("recon_owned", "T1594",     "TA0043", "Search Victim-Owned Websites",
    "Searches victim-owned sites for host, identity, and network information.")

# -- Resource Development (Table 6) -----------------------------------------
act("rd_vps",      "T1583.003", "TA0042", "Acquire Infrastructure: Virtual Private Server",
    "Multi-hop C2 proxy composed of virtual private servers (VPSs).")
act("rd_botnet",   "T1584.005", "TA0042", "Compromise Infrastructure: Botnet",
    "Cisco and NETGEAR end-of-life SOHO routers implanted with KV Botnet malware.")
act("rd_server",   "T1584.004", "TA0042", "Compromise Infrastructure: Server",
    "Converted a compromised PRTG server into a proxy for C2 traffic.")
act("rd_dev_exp",  "T1587.004", "TA0042", "Develop Capabilities: Exploits",
    "Adept at discovering and exploiting zero-day vulnerabilities.")
act("rd_obt_exp",  "T1588.005", "TA0042", "Obtain Capabilities: Exploits",
    "Uses publicly available exploit code for known vulnerabilities.")

# -- Initial Access (Table 7) -----------------------------------------------
act("ia_exploit",  "T1190",     "TA0001", "Exploit Public-Facing Application",
    "Exploits vulnerabilities in networking appliances (Fortinet, Ivanti, NETGEAR, Citrix, Cisco); "
    "one confirmed case exploited CVE-2022-42475 in an unpatched FortiGate 300D.")
act("ia_vpn",      "T1133",     "TA0001", "External Remote Services",
    "Connects to the victim network via VPN sessions for discreet follow-on activity.")

# -- Execution (Table 8) -----------------------------------------------------
act("ex_cli",      "T1059",     "TA0002", "Command and Scripting Interpreter",
    "Hands-on-keyboard execution via the command-line.")
act("ex_ps",       "T1059.001", "TA0002", "Command and Scripting Interpreter: PowerShell",
    "Executes FRP clients and scripts via PowerShell.")
act("ex_unix",     "T1059.004", "TA0002", "Command and Scripting Interpreter: Unix Shell",
    "Brightmetricagent.exe CLI library can leverage PowerShell, WMI, and Z Shell.")
act("ex_wmi",      "T1047",     "TA0002", "Windows Management Instrumentation",
    "WMIC commands execute ntdsutil to copy NTDS.dit and the SYSTEM hive from a shadow copy.")

# -- Persistence (Table 9) ---------------------------------------------------
act("pers_valid",  "T1078",     "TA0003", "Valid Accounts",
    "Primarily relies on valid credentials for persistence.")

# -- Privilege Escalation (Table 10) ----------------------------------------
act("pe_exploit",  "T1068",     "TA0004", "Exploitation for Privilege Escalation",
    "Obtains credentials from public-facing appliances by exploiting privilege-escalation "
    "vulnerabilities in the OS or network services.")

# -- Defense Evasion (Table 11) ---------------------------------------------
act("de_vss",      "T1006",     "TA0005", "Direct Volume Access",
    "Executes the Windows-native vssadmin command to create a volume shadow copy.")
act("de_clearwin", "T1070.001", "TA0005", "Indicator Removal: Clear Windows Event Logs",
    "Selectively clears Windows Event Logs to remove evidence. (v19.1: revoked -> T1685.005.)")
act("de_delete",   "T1070.004", "TA0005", "Indicator Removal: File Deletion",
    "Created systeminfo.dat in C:\\Users\\Public\\Documents, then deleted it.")
act("de_clearpers","T1070.009", "TA0005", "Indicator Removal: Clear Persistence",
    "Clears system logs and other technical artifacts to remove intrusion evidence.")
act("de_masq",     "T1036.005", "TA0005", "Masquerading: Match Legitimate Name or Location",
    "Masquerades file names; downloaded comsvcs.dll to a non-standard folder.")
act("de_reg",      "T1112",     "TA0005", "Modify Registry",
    "Uses netsh to create a PortProxy registry modification on the PRTG server.")
act("de_pack",     "T1027.002", "TA0005", "Obfuscated Files or Information: Software Packing",
    "Packed FRP clients and ScanLine with UPX.")
act("de_lolbin",   "T1218",     "TA0005", "System Binary Proxy Execution",
    "LOTL / LOLBins: native tools and processes to maintain and expand access.")

# -- Credential Access (Table 12) -------------------------------------------
act("ca_unsecured","T1552",     "TA0006", "Unsecured Credentials",
    "Obtained a domain-admin credential insecurely stored on the appliance.")
act("ca_privkey",  "T1552.004", "TA0006", "Unsecured Credentials: Private Keys",
    "Accessed the Chrome Local State file holding the AES key that decrypts stored passwords.")
act("ca_lsass",    "T1003.001", "TA0006", "OS Credential Dumping: LSASS Memory",
    "Used comsvcs.dll MiniDump with the LSASS PID to dump LSASS process memory.")
act("ca_ntds",     "T1003.003", "TA0006", "OS Credential Dumping: NTDS",
    "Extracts the Active Directory database (NTDS.dit) from the DC -> full domain compromise.")
act("ca_crack",    "T1110.002", "TA0006", "Brute Force: Password Cracking",
    "Exfiltrates NTDS.dit and the SYSTEM hive to crack passwords offline.")
act("ca_stores",   "T1555",     "TA0006", "Credentials from Password Stores",
    "Harvests saved passwords, history, and cookies from browsers.")
act("ca_browser",  "T1555.003", "TA0006", "Credentials from Web Browsers",
    "Targets network-administrator browser history and stored credentials.")

# -- Discovery (Table 13) ----------------------------------------------------
act("di_sysinfo",  "T1082",     "TA0007", "System Information Discovery",
    "LOTL utilities for system-information discovery.")
act("di_netsvc",   "T1046",     "TA0007", "Network Service Discovery",
    "LOTL utilities for network-service discovery.")
act("di_groups",   "T1069",     "TA0007", "Permission Groups Discovery",
    "LOTL utilities for group discovery.")
act("di_owner",    "T1033",     "TA0007", "System Owner/User Discovery",
    "LOTL utilities for user discovery.")
act("di_files",    "T1083",     "TA0007", "File and Directory Discovery",
    "Enumerated directories containing vulnerability-testing content and facilities data.")
act("di_proc",     "T1057",     "TA0007", "Process Discovery",
    "Executed tasklist /v for a detailed process listing.")
act("di_localacct","T1087.001", "TA0007", "Account Discovery: Local Account",
    "Executed net user and quser for account information.")
act("di_netconf",  "T1016.001", "TA0007", "Internet Connection Discovery",
    "Employs ping with various IPs to check network connectivity.")
act("di_svc",      "T1007",     "TA0007", "System Service Discovery",
    "Uses net start to list running services.")
act("di_window",   "T1010",     "TA0007", "Application Window Discovery",
    "rult3uil.log captured window-title information and focus shifts.")
act("di_logenum",  "T1654",     "TA0007", "Log Enumeration",
    "Captured successful logon events (Event ID 4624) via PowerShell queries.")
act("di_query",    "T1012",     "TA0007", "Query Registry",
    "Enumerated stored PuTTY sessions.")
act("di_software", "T1518",     "TA0007", "Software Discovery",
    "Obtained the victim's list of installed applications.")
act("di_periph",   "T1120",     "TA0007", "Peripheral Device Discovery",
    "Obtained screen dimension and display-device information.")
act("di_loc",      "T1614",     "TA0007", "System Location Discovery",
    "Obtained the victim's system locale.")
act("di_time",     "T1124",     "TA0007", "System Time Discovery",
    "Obtained the victim's system timezone.")
act("di_browserinfo","T1217",   "TA0007", "Browser Information Discovery",
    "Enumerated browser history and stored data.")

# -- Lateral Movement (Table 14) --------------------------------------------
act("lm_rdp",      "T1021.001", "TA0008", "Remote Services: Remote Desktop Protocol",
    "Moves laterally to the DC via an interactive RDP session with a domain-admin account.")
act("lm_hijack",   "T1563",     "TA0008", "Remote Service Session Hijacking",
    "PuTTY profiles for water-treatment, wells, a substation, and OT systems would enable "
    "access to those critical systems.")
act("lm_cloud",    "T1021.007", "TA0008", "Remote Services: Cloud Services",
    "[Attribution inconclusive] anomalous login attempts to an Azure tenant.")
act("lm_altauth",  "T1550",     "TA0008", "Use Alternate Authentication Material",
    "[May be capable] Pass-the-Hash or Pass-the-Ticket after full AD compromise.")
act("lm_cloudacct","T1078.004", "TA0008", "Valid Accounts: Cloud Accounts",
    "[Attribution inconclusive] Azure logins potentially using credentials stolen via NTDS.dit.")

# -- Collection (Table 15) ---------------------------------------------------
act("col_archive", "T1560",     "TA0009", "Archive Collected Data",
    "Collected sensitive file-server information in multiple zipped files.")
act("col_util",    "T1560.001", "TA0009", "Archive Collected Data: Archive via Utility",
    "Compressed extracted NTDS.dit and registry hives with ronf.exe (a renamed rar.exe).")
act("col_staged",  "T1074",     "TA0009", "Data Staged",
    "Saved History.zip to the Downloads directory for exfiltration.")
act("col_screen",  "T1113",     "TA0009", "Screen Capture",
    "Captured a screenshot using gdi32.dll and gdiplus.dll.")

# -- Command and Control (Table 16) -----------------------------------------
act("c2_proxy",    "T1090",     "TA0011", "Proxy",
    "FRP clients establish covert C2 channels; SOHO routers and VPSs proxy C2 traffic.")
act("c2_internal", "T1090.001", "TA0011", "Proxy: Internal Proxy",
    "netsh PortProxy modification on the PRTG server redirects port traffic.")
act("c2_multihop", "T1090.003", "TA0011", "Proxy: Multi-hop Proxy",
    "Multi-hop proxies (VPSs / SOHO routers) for C2 infrastructure.")
act("c2_ingress",  "T1105",     "TA0011", "Ingress Tool Transfer",
    "Downloaded an outdated comsvcs.dll to the DC in a non-standard folder.")
act("c2_enc",      "T1573",     "TA0011", "Encrypted Channel",
    "FRP clients open reverse proxies establishing covert (encrypted) C2 channels.")

# -- Exfiltration (Table 17) -------------------------------------------------
act("ex_smb",      "T1048",     "TA0010", "Exfiltration Over Alternative Protocol",
    "Likely exfiltrated collected files via Server Message Block (SMB).")

# -- Post-compromise identity targeting (advisory: T1589.002 "post compromise")
act("recon_email", "T1589.002", "TA0043", "Gather Victim Identity Information: Email Addresses",
    "Post-compromise: targets the personal emails of key network and IT staff, informed by "
    "harvested browser data.")

# ---------------------------------------------------------------------------
# CONDITIONS
# ---------------------------------------------------------------------------
C = {
    "cond_entry": "A public-facing network appliance is unpatched and exploitable "
                  "(one confirmed case: CVE-2022-42475 in a FortiGate 300D).",
    "cond_objective": "Volt Typhoon is pre-positioned on the IT network with the capability to "
                      "reach OT assets; consistent with the advisory, no destructive OT action "
                      "is executed -- the objective is long-term, stealthy persistence.",
}

# ---------------------------------------------------------------------------
# OPERATORS
# ---------------------------------------------------------------------------
OPS = {
    "or_credsource": "OR",  # appliance priv-esc OR unsecured stored credential -> valid accounts
}

# ---------------------------------------------------------------------------
# EDGES  (src, dst, kind, basis)
#   kind: "stated"   -- advisory asserts this order/dependency
#         "inferred" -- causal dependency the advisory's mechanism entails
# Condition edges use on_true; everything else is an effect edge.
# ---------------------------------------------------------------------------
E = [
    # Recon precedes and informs initial access (Overview: recon "to learn about
    # the network" then "typically gains initial access").
    ("recon_org",   "ia_exploit", "stated",   "Overview: extensive pre-compromise recon precedes initial access."),
    ("recon_net",   "ia_exploit", "stated",   "Overview: recon of network topology precedes initial access."),
    ("recon_staff", "ia_exploit", "inferred", "Recon on staff feeds targeting; order into IA implied."),
    ("recon_host",  "ia_exploit", "inferred", "Host recon feeds targeting of the exploited appliance."),
    ("recon_search","ia_exploit", "stated",   "FOFA/Shodan/Censys search for exposed infrastructure precedes access."),
    ("recon_owned", "ia_exploit", "inferred", "Victim-owned-site search feeds targeting."),

    # Exploit capability is the means of initial access.
    ("rd_obt_exp",  "ia_exploit", "stated",   "IA section: uses publicly available exploit code for known vulns [T1588.005]."),
    ("rd_dev_exp",  "ia_exploit", "stated",   "IA section: also exploits zero-days [T1587.004]."),

    # Entry precondition -> exploit.
    ("cond_entry",  "ia_exploit", "stated",   "Confirmed compromise exploited CVE-2022-42475 in an unpatched FortiGate."),

    # Initial access -> VPN foothold; "and then connects to the victim's network via VPN".
    ("ia_exploit",  "ia_vpn",     "stated",   "'...and then connects to the victim's network via VPN for follow-on activities.'"),

    # Foothold -> credential sources on the appliance ("first obtain credentials
    # from public-facing appliances after gaining initial access").
    ("ia_exploit",  "pe_exploit", "stated",   "'...first obtain credentials from public-facing appliances after gaining initial access by exploiting privilege escalation vulnerabilities [T1068].'"),
    ("ia_exploit",  "ca_unsecured","stated",  "'In some cases, they have obtained credentials insecurely stored on the appliance [T1552].'"),

    # Either credential source -> valid accounts (OR).
    ("pe_exploit",  "or_credsource","stated", "Priv-esc yields admin credentials."),
    ("ca_unsecured","or_credsource","stated", "Stored appliance credential is an alternative source."),
    ("or_credsource","pers_valid", "stated",  "'Volt Typhoon primarily relies on valid credentials for persistence [T1078].'"),
    ("ia_vpn",      "pers_valid",  "inferred","VPN external remote service sustains the valid-account foothold."),

    # Valid accounts -> lateral move to DC via RDP.
    ("pers_valid",  "lm_rdp",      "stated",  "'uses valid administrator credentials to move laterally to the domain controller (DC) ... via ... RDP [T1021.001].'"),

    # NTDS.dit procedure (advisory's numbered steps), on the DC reached by RDP.
    ("lm_rdp",      "de_vss",      "stated",  "NTDS steps: after moving to the DC, 'Execute the Windows-native vssadmin [T1006] command to create a volume shadow copy'."),
    ("de_vss",      "ex_wmi",      "stated",  "'Use WMIC commands [T1047] to execute ntdsutil ... to copy NTDS.dit ... from the volume shadow copy.'"),
    ("ex_wmi",      "ca_ntds",     "stated",  "The ntdsutil copy is the NTDS.dit extraction [T1003.003]."),
    ("ca_ntds",     "ca_crack",    "stated",  "'Exfiltrate NTDS.dit and SYSTEM registry hive to crack passwords offline [T1110.002].'"),
    ("ca_ntds",     "ex_smb",      "inferred","NTDS.dit/SYSTEM hive exfiltration; advisory pairs exfil (SMB) with staged data."),
    ("ca_ntds",     "col_util",    "stated",  "'compressed and archived the extracted ntds.dit and registry files by executing ronf.exe [T1560.001].'"),

    # Alternative LSASS credential path.
    ("c2_ingress",  "ca_lsass",    "stated",  "'downloaded an outdated comsvcs.dll [T1105] ... used this DLL with MiniDump and the LSASS PID to dump LSASS memory [T1003.001].'"),
    ("de_masq",     "c2_ingress",  "inferred","comsvcs.dll placed in a non-standard folder (masquerading) precedes its use."),

    # Full domain compromise -> broader access toward OT.
    ("ca_crack",    "lm_hijack",   "stated",  "'uses elevated credentials for ... additional discovery, often focusing on gaining capabilities to access OT assets'; PuTTY profiles enable access to critical systems [T1563]."),
    ("di_query",    "lm_hijack",   "stated",  "Enumerated stored PuTTY sessions [T1012] gave potential access to OT PuTTY profiles."),

    # Speculative cloud branch (attribution inconclusive).
    ("ca_crack",    "lm_cloudacct","inferred","'Azure logins potentially using credentials previously compromised from theft of NTDS.dit' (attribution inconclusive)."),
    ("lm_cloudacct","lm_cloud",    "stated",  "Anomalous Azure-tenant login attempts [T1021.007] (attribution inconclusive)."),
    ("ca_crack",    "lm_altauth",  "inferred","'may be capable of using Pass-the-Hash or Pass-the-Ticket' after full AD compromise."),

    # Discovery fan-out from the valid-account foothold (LOTL).
    ("pers_valid",  "di_sysinfo",  "stated",  "'conducts discovery in the victim's network, leveraging LOTL binaries.'"),
    ("pers_valid",  "di_netsvc",   "stated",  "LOTL discovery (network service)."),
    ("pers_valid",  "di_groups",   "stated",  "LOTL discovery (groups)."),
    ("pers_valid",  "di_owner",    "stated",  "LOTL discovery (users)."),
    ("pers_valid",  "di_files",    "stated",  "Enumerated directories with facilities data [T1083]."),
    ("pers_valid",  "di_proc",     "stated",  "tasklist /v process discovery [T1057]."),
    ("pers_valid",  "di_localacct","stated",  "net user / quser account discovery [T1087.001]."),
    ("pers_valid",  "di_netconf",  "stated",  "ping connectivity checks [T1016.001]."),
    ("pers_valid",  "di_svc",      "stated",  "net start service listing [T1007]."),
    ("pers_valid",  "di_window",   "stated",  "rult3uil.log window-title capture [T1010]."),
    ("pers_valid",  "di_logenum",  "stated",  "PowerShell logon-event capture (4624) [T1654]."),
    ("pers_valid",  "di_query",    "stated",  "Enumerated stored PuTTY sessions [T1012]."),
    ("pers_valid",  "di_software", "stated",  "Installed-application discovery [T1518]."),
    ("pers_valid",  "di_periph",   "stated",  "Display-device discovery [T1120]."),
    ("pers_valid",  "di_loc",      "stated",  "System-locale discovery [T1614]."),
    ("pers_valid",  "di_time",     "stated",  "System-timezone discovery [T1124]."),
    ("pers_valid",  "di_browserinfo","stated","Browser-information discovery [T1217]."),
    ("pers_valid",  "ex_cli",      "stated",  "'hands-on-keyboard activity via the command-line [T1059].'"),
    ("ex_cli",      "de_lolbin",   "stated",  "'other native tools and processes on systems [T1218]' (LOTL) alongside CLI."),

    # Browser-credential path.
    ("di_browserinfo","ca_browser","stated",  "Browser-info discovery precedes targeting stored browser credentials [T1555.003]."),
    ("ca_browser",  "ca_stores",   "inferred","Web-browser credentials are a password-store source [T1555]."),
    ("ca_browser",  "col_staged",  "stated",  "'saved History.zip in the Downloads directory for exfiltration [T1074].'"),
    ("ca_browser",  "ca_privkey",  "stated",  "'accessed the Local State file [that] contains the AES encryption key [T1552.004].'"),
    ("ca_browser",  "recon_email", "stated",  "Browser data used '...to facilitate targeting of personal email addresses [T1589.002].'"),
    ("col_staged",  "col_archive", "inferred","Staged data archived into zipped files [T1560]."),

    # Collection -> exfiltration.
    ("col_archive", "ex_smb",      "stated",  "'collected ... in multiple zipped files [T1560] and likely exfiltrated ... via SMB [T1048].'"),
    ("di_files",    "col_archive", "stated",  "Collected OT diagrams/documentation from the file server."),
    ("di_periph",   "col_screen",  "inferred","Display discovery accompanies screen capture [T1113]."),

    # Defense evasion applied across the intrusion (log clearing after activity).
    ("ca_ntds",     "de_clearwin", "stated",  "'selectively cleared Windows Event Logs [T1070.001]' to remove evidence."),
    ("de_clearwin", "de_clearpers","stated",  "Clears system logs / persistence artifacts [T1070.009]."),
    ("di_logenum",  "de_delete",   "stated",  "systeminfo.dat created then deleted [T1070.004]."),
    ("ca_ntds",     "de_masq",     "inferred","Masqueraded file names accompany the intrusion."),

    # C2 infrastructure -> proxy channel.
    ("rd_botnet",   "c2_multihop", "stated",  "SOHO-router botnet supports multi-hop proxy C2 [T1090.003]."),
    ("rd_vps",      "c2_multihop", "stated",  "VPSs compose the multi-hop C2 proxy [T1090.003]."),
    ("rd_server",   "c2_internal", "stated",  "Compromised PRTG server converted into a C2 proxy [T1584.004->T1090.001]."),
    ("de_reg",      "c2_internal", "stated",  "netsh PortProxy registry mod [T1112] created the internal proxy [T1090.001]."),
    ("c2_multihop", "c2_proxy",    "inferred","Multi-hop proxy realises the FRP proxy channel [T1090]."),
    ("c2_internal", "c2_proxy",    "inferred","Internal proxy realises the FRP proxy channel [T1090]."),
    ("ex_ps",       "c2_proxy",    "stated",  "'FRP clients, when executed via PowerShell [T1059.001], open reverse proxies.'"),
    ("c2_proxy",    "c2_enc",      "stated",  "Reverse proxies 'establish covert communications channels [T1573]' for C2."),
    ("de_pack",     "ex_ps",       "inferred","UPX-packed FRP clients [T1027.002] are the executables PowerShell runs."),
    ("ex_ps",       "ex_unix",     "inferred","Brightmetricagent CLI can leverage PowerShell/WMI/zsh [T1059.004]."),

    # Objective (end-state condition).
    ("lm_hijack",   "cond_objective","stated","OT-adjacent access positions the actor for potential OT disruption; no destructive action executed."),
]

# ---------------------------------------------------------------------------
# Build the STIX bundle.
# ---------------------------------------------------------------------------
def det_uuid(key: str) -> str:
    """Deterministic, UUIDv4-shaped id from a stable key.

    uuid5 gives reproducibility; we then stamp the version/variant nibbles to v4
    so the strict ``stix2`` loader (used by the Attack Flow CLI renderers)
    accepts every id while re-runs stay byte-identical.
    """
    b = bytearray(uuid.uuid5(NS, key).bytes)
    b[6] = (b[6] & 0x0F) | 0x40  # version 4
    b[8] = (b[8] & 0x3F) | 0x80  # RFC 4122 variant
    return str(uuid.UUID(bytes=bytes(b)))


def sid(kind, key):
    return f"{kind}--{det_uuid(kind + ':' + key)}"

TS = "2024-02-08T00:00:00.000Z"
ext_block = {AF_EXT: {"extension_type": "new-sdo"}}

# Resolve local keys -> stix ids.
stix_id = {}
for k in A:
    stix_id[k] = sid("attack-action", k)
for k in C:
    stix_id[k] = sid("attack-condition", k)
for k in OPS:
    stix_id[k] = sid("attack-operator", k)

# effect_refs / on_true_refs per source.
effect_refs = {k: [] for k in list(A) + list(OPS)}
on_true_refs = {k: [] for k in C}
for src, dst, kind, basis in E:
    tgt = stix_id[dst]
    if src in C:
        on_true_refs[src].append(tgt)
    else:
        effect_refs[src].append(tgt)

# start_refs: nodes with no incoming edge.
has_incoming = {dst for _, dst, _, _ in E}
start_keys = [k for k in list(A) + list(C) if k not in has_incoming]

objects = []

# Attack Flow SDO.
flow_id = "attack-flow--" + det_uuid("attack-flow")
identity_id = "identity--" + det_uuid("author-identity")
objects.append({
    "type": "attack-flow",
    "id": flow_id,
    "spec_version": "2.1",
    "created": TS,
    "modified": TS,
    "extensions": ext_block,
    "created_by_ref": identity_id,
    "start_refs": [stix_id[k] for k in start_keys],
    "name": "Volt Typhoon Critical Infrastructure Intrusion (AA24-038A)",
    "description": (
        "Hand-curated Attack Flow of PRC state-sponsored actor Volt Typhoon, "
        "reconstructed solely from joint advisory AA24-038A (CISA/NSA/FBI et al., "
        "8 Feb 2024). Campaign-typical behaviour: edge-appliance exploitation, "
        "VPN/valid-account persistence, NTDS.dit domain compromise via "
        "vssadmin+ntdsutil, LOTL discovery, and pre-positioning toward OT assets "
        "without executing destructive action."
    ),
    "scope": "campaign",
    "external_references": [
        {
            "source_name": "CISA AA24-038A",
            "description": ("PRC State-Sponsored Actors Compromise and Maintain Persistent "
                            "Access to U.S. Critical Infrastructure. CISA, NSA, FBI, with DOE, "
                            "EPA, TSA, ASD's ACSC, CCCS, NCSC-UK, NCSC-NZ. 8 Feb 2024."),
            "url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a",
        },
        {
            "source_name": "ASD's ACSC (republication)",
            "description": "Text source used for this reconstruction (cisa.gov blocks automated retrieval).",
            "url": ("https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/"
                    "prc-state-sponsored-actors-compromise-and-maintain-persistent-access-us-critical-infrastructure"),
        },
    ],
})

# Author identity.
objects.append({
    "type": "identity", "id": identity_id, "spec_version": "2.1",
    "created": TS, "modified": TS,
    "name": "MTDSim (hand-curated from AA24-038A)", "identity_class": "organization",
})

# Actions.
for k, a in A.items():
    obj = {
        "type": "attack-action",
        "id": stix_id[k],
        "spec_version": "2.1",
        "created": TS, "modified": TS,
        "extensions": ext_block,
        "name": a["name"],
        "tactic_id": a["tactic"],
        "tactic_ref": TACTIC_REF[a["tactic"]],
        "technique_id": a["tid"],
        "description": a["desc"],
    }
    if effect_refs[k]:
        obj["effect_refs"] = effect_refs[k]
    objects.append(obj)

# Operators.
for k, op in OPS.items():
    obj = {
        "type": "attack-operator", "id": stix_id[k], "spec_version": "2.1",
        "created": TS, "modified": TS, "extensions": ext_block, "operator": op,
    }
    if effect_refs[k]:
        obj["effect_refs"] = effect_refs[k]
    objects.append(obj)

# Conditions.
for k, desc in C.items():
    obj = {
        "type": "attack-condition", "id": stix_id[k], "spec_version": "2.1",
        "created": TS, "modified": TS, "extensions": ext_block, "description": desc,
    }
    if on_true_refs[k]:
        obj["on_true_refs"] = on_true_refs[k]
    objects.append(obj)

# Attack Flow extension-definition SDO (self-contained bundle).
objects.append({
    "type": "extension-definition",
    "id": AF_EXT,
    "spec_version": "2.1",
    "created": "2022-08-02T19:34:35.143Z",
    "modified": "2022-08-02T19:34:35.143Z",
    "name": "Attack Flow",
    "description": "Extends STIX 2.1 with features to create Attack Flows.",
    "created_by_ref": "identity--fb9c968a-745b-4ade-9b25-c324172197f4",
    "schema": "https://center-for-threat-informed-defense.github.io/attack-flow/stix/attack-flow-schema-2.0.0.json",
    "version": "2.0.0",
    "extension_types": ["new-sdo"],
})

bundle = {
    "type": "bundle",
    "id": "bundle--" + det_uuid("bundle"),
    "spec_version": "2.1",
    "created": TS,
    "modified": TS,
    "objects": objects,
}

json_path = HERE / "volt_typhoon_aa24038a.json"
json_path.write_text(json.dumps(bundle, indent=2) + "\n")

# ---- round-trip through the repo's own parser -> per-flow YAML -------------
import sys
sys.path.insert(0, str(HERE.parents[2] / "src"))
from mtdsim.l1_construction.attack_flow_parser import parse_flow_file  # noqa: E402
from mtdsim.l1_construction.schema import TACTIC_ID_TO_NAME  # noqa: E402

extract = parse_flow_file(
    json_path, flow_id="volt_typhoon_aa24038a", source="hand_curated",
    tactic_id_to_name=TACTIC_ID_TO_NAME,
)
yaml_path = HERE / "volt_typhoon_aa24038a.yaml"
yaml_path.write_text(extract.to_yaml())

# ---- self-validation report ------------------------------------------------
n_act = len(A); n_cond = len(C); n_op = len(OPS); n_edge = len(E)
stated = sum(1 for *_, k, _ in E if k == "stated")
inferred = n_edge - stated
print(f"actions={n_act} conditions={n_cond} operators={n_op} edges={n_edge} "
      f"(stated={stated} inferred={inferred})")
print(f"start_refs ({len(start_keys)}): {', '.join(start_keys)}")
# Parser round-trip counts.
pa = sum(1 for n in extract.nodes if n.kind == 'action')
pc = sum(1 for n in extract.nodes if n.kind == 'condition')
po = sum(1 for n in extract.nodes if n.kind == 'operator')
print(f"parsed nodes: action={pa} condition={pc} operator={po} edges={len(extract.edges)}")
assert pa == n_act and pc == n_cond and po == n_op, "round-trip node-count mismatch"
assert len(extract.edges) == n_edge, "round-trip edge-count mismatch"
# Every action technique parses and parent-collapses.
unmapped = [n.id for n in extract.nodes if n.kind == 'action' and not n.technique_id]
assert not unmapped, f"unmapped actions: {unmapped}"
print("OK: round-trip node/edge counts match; every action carries a parent technique_id")
print(f"wrote {json_path.name} and {yaml_path.name}")
