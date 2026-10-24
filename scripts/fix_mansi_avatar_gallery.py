#!/usr/bin/env python3
"""Patch the avatar picker with a visible WebView fallback if its gallery JS fails."""
from pathlib import Path

path = Path("source/mansi/app/src/main/java/com/jarvis/assistant/ui/settings/OverlayAvatarActivity.kt")
if not path.is_file():
    raise SystemExit(f"Avatar picker source not found: {path}")
source = path.read_text(encoding="utf-8")
marker = "MANSI_AVATAR_GALLERY_FALLBACK_V1"
if marker in source:
    print("Avatar gallery fallback already installed.")
    raise SystemExit(0)

needle = """                avatarGallery.evaluateJavascript(
                    "window.setGalleryTheme && window.setGalleryTheme('#${themeColor(R.attr.themeTextPrimary)}', '#${themeColor(R.attr.themeAccent)}')",
                    null
                )
"""
replacement = needle + r'''
                // MANSI_AVATAR_GALLERY_FALLBACK_V1: recover if the WebView page loaded
                // but its inline gallery script failed, leaving the blank area seen in reports.
                avatarGallery.evaluateJavascript(
                    """
                    (function() {
                      const gallery = document.getElementById('gallery');
                      if (!gallery || gallery.children.length > 0) return;
                      const choices = [
                        ['alien','👽'],['blob','🟢'],['cat','🐱'],['circle','🟣'],
                        ['cloud','☁️'],['droid','🤖'],['drop','💧'],['flower','🌼'],
                        ['ghost','👻'],['hexagon','🔷'],['mech','🦾'],['pebble','🪨'],
                        ['pill','💜'],['puddle','🩷'],['square','🟦'],['star','⭐'],
                        ['triangle','🔺']
                      ];
                      gallery.style.display = 'grid';
                      gallery.style.gridTemplateColumns = 'repeat(3,minmax(0,1fr))';
                      gallery.style.gap = '10px';
                      gallery.innerHTML = choices.map(([name, emoji]) =>
                        '<button type="button" id="avatar-'+name+'" class="avatar-card" '+
                        'style="min-height:104px;padding:8px;border-radius:16px;border:1px solid #c9b8c4;'+
                        'background:rgba(255,255,255,.65);display:flex;flex-direction:column;'+
                        'align-items:center;justify-content:center;gap:5px;color:#4b3042;font-size:12px" '+
                        'onclick="window.JarvisAvatarPicker && window.JarvisAvatarPicker.selectAvatar(&quot;'+name+'&quot;)">'+
                        '<span style="font-size:30px;line-height:42px">'+emoji+'</span>'+
                        '<span style="text-transform:capitalize">'+name+'</span></button>'
                      ).join('');
                      window.setSelectedAvatar = name => {
                        document.querySelectorAll('.avatar-card').forEach(card => {
                          card.classList.remove('selected');
                          card.style.outline = 'none';
                        });
                        const selected = document.getElementById('avatar-'+name);
                        if (selected) { selected.classList.add('selected'); selected.style.outline = '2px solid #ff7043'; }
                      };
                      if (window.JarvisAvatarPicker) window.JarvisAvatarPicker.pageReady();
                    })();
                    """.trimIndent(),
                    null
                )
'''
if needle not in source:
    raise SystemExit("Could not find onPageFinished insertion point; source left unchanged.")
path.write_text(source.replace(needle, replacement, 1), encoding="utf-8")
print("Installed resilient avatar gallery fallback.")
