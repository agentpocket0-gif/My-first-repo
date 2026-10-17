# 🎮 Idea → Game → APK (Bina Coding!)

**Aap sirf game ka idea likho — AI poora game banayega (2D ya 3D), APK build hoga, download ho jayega.** Ek line coding nahi karni padegi.

## ✨ 3D games bhi!
Pipeline ab **3D** games bhi bana sakta hai — Three.js (MIT license, 100% legal & free) ke saath:
- Run workflow karte time **Game type** mein `three` (3D) ya `canvas2d` (2D) chuno — **default 3D hai**
- 3D engine build ke waqt game ke andar automatically embed ho jata hai — game phir bhi **fully offline** chalta hai

## One-time setup (2 minute)
1. **DeepSeek API key lo**: [platform.deepseek.com](https://platform.deepseek.com) → API Key banayein
2. **Key repo mein add karo**:
   - Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   - Name: `DEEPSEEK_API_KEY` · Value: aapki key
   - (Optional) `DEEPSEEK_MODEL` secret se model change (default: `deepseek-chat`)

## Game kaise banayein

### Tareeka 1 — Actions tab (sabse aasan)
1. Repo → **Actions** → **Build Game APK** → **Run workflow**
2. Idea likho (Hindi ya English), Game type chuno (3D default), Run dabao
3. 5-10 minute mein: **Artifacts** section mein `game-apk` + **Releases** page mein APK link

### Tareeka 2 — Issue se
1. **Issues** → **New Issue** — title: game ka naam, body: pura idea
2. Label `game-idea` lagao (3D default hai)
3. Pipeline apne aap chalega, APK Release mein aa jayega

## Phone mein kaise chalayein
APK download karo → kholo → **Install unknown apps** allow karo → khelo! 🎉

## Kya ban sakta hai / kya nahi
| Ho sakta hai | Nahi hota |
|---|---|
| 2D: Snake, Flappy-type, runner, puzzle, arcade | Online multiplayer |
| 3D: highway racer, obstacle dodger, space flyer, maze, tunnel runner | GTA/PUBG jaise bade open-world 3D games |
| Hindi + English UI, touch controls | High-end commercial graphics |
| 80-90% cases mein chalne wala game | 100% guarantee (fail ho toh dobara run karo) |

**3D ke liye tip:** idea mein detail likho — camera kahan, player kya karta hai, kaise score hota hai. Simple 3D ideas (racer, dodger, flyer) sabse achhe bante hain.

## Customization (optional)
- AI ka style: `scripts/generate_game.py` mein `system_prompt()` edit karo
- Fallback template: `game/index.html` change karo

## ⚖️ Legal note
- Sirf **apne original ideas** ya **open-source games** ke liye use karo
- Kisi copyrighted game ka code copy karke assets badalna bhi **illegal** hai — code bhi copyright hota hai
- Clean-room approach: game ka behavior dekho, apna code scratch se likho, apne assets lagao

## Troubleshooting
- **Build fail?** Dobara run karo (AI kabhi-kabhi galat code deta hai)
- **Game adhoora/khali?** Idea mein zyada detail likho; ya engine 2D try karo (zyada reliable)
- **3D game black screen?** Dobara run karo ya idea simple karo
- **DeepSeek error?** Key aur account balance check karo

---
*Yeh pipeline GitHub Actions par chalta hai — aapke phone ya computer par kuch install nahi karna padta.*