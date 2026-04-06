# Role Templates for Workflow Brainstorming

## How to Use

Present the role table to the user. After they choose, use the corresponding deep-dive questions. Skip questions already answered by the analysis report.

**Questioning strategy:** Prefer walkthrough questions ("Walk me through the last time you...") over inventory questions ("What tools do you use?"). Walkthroughs reveal actual workflow pain points; inventories just list tools.

---

## Software Developer

**Typical workflows:** coding, testing, code review, CI/CD, deployment, debugging

**Deep-dive questions (one at a time):**
1. Walk me through the last feature you shipped — from starting to merging. Where did friction happen?
2. What's your testing approach? (unit, integration, e2e, manual) What breaks most often?
3. Walk me through a recent bug fix. How did you find the root cause?
4. What code quality tools do you use? Which ones actually catch real issues vs. noise?
5. What's your branching and PR workflow? Where do things get stuck?
6. Are there conventions your team enforces manually that could be automated?
7. What have you tried automating before? What worked, what didn't, and why?

**Likely components:**
- CLAUDE.md: code style, build commands, project structure
- Rules: language conventions, API patterns, test patterns
- Hooks: linting, formatting, type checking
- Skills: deployment, release, migration workflows

---

## Project Manager

**Typical workflows:** task tracking, reporting, scheduling, stakeholder communication

**Deep-dive questions (one at a time):**
1. Walk me through how you track a feature from request to delivery. Where do things get lost?
2. Walk me through your last status report. How long did it take, and where did the data come from?
3. What recurring meetings do you prepare for? Walk me through the prep for the most tedious one.
4. When something slips, how do you find out? Walk me through a recent example.
5. What have you tried automating in project coordination? What worked, what didn't?

**Likely components:**
- CLAUDE.md: project context, team structure, key dates
- Rules: document formatting, report templates
- Skills: status report generation, task sync, meeting prep

---

## Content Creator

**Typical workflows:** writing, editing, translation, publishing, social media

**Deep-dive questions (one at a time):**
1. Walk me through the last piece of content you published — from blank page to live. Where was the friction?
2. Do you work in multiple languages? Walk me through how you handle translation.
3. Walk me through your review/approval process. Where does it get stuck?
4. Do you have brand guidelines or style guides? How often do you catch yourself violating them?
5. What have you tried automating in your publishing workflow? What worked, what didn't?

**Likely components:**
- CLAUDE.md: brand voice, style guidelines
- Rules: writing conventions, formatting standards
- Skills: translation, publishing, content review workflows

---

## Data Analyst

**Typical workflows:** data processing, visualization, reporting, automation

**Deep-dive questions (one at a time):**
1. Walk me through your most recent analysis — from question to deliverable. Where did you spend the most time?
2. Walk me through a recurring report you produce. How much is manual vs. automated?
3. Walk me through the last time you found bad data. How did you catch it, and how did you fix it?
4. Are there compliance or privacy requirements? Walk me through how you ensure compliance today.
5. What have you tried automating in your data workflow? What worked, what didn't?

**Likely components:**
- CLAUDE.md: data sources, key metrics, compliance rules
- Rules: SQL conventions, notebook patterns
- Hooks: data validation checks
- Skills: report generation, data pipeline workflows

---

## Operations / DevOps

**Typical workflows:** monitoring, deployment, incident response, infrastructure

**Deep-dive questions (one at a time):**
1. Walk me through your last deployment — from code ready to running in production. Where was the risk?
2. Walk me through the last incident you responded to. How did you find the root cause?
3. Walk me through how you manage infrastructure changes. What guardrails do you have?
4. What monitoring/alerting do you rely on most? Walk me through a recent false alarm vs. real alert.
5. What have you tried automating in your ops workflow? What worked, what didn't?

**Likely components:**
- CLAUDE.md: infrastructure overview, critical services
- Rules: IaC conventions, security policies
- Hooks: security checks, deployment validation
- Skills: incident response, deployment, monitoring workflows

---

## Custom Role

**Approach:**
1. Ask: "Please describe your role in 2-3 sentences"
2. Ask: "Walk me through a typical day — what's the first task, and what follows?"
3. Ask: "What's the most frustrating repetitive task you do? Walk me through it step by step."
4. Ask: "What have you tried automating before? What worked, what didn't?"
5. Ask: "Are there rules or standards you must follow that are easy to accidentally violate?"

**Map answers to components** using the same pattern as above.
