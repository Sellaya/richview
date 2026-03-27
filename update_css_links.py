#!/usr/bin/env python3
import os
import re

# List of HTML files to update
html_files = [
    'home.html',
    'terms.html',
    'privacy.html',
    'thank-you.html',
    'disclaimer.html',
    'richview-faq.html',
    'richview-blog.html',
    'richview-about.html',
    'richview-borrowers.html',
    'richview-capital-mic.html',
    'richview-what-is-a-mic.html',
    'richview-capital-brokers.html'
]

# Old CSS links pattern
old_pattern = r'<link rel="stylesheet" href="css/design-tokens\.css">.*?<link rel="stylesheet" href="css/calendly-style-picker\.css">'

# New CSS links
new_links = '''<link rel="stylesheet" href="css/design-tokens.css">
    <link rel="stylesheet" href="css/typography-system.css">
    <link rel="stylesheet" href="css/responsive-spacing.css">
    <link rel="stylesheet" href="css/focus-states.css">
    <link rel="stylesheet" href="css/animations-professional.css">
    <link rel="stylesheet" href="css/button-contrast.css">
    <link rel="stylesheet" href="css/mobile-menu-improved.css">
    <link rel="stylesheet" href="css/nav-hover-orange.css">
    <link rel="stylesheet" href="css/hero-ctas-buttons.css">
    <link rel="stylesheet" href="css/faq-section.css">
    <link rel="stylesheet" href="css/motion-home.css">
    <link rel="stylesheet" href="css/lottie-forms.css">
    <link rel="stylesheet" href="css/testimonials-google.css">
    <link rel="stylesheet" href="css/calendly-style-picker.css">'''

for html_file in html_files:
    file_path = f'/tmp/cc-agent/65091092/project/{html_file}'

    if not os.path.exists(file_path):
        print(f'Skipping {html_file} - file not found')
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace old CSS links with new ones
        updated_content = re.sub(old_pattern, new_links, content, flags=re.DOTALL)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f'Updated {html_file}')
    except Exception as e:
        print(f'Error updating {html_file}: {e}')

print('CSS links update complete!')
