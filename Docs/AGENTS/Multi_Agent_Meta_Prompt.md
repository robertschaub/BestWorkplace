# BestWorkplace Multi-Agent Meta-Prompt Template

**Version:** 1.0
**Date:** 2026-02-15

---

## How to Use

Two options depending on task complexity:

### Quick-Start (for simple/moderate tasks)

Most tasks only need a one-liner. The "As \<Role\>" pattern triggers the Role Activation Protocol in AGENTS.md:

```
As {ROLE}, {one-sentence task}.
Area: {area from Multi_Agent_Collaboration_Rules.md §1.2}
Complexity: {simple|moderate|complex}
```

**Examples:**
```
As Tech Writer, update the Team Topologies page with new content about platform teams.
Area: Content
Complexity: simple
```

```
As Tech Writer, reorganize the Knowledge section to add a new sub-category for "Scaling Agile".
Area: Documentation, Structure
Complexity: moderate
```

```
As DevOps Expert, fix the GitHub Actions workflow that fails when attachment filenames contain spaces.
Area: Deployment
Complexity: moderate
```

### Captain's Assignment Checklist

What to provide based on task complexity:

| Complexity | What to Include |
|------------|----------------|
| **Simple** | Role + instruction (the "As \<Role\> ..." pattern above) |
| **Moderate** | + Area + relevant context/files |
| **Complex** | + Constraints + acceptance criteria + related WIP docs + which roles reviewed previously |

### Full Template (for complex/multi-agent tasks)

Copy the template below and fill in the `{PLACEHOLDERS}`. Use this for complex tasks or when multiple agents will collaborate on the same work.

---

# META-PROMPT TEMPLATE

```markdown
# BestWorkplace Task Assignment

## Your Role
**Role:** {ROLE}
<!-- Options: Technical Writer | Content Strategist | DevOps Expert | Viewer Developer -->

---

## Task Information

**Task Title:** {TASK_TITLE}
<!-- Brief descriptive title -->

**Area:** {AREA}
<!-- Options: Documentation | Content | Deployment | Structure -->
<!-- Or leave blank for agent to identify relevant documents -->

**Complexity:** {COMPLEXITY}
<!-- Options: Low | Medium | High | Investigation -->

---

## Goals

{GOALS}
<!--
Describe what needs to be accomplished. Be specific.
Example:
- Reorganize the Knowledge section into clearer sub-categories
- Add a new page on "Psychological Safety in Teams"
- Ensure all cross-references between pages are valid
-->

---

## Constraints & Context

{CONSTRAINTS}
<!--
Any specific constraints or context.
Example:
- Must preserve existing page URLs for gh-pages links
- Content must align with the 6 core principles on the root page
- All content under CC BY-SA 4.0 license
-->

---

## Deliverables

{DELIVERABLES}
<!--
What outputs are expected.
Example:
- Updated xWiki pages in Docs/xwiki-pages/The Best Workplace/
- Successful gh-pages build verification
- Summary of changes made
-->

---

## Workflow Phase

**Current Phase:** {PHASE}
<!-- Options: Planning | Review | Implementation | Deployment | Finalization -->

**Previous Documents:**
{PREVIOUS_DOCS}
<!--
List any existing documents this task builds on.
Example:
- Docs/WIP/Knowledge_Reorganization_Plan.md (Draft by Content Strategist)
-->

---

## MANDATORY

Read and follow `/Docs/AGENTS/Multi_Agent_Collaboration_Rules.md`

---

{ADDITIONAL_INSTRUCTIONS}
<!--
Any final task-specific instructions.
Example:
- Start by reading the existing Knowledge section pages
- Preview changes locally with View.cmd before committing
- Coordinate with the Content Strategist for content direction
-->

---

Now proceed with your task as {ROLE}.
```

---

# QUICK-START EXAMPLES

## Example 1: Technical Writer - Content Update

