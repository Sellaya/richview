#!/usr/bin/env python3
"""Apply full-screen mobile menu (from index.html) to all pages."""

import re
import os

FULLSCREEN_BLOCK = r'''            /* --- Mobile menu: full-screen overlay (matches homepage) --- */
            .nav-links {
                display: none !important;
                position: absolute;
                left: 0; right: 0; top: 0; bottom: 0;
                list-style: none !important;
            }
            nav.menu-open {
                position: fixed !important;
                top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
                width: 100% !important; height: 100% !important;
                min-height: 100vh; min-height: 100dvh;
                max-height: 100vh; max-height: 100dvh;
                z-index: 9999 !important;
                transform: none !important;
                margin: 0 !important;
                background: #ffffff !important;
                border-radius: 0 !important;
                box-shadow: none !important;
                border: none !important;
                display: flex !important;
                flex-direction: column !important;
                overflow: hidden;
            }
            nav.menu-open .nav-inner {
                flex: 1;
                min-height: 0;
                display: grid !important;
                grid-template-rows: minmax(60px, auto) 1fr;
                grid-template-columns: 1fr auto;
                grid-template-areas: "menu-header menu-header" "menu-links menu-links";
                gap: 0;
                padding: 0;
                background: #ffffff;
                width: 100%;
            }
            nav.menu-open .logo {
                grid-area: menu-header;
                grid-column: 1;
                align-self: center;
                justify-self: start;
                margin: 0; padding: 0;
                padding-top: max(0.75rem, env(safe-area-inset-top));
                padding-bottom: 0.75rem;
                padding-left: max(1rem, env(safe-area-inset-left));
            }
            nav.menu-open .mobile-menu-btn {
                grid-area: menu-header;
                grid-column: 2;
                align-self: center;
                justify-self: end;
                margin: 0; padding: 0;
                padding-top: max(0.75rem, env(safe-area-inset-top));
                padding-bottom: 0.75rem;
                padding-right: max(1rem, env(safe-area-inset-right));
                padding-left: 1rem;
                min-width: 48px !important;
                min-height: 48px !important;
            }
            nav.menu-open .cta-nav { display: none !important; }
            nav.menu-open .nav-links {
                display: flex !important;
                grid-area: menu-links;
                grid-column: 1 / -1;
                flex-direction: column;
                align-items: stretch;
                align-self: stretch;
                justify-self: stretch;
                position: relative;
                width: 100%;
                height: 100%;
                min-height: 0;
                margin: 0;
                padding: 1rem max(1rem, env(safe-area-inset-right)) max(1.5rem, calc(1rem + env(safe-area-inset-bottom))) max(1rem, env(safe-area-inset-left)) !important;
                gap: 0;
                background: #ffffff;
                border-top: 1px solid rgba(11, 22, 53, 0.08);
                border-radius: 0;
                box-shadow: none;
                overflow-y: auto;
                -webkit-overflow-scrolling: touch;
                overscroll-behavior: contain;
                touch-action: manipulation;
                opacity: 0;
                visibility: hidden;
                transform: translateY(6px);
                transition: opacity 0.25s ease, visibility 0.25s, transform 0.25s ease;
                pointer-events: none;
            }
            nav.menu-open .nav-links.active {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
                pointer-events: auto;
            }
'''

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already full-screen
    if 'grid-template-areas: "menu-header menu-header"' in content:
        return False, "already full-screen"
    
    # Must have bottom sheet to replace
    if 'bottom: 0' not in content or 'nav.menu-open::before' not in content:
        return False, "no bottom sheet found"
    
    # Match block from nav-inner (with nav and logo) through ::before, @keyframes, ::after, .nav-links, .nav-links.active
    # Use a single flexible pattern - match from "nav.menu-open .nav-inner" in 1024px block
    # until ".nav-mobile-logo" - we match the bottom sheet section
    
    pattern = re.compile(
        r'\s*nav\.menu-open \.nav-inner \{ z-index: 1001[^}]*\}\s*'
        r'\s*nav \{ left: 4%[^}]*\}\s*'
        r'\s*nav\.menu-open \.logo, nav\.menu-open \.mobile-menu-btn \{ z-index: 1002[^}]*\}\s*'
        r'(\s*/\*[^*]*\*/\s*)?'
        r'\s*nav\.menu-open::before \{[^}]+\}\s*'
        r'\s*@keyframes navBackdropIn \{[^}]+\}\s*'
        r'\s*nav\.menu-open::after \{[^}]+\}\s*'
        r'\s*\.nav-links \{\s*[\s\S]*?bottom: 0[\s\S]*?\}\s*'
        r'\s*\.nav-links\.active \{\s*[\s\S]*?\}\s*'
        r'(\s*\.nav-links::before \{[^}]*\}\s*)?',
        re.DOTALL
    )
    
    def replacer(m):
        return '\n            nav { left: 4% !important; right: 4% !important; width: auto !important; transform: none !important; }\n' + FULLSCREEN_BLOCK
    
    new_content, count = pattern.subn(replacer, content, count=1)
    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "UPDATED"
    
    # Fallback: try without nav { } in the middle (some files have different order)
    pattern2 = re.compile(
        r'(\s*nav\.menu-open \.nav-inner \{[^}]*\})\s*'
        r'(\s*nav \{[^}]*\})\s*'
        r'(\s*nav\.menu-open \.logo, nav\.menu-open \.mobile-menu-btn \{[^}]*\})\s*'
        r'(\s*/\*[^*]*\*/\s*)?'
        r'\s*nav\.menu-open::before \{[^}]*\}\s*'
        r'\s*@keyframes navBackdropIn[^}]*\}\s*'
        r'\s*nav\.menu-open::after \{[^}]*\}\s*'
        r'\s*\.nav-links \{\s*'
        r'position: fixed[^}]*?bottom: 0[^}]*\}\s*'
        r'\.nav-links\.active \{[^}]*\}\s*'
        r'(\s*\.nav-links::before \{[^}]*\}\s*)?',
        re.DOTALL
    )
    new_content, count = pattern2.subn(replacer, content, count=1)
    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "UPDATED (pattern2)"
    
    return False, "pattern not found"

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pages = [
        'terms/index.html', 'privacy/index.html', 'disclaimer/index.html', 'thank-you/index.html',
        'about/index.html', 'faq/index.html', 'blog/index.html',
        'borrowers/index.html', 'what-is-a-mic/index.html',
        'brokers/index.html', 'investors/index.html',
    ]
    for name in pages:
        path = os.path.join(root, name)
        if os.path.exists(path):
            ok, msg = fix_file(path)
            print(f"{name}: {msg}")

if __name__ == '__main__':
    main()
