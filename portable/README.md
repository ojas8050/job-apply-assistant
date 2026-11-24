# Chat mode: use this with ChatGPT, Gemini or Claude chat

This mode needs **no installation and no browser tool**. It works in any chat assistant that lets
you save custom instructions. The assistant does the thinking and writing (profile, scoring,
tailored resume text, cover letters, form answers, interview prep, follow-ups) and **you** do the
clicking and submitting.

## What it can and cannot do

| It can | It cannot |
|---|---|
| Build your profile from your resume | Search job boards for you |
| Score a job description you paste | Log in to anything |
| Rewrite your resume for one job (true facts only) | Fill or submit forms |
| Write cover letters and answer form questions | Check your Applied lists |
| Check a job against your tracker for duplicates | Remember things between chats on its own |
| Interview prep, mock interviews, follow-up drafts | Install anything on your computer |

For searching and filling forms automatically you need the full agent mode (see the main
README), which runs in Claude Code or another assistant with a browser tool.

## Set it up (about 5 minutes)

Menu names change from time to time, so look for the closest match.

**ChatGPT**
1. Create a custom GPT (the "Create" option under GPTs).
2. Paste the whole of `ASSISTANT-PROMPT.md` into the **Instructions** box. It is about 6,100
   characters, under the 8,000-character limit.
3. Optional: upload `../references/profile-template.md`, `../references/match-rubric.md` and
   `../references/tailoring.md` as knowledge files.
4. Save it as private ("Only me"), then start a chat with it.

**Gemini**
1. Create a Gem (under Gems, "New Gem").
2. Paste the whole of `ASSISTANT-PROMPT.md` into the instructions.
3. Optional: add the same three files from `../references/` as knowledge.

**Claude (chat)**
1. Create a Project and paste the whole of `ASSISTANT-PROMPT.md` into the project instructions.
2. Optional: add the same three files as project knowledge.

**Any other assistant:** paste `ASSISTANT-PROMPT.md` as the first message of a chat.

## How to use it
1. Start a chat and say "hello". It asks for your resume and a few questions, then shows your
   profile. **Copy the profile and keep it in a note.** Chats can forget, so paste it back at the
   start of future chats.
2. Find jobs yourself on the boards. When one looks interesting, paste its description and type
   `score`, then `tailor`, then `cover`.
3. Paste the form's questions and type `answers`.
4. Keep a small table of jobs you applied to. Paste it back and use `track` before applying, so
   you don't apply twice to the same job on two boards.
5. Use `prep <company>`, `mock`, `followup` and `review` as you go.

## Privacy
Your resume and answers go to whichever assistant you use, under that service's privacy
settings. Don't paste passwords, ID numbers or bank details; the prompt tells the assistant
never to ask for them.