```markdown
# BestWorkplace Task Assignment

## Your Role
**Role:** Technical Writer

---

## Task Information
**Task Title:** Add Psychological Safety Page
**Area:** Content
**Complexity:** Medium

---

## Goals
- Create a new xWiki page "Psychological Safety" under Knowledge
- Include key concepts from Amy Edmondson's research
- Add a Mermaid diagram showing the impact model
- Cross-reference from the Leadership to foster Innovation page

---

## Constraints & Context
- Must follow xWiki 2.1 syntax
- Content under CC BY-SA 4.0 license
- Align with the "We Practice Transparency and Build Trust" principle

---

## Deliverables
- New page: `Docs/xwiki-pages/The Best Workplace/Knowledge/Psychological Safety/WebHome.xwiki`
- Updated cross-references in related pages
- Successful local preview verification

---

## Workflow Phase
**Current Phase:** Implementation
**Previous Documents:** None (new content)

---

## MANDATORY

Read and follow `/Docs/AGENTS/Multi_Agent_Collaboration_Rules.md`

---

Preview changes with `Docs\xwiki-pages\View.cmd` before committing.

---

Now proceed with your task as Technical Writer.
```

---

## Example 2: Content Strategist - Content Review

```markdown
# BestWorkplace Task Assignment

## Your Role
**Role:** Content Strategist

---

## Task Information
**Task Title:** Knowledge Section Content Strategy Review
**Area:** Content
**Complexity:** Medium

---

## Goals
- Review all pages under Knowledge/ for completeness and relevance
- Identify gaps in coverage vs. the 6 core principles
- Propose new topics or reorganization
- Prioritize improvements

---

## Constraints & Context
- Target audience: agile practitioners, leaders, coaches
- Content should be actionable, not just theoretical
- Consider what would make the gh-pages site most valuable

---

## Deliverables
- Content audit document in Docs/WIP/
- Prioritized list of improvements
- Recommendations for new topics

---

## Workflow Phase
**Current Phase:** Planning
**Previous Documents:** None

---

## MANDATORY

Read and follow `/Docs/AGENTS/Multi_Agent_Collaboration_Rules.md`

---

Start by reading the root WebHome.xwiki to understand the vision, then review each Knowledge page.

---

Now proceed with your task as Content Strategist.
```

---

## Example 3: DevOps Expert - Deployment Fix

```markdown
# BestWorkplace Task Assignment

## Your Role
**Role:** DevOps Expert

---

## Task Information
**Task Title:** Fix gh-pages Build for Special Characters
**Area:** Deployment
**Complexity:** Medium

---

## Goals
- Investigate why pages with special characters in directory names fail during gh-pages build
- Fix the build_ghpages.py script to handle edge cases
- Ensure the GitHub Actions workflow handles the fix correctly

---

## Constraints & Context
- Must not break existing pages
- Build must work on both Windows (local) and Ubuntu (GitHub Actions)
- Preview must still work via View.cmd

---

## Deliverables
- Fixed build_ghpages.py
- Verified successful build with all pages
- Updated deploy-docs.yml if needed

---

## Workflow Phase
**Current Phase:** Implementation
**Previous Documents:** None

---

## MANDATORY

Read and follow `/Docs/AGENTS/Multi_Agent_Collaboration_Rules.md`

---

Test locally before pushing: `python Docs/xwiki-pages/scripts/build_ghpages.py`

---

Now proceed with your task as DevOps Expert.
```

---

# DOCUMENT TYPE REFERENCE

| Document Type | Purpose | Typical Author |
|---------------|---------|----------------|
| `_Plan.md` | Implementation plan with steps | Content Strategist |
| `_Review.md` | Review comments and feedback | Any reviewer |
| `_Analysis.md` | Investigation findings | Any analyst |
| `_Content_Audit.md` | Content review and recommendations | Content Strategist |
| `_Doc_Review.md` | Documentation review | Technical Writer |

---

## Related Documents

- [Multi-Agent Collaboration Rules](./Multi_Agent_Collaboration_Rules.md) - Full rules and role definitions
- [GlobalMasterKnowledge for xWiki](./GlobalMasterKnowledge_for_xWiki.md) - XWiki-specific protocols

---

**Document Maintainer:** Technical Writer
**Last Reviewed:** 2026-02-15
