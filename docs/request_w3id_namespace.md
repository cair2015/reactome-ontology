# W3ID namespace request notes for `reactome-ontology`

## Goal

Create a persistent namespace for the project:

- Base namespace: `https://w3id.org/reactome-ontology`
- Term URI example: `https://w3id.org/reactome-ontology/Disease`

Main project links:

- GitHub: `https://github.com/cair2015/reactome-ontology`
- Docs: `https://cair2015.github.io/reactome-ontology/`

## Basic process

1. Fork `perma-id/w3id.org`
2. Create a new directory:

```text
reactome-ontology/
```

3. Add these files:

```text
reactome-ontology/README.md
reactome-ontology/.htaccess
```

4. Commit the changes
5. Open a pull request to `perma-id/w3id.org`
6. After merge, test the namespace URL

## Minimal README content

```md
# reactome-ontology

Permanent identifiers for the Reactome Ontology project.

## Maintainer
- Robin Cai
- GitHub: @cair2015

## Namespace
- https://w3id.org/reactome-ontology
```

## Final `.htaccess`

```apache
Options +FollowSymLinks
RewriteEngine on

# Base namespace
RewriteRule ^$ https://cair2015.github.io/reactome-ontology/ [R=302,L]

# Optional convenience redirects
RewriteRule ^index\.html$ https://cair2015.github.io/reactome-ontology/ [R=302,L]
RewriteRule ^README\.md$ https://github.com/cair2015/reactome-ontology [R=302,L]

# Term URIs
RewriteRule ^([^/]+)$ https://cair2015.github.io/reactome-ontology/elements/$1 [R=303,L]
```

## What this does

- `https://w3id.org/reactome-ontology`
  -> `https://cair2015.github.io/reactome-ontology/`

- `https://w3id.org/reactome-ontology/Disease`
  -> `https://cair2015.github.io/reactome-ontology/elements/Disease`

## Why `302` and `303`

- `302` for the base namespace homepage redirect
- `303` for ontology term URIs, because the term URI identifies the concept and redirects to a page describing it

## Important note on rule order

Put specific rules before the general term rule.

This avoids the catch-all term rule matching paths like `index.html` and `README.md` first.

## Suggested commit / PR text

Commit message:

```text
Add term URI redirects in .htaccess
```

PR title:

```text
Add term URI redirects for reactome-ontology
```

## Test after merge

Check:

- `https://w3id.org/reactome-ontology`
- `https://w3id.org/reactome-ontology/Disease`
- `https://w3id.org/reactome-ontology/Pathway`

If term URIs do not work yet, it may just need a little time after the PR is merged.
