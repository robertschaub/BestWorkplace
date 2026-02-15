# Unresolvable Broken Links

**Date:** 2026-02-15
**Status:** Resolved

## Context

A full link check was performed across all 21 xWiki pages. Of 187 external URLs checked, 14 broken links were fixed with working replacements (committed in `09620e5`). The 8 links below are genuinely broken with no direct replacement found.

## Unresolvable Links


| Page                      | Link Text                                                               | Original URL                                                                                                                                                                                 | Issue                               | Replacement                                                                                                         |
| --------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Business agility          | Creating and sustaining a Culture of Agile (kpmg.us)                    | [advisory.kpmg.us/.../culture-of-agile.pdf](https://advisory.kpmg.us/content/dam/advisory/en/pdfs/2020/culture-of-agile.pdf)                                                                 | PDF removed, no replacement         | https://assets.kpmg.com/content/dam/kpmg/my/pdf/driving-workforce-agility-whitepaper.pdf                            |
| Business agility          | A Journey of Change in the Aircraft Industry (saabaircraftindustry.com) | [saabaircraftindustry.com/.../agile-methods-in-software-development/](https://saabaircraftindustry.com/en/roads-to-new-capability/development-skills/agile-methods-in-software-development/) | Domain DNS failure                  | delete                                                                                                              |
| Agile Hardware Dev        | A Journey of Change in the Aircraft Industry (saabaircraftindustry.com) | [saabaircraftindustry.com/.../agile-methods-in-software-development/](https://saabaircraftindustry.com/en/roads-to-new-capability/development-skills/agile-methods-in-software-development/) | Same — domain DNS failure          | delete                                                                                                              |
| Leadership                | 5 Essential Leadership Functions - Anthology Coaching                   | [anthologycoaching.com/essential-leadership-functions/](https://anthologycoaching.com/essential-leadership-functions/)                                                                       | Domain gone                         | https://www.franklincovey.com/blog/leadership-qualities/                                                            |
| Leadership                | Nimble (nimbleleading.com)                                              | [nimbleleading.com](https://www.nimbleleading.com/)                                                                                                                                          | Domain gone                         | delete                                                                                                              |
| Coaching                  | How Agile Coaching can enable New Ways of Working (wavestone.com)       | [wavestone.com/.../how-agile-coaching-can-enable-new-ways-of-working/](https://www.wavestone.com/en/insight/how-agile-coaching-can-enable-new-ways-of-working/)                              | 404 — page removed                 | https://www.wavestone.com/en/insight/agile-leadership-mastering-change-and-making-organizations-fit-for-the-future/ |
| Cross-Functional Teamwork | Here's the Thing About "T-shaped" People (adventureswithagile.com)      | [adventureswithagile.com/.../heres-thing-t-shaped-people/](https://www.adventureswithagile.com/2017/07/12/heres-thing-t-shaped-people/)                                                      | SSL certificate mismatch (x2 links) | delete                                                                                                              |
| User Centered Design      | Think like a designer (orponchy.com)                                    | [blog.orponchy.com/.../think-like-a-designer...](https://blog.orponchy.com/think-like-a-designer-user-centered-design-5-elements-of-ux-design-design-thinking-process/)                      | Domain gone                         | delete                                                                                                              |

## Options

- **Remove** the broken links entirely
- **Replace** with alternative articles on the same topic
- **Leave as-is** (links will show errors when clicked)
