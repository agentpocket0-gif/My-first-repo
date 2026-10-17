# 🎮 Idea → Game → APK (Bina Coding!)

**Aap sirf game ka idea likho — AI poora game banayega, APK build hoga, download ho jayega.** Ek line coding nahi karni padegi.

## Demo game
Is repo mein pehle se ek demo game hai (`game/index.html` — Space Dodge 🚀).
Jaise hi pipeline chalao, AI aapke idea ka naya game bana dega.

## One-time setup (2 minute)
1. **DeepSeek API key lo**: [platform.deepseek.com](https://platform.deepseek.com) → API Key banayein
2. **Key repo mein add karo**:
   - Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   - Name: `DEEPSEEK_API_KEY`
   - Value: aapki key
   - (Optional) Model change karne ke liye ek aur secret: `DEEPSEEK_MODEL` (default: `deepseek-chat`)

## Game kaise banayein

### Tareeka 1 — Actions tab (sabse aasan)
1. Repo mein **Actions** tab kholo
2. **Build Game APK** workflow chuno (pehli baar "Enable workflows" karna pad sakta hai)
3. **Run workflow** button dabao
4. Idea box mein likho (Hindi ya English), jaise: *ek space game jisme ship asteroid se bachti hai*
5. **Run workflow** dabao — 5-10 minute wait karo
6. Neeche **Artifacts** section mein `game-apk` milega, aur **Releases** page mein APK ka permanent link

### Tareeka 2 — Issue se
1. **Issues** → **New Issue** — title mein game ka naam, body mein pura idea
2. Issue par label `game-idea` lagao
3. Pipeline apne aap chalega, APK Release mein aa jayega

## Phone mein kaise chalayein
1. APK download karo
2. Phone mein kholo → **Install unknown apps** allow karo
3. Game khelo! 🎉

## Kya ban sakta hai / kya nahi
| Ho sakta hai | Nahi hota |
|---|---|
| Simple 2D games: Snake, Flappy-type, runner, puzzle, arcade | Bade 3D / online multiplayer games |
| Hindi + English UI, touch controls | High-end commercial graphics |
| 80-90% cases mein chalne wala game | 100% guarantee (fail ho toh dobara run karo) |

## Customization (optional)
- AI ka style badalne ke liye `scripts/generate_game.py` mein `SYSTEM_PROMPT` edit karo
- Fallback template badalne ke liye `game/index.html` change karo

## ⚖️ Legal note
- Sirf **apne original ideas** ya **open-source games** ke liye use karo
- Kisi copyrighted game ka clone ya renamed copy banana **illegal** hai — is repo ka maqsad creativity aur seekhna hai

## Troubleshooting
- **Build fail?** Workflow dobara run karo — AI kabhi-kabhi galat code deta hai, retry se theek ho jata hai
- **Game adhoora lage?** Idea mein zyada detail likho: kitne levels, kya controls, kya theme, kya score system
- **DeepSeek error?** Key sahi hai aur account mein balance hai — check karo

---
*Yeh pipeline GitHub Actions par chalta hai — aapke phone ya computer par kuch install nahi karna padta.*