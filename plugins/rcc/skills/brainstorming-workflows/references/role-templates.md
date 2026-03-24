# Role Templates for Workflow Brainstorming

## How to Use

Present the role table to the user. After they choose, use the corresponding deep-dive questions. Skip questions already answered by the analysis report.

---

## Software Developer

**Typical workflows:** coding, testing, code review, CI/CD, deployment, debugging

**Deep-dive questions (one at a time):**
1. What languages and frameworks do you use daily?
2. What's your testing approach? (unit, integration, e2e, manual)
3. Do you use CI/CD? What pipeline steps matter most?
4. What code quality tools do you use? (linter, formatter, type checker)
5. What's your branching and PR workflow?
6. Are there project-specific conventions your team enforces?
7. What repetitive tasks do you wish were automated?

**Likely components:**
- CLAUDE.md: code style, build commands, project structure
- Rules: language conventions, API patterns, test patterns
- Hooks: linting, formatting, type checking
- Skills: deployment, release, migration workflows

---

## Project Manager

**Typical workflows:** task tracking, reporting, scheduling, stakeholder communication

**Deep-dive questions (one at a time):**
1. What project management tools do you use? (Linear, Jira, etc.)
2. What reports do you produce regularly? (status, metrics, etc.)
3. What communication channels does your team use?
4. Do you have recurring meetings that need preparation?
5. What's your biggest time sink in project coordination?

**Likely components:**
- CLAUDE.md: project context, team structure, key dates
- Rules: document formatting, report templates
- Skills: status report generation, task sync, meeting prep

---

## Content Creator

**Typical workflows:** writing, editing, translation, publishing, social media

**Deep-dive questions (one at a time):**
1. What types of content do you produce? (docs, blog, marketing, etc.)
2. Do you work in multiple languages?
3. What's your review/approval process?
4. Do you have brand guidelines or style guides?
5. What publishing platforms do you use?

**Likely components:**
- CLAUDE.md: brand voice, style guidelines
- Rules: writing conventions, formatting standards
- Skills: translation, publishing, content review workflows

---

## Data Analyst

**Typical workflows:** data processing, visualization, reporting, automation

**Deep-dive questions (one at a time):**
1. What data tools do you use? (Python/R, SQL, BI tools)
2. What types of analysis do you do most often?
3. Do you produce recurring reports?
4. What data quality checks matter to you?
5. Are there compliance or privacy requirements?

**Likely components:**
- CLAUDE.md: data sources, key metrics, compliance rules
- Rules: SQL conventions, notebook patterns
- Hooks: data validation checks
- Skills: report generation, data pipeline workflows

---

## Operations / DevOps

**Typical workflows:** monitoring, deployment, incident response, infrastructure

**Deep-dive questions (one at a time):**
1. What infrastructure do you manage? (cloud provider, services)
2. What monitoring/alerting tools do you use?
3. What's your deployment process?
4. How do you handle incidents?
5. What IaC tools do you use? (Terraform, Pulumi, etc.)

**Likely components:**
- CLAUDE.md: infrastructure overview, critical services
- Rules: IaC conventions, security policies
- Hooks: security checks, deployment validation
- Skills: incident response, deployment, monitoring workflows

---

## Custom Role

**Approach:**
1. Ask: "Please describe your role in 2-3 sentences"
2. Ask: "What are the 3 tasks you do most often?"
3. Ask: "What tools or platforms do you use daily?"
4. Ask: "What repetitive tasks frustrate you most?"
5. Ask: "Are there rules or standards you must follow?"

**Map answers to components** using the same pattern as above.
