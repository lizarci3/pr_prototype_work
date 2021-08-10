# Contributing Guidelines

Before contributing to the `pytemplate` repository, discuss the changes you intend
to make with a colleague. The goal is to minimize the likelihood of a scenario
where you spend a lot of your time and effort on a solution that may not be the
best fit.

## Branch naming

Branch names in our repository follow the pattern
`<creator name>/<JIRA ticket>/<clear-description-in-kebab-case>`.

If a JIRA ticket is not available, you may avoid the middle section.

## Submitting a pull request

One important goal when submitting PRs is to keep them *bite-sized*. Small PRs
increase the quality of software by leading to better (and faster) reviews. This
means that each JIRA ticket can spawn multiple PRs. There does not need to be a
1-1 relationship between JIRA tickets and PRs, but you can create subtasks if
you find that helpful.

A good PR has most of the following characteristics:

- It does one and only one thing.
- The description explains the intent of the PR as well as any background
  information required to understand the role of that PR in the context of the
  project.
- It contains some form of automated testing, if appropriate.
- It contains some proof that the PR does what it claims. See explanation below.

In addition to this,

- Add a good descriptive title to your PR: our recommended format is
`[<JIRA ticket>]: <short description of actual PR not just ticket>`.
- Assign yourself as "assignee".
- Use labels whenever they are relevant for describing the PR.
- Invite at least two reviewers to check your code.

When opening a PR, the description is autopopulated with an outline of what
needs to be described. Please make an effort to fill this out with a good amount
of detail; do not just ignore it. PRs will be rejected if no attempt has been
made to follow our guidelines.

### Draft Pull Requests

For work in progress, open a draft pull request. This would signal that your pull
request is not done, but you may want some early feedback and collaboration.

### Proving that the PR does what it claims

For most PRs, it is possible to establish proof that the PR does what it claims.
You'll have to figure how to do this on a case-by-case basis, but here are some
examples to help you along:

- If a PR adds new logic, additional tests that cover that logic and pass is
  proof enough.
- If a PR claims to improve the performance of a module, add some benchmark
  results in the description.
- In some cases, the proof is self-evident and you don't need to do anything.
  For example, if a PR updates the versions of some packages by updating the
  `setup.py` file, the proof is self-evident.
