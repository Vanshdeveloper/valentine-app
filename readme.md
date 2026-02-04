# Valentine Flask App 💌

A cheeky, charming, and slightly spicy single-page Valentine proposal built with a Jinja/HTML template and sweet visuals. Drop in your names, a flirtatious message, and deliver the vibe — responsibly seductive. 😉💌

## Live Url 🔗
 https://valentine-app-hgeu.onrender.com/

## Preview 👀
Open `templates/love.html` in your browser (or serve via your web framework) to see the card: floating hearts, a rose-petals hero image, and two big buttons — "Yes, I will!" and "No" (cute either way). 🌹✨

## Features ✨
- Elegant, responsive card layout with floating hearts ❤️
- Jinja placeholders: {{ your_name }}, {{ crush_name }}, {{ message }}, {{ unique_id }} 🧩
- Clickable response handler that sends Yes/No back to `/response/{{ unique_id }}/<answer>` ✅❌
- Easy to customize fonts, styles, and imagery — make it as sassy as you dare 😏

## Quick Start (Windows) 🪟
1. Add your values to the rendering context (`your_name`, `crush_name`, `message`, `unique_id`). 📝
2. Serve the template with your web app (Flask, Django, etc.) or open the file directly. 🚀
3. Click the buttons to test responses — alerts confirm selection. 🎯

## Customize (spice it up) 🌶️
- Swap the hero image: replace `/static/rose-petals-crush-side-img.png` 📸
- Edit the copy: change the main heading or button text for extra sass (“Be mine?”, “Heck yes!”) 💬
- Tweak colors in the `<style>` block to match your mood or aesthetic 🎨
- Add confetti, sounds, or subtle animations for max effect 🎉🔊

## Deployment 🚢
Serve through your usual static/template pipeline. Ensure the response route (`/response/{{ unique_id }}/<answer>`) stores results or triggers notifications so you can see who said yes (or ghosted you). 📬

## Contributing 🤝
Want to add new message templates, animations, or a cheekier UI? Contributions welcome — keep it playful and kind. 🥂

Made with ♥, a wink, and a hint of mischief. 😘
