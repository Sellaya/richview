Original image masters (optional)
===================================

Use this folder for unmodified or highest-quality exports before web optimization
(e.g. camera JPEG, TIFF, or large PNG from design). The live site uses files in
the parent images/ folder (and images/blog/).

Naming convention
-------------------
- Lowercase, hyphen-separated slugs: team-member-name-original.jpg
- Include role or context if needed: about-hero-office-original.png
- Avoid spaces and special characters in filenames.

Workflow
--------
1. Drop originals here.
2. Export optimized copies to images/ (or images/blog/) for production.
3. git add images/originals/ && git commit && git push

Very large files
----------------
If originals exceed ~50–100 MB total, consider Git LFS for this path on GitHub.
