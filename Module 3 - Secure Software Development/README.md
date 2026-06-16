# Module 3: Secure Software Development (MSc Computer Science)

## 📌 Module Overview
This repository contains my complete academic registry, laboratory artifacts, and collaborative engineering projects completed during **Module 3: Secure Software Development** at the University of Essex Online. 

The core focus of this module is evaluating software architectures through a security lens—bridging high-level security governance (such as threat modelling and risk management standards) with low-level secure code execution constraints (such as memory safety, safe regex construction, and automated static application security testing).

---

## 🏆 Core Milestone Highlight
* **Unit 6 Collaborative Poster Assignment:** Design Weaknesses & Mitigation Roadmap.
* **Grade Awarded:** **Distinction** 🏆
* **Key Learning Objective:** Successfully identified architectural system vulnerabilities and synthesized an enterprise-grade threat-mitigation strategy within a cross-functional development team.

---

## 🗂️ Repository Architecture & Index

This module is organized into structured, modular units. Each folder contains functional source code files paired with a technical write-up or an academic reflective commentary framed using **John Driscoll's ("What? So What? Now What?") Reflective Model**:

```text
Module 3 - Secure Software Development/
├── README.md                                            <- This root module index page
├── Unit 2 - UML Modelling to Support Secure System Planning/
│   ├── README.md                                        <- Threat analysis framework
│   └── secure_system_models.png                         <- OWASP A02:2021 Misuse Case Diagram
├── Unit 3 - Cryptography and Secure Execution/
│   ├── README.md                                        <- Memory Corruption Lab (C vs. Python)
│   ├── seminar_discussion.md                            <- Language Security Review (Cifuentes & Bierman)
│   ├── bufoverflow.c                                    <- Legacy C buffer vulnerability code
│   └── overflow.py                                      <- Out-of-bounds Python script
├── Unit 4 - Exploring Programming Language Concepts/
│   ├── README.md                                        <- Recursion & Stack limits analysis
│   ├── regex_analysis.md                                <- ReDoS & Catastrophic Backtracking brief
│   ├── hanoi.py                                         <- Recursive Towers of Hanoi tracking script
│   └── regex_lab.py                                     <- Anchor-secured UK Postcode validator
├── Unit 5 - Validating Product Security/
│   └── README.md                                        <- Input sanitisation & defensive linting matrices
└── Unit 7 - Introduction to Operating Systems/
    ├── README.md                                        <- CLI custom shell assessment & index
    ├── reflective_models_analysis.md                   <- Comparative critique of reflective frameworks
    └── custom_shell.py                                  <- Hardened interactive Python shell sandbox