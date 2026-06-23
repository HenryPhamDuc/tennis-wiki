---
title: how to install hermes agent with ollama in linux mint
tags:
  - ai-research
  - nghiên-cứu
source: "Manus-Papers\\how-to-install-hermes-agent-with-ollama-in-linux-mint.md"
updated: 2026-06-20
---


Ask Gemini: how to install hermes agent with ollama in linux mint to run agentic tasks?



To install [Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation) with [Ollama](https://docs.ollama.com/linux) on Linux Mint, you need to install the Ollama background service, download an agent-friendly local model, run the official Nous Research install script, and link the agent to your local endpoint. [1, 2]

Follow this step-by-step terminal workflow to build your private, local AI system. [3]

1. Install and Start Ollama

---------------------------

Open your Linux Mint terminal window and execute the standard Linux installation script provided by Ollama: [2, 4]
    curl -fsSL https://ollama.com | sh

Verify that the service is up and running natively on port 11434: [5]
    curl http://localhost:11434

_(You should see a brief "Ollama is running" text confirmation)._ [4]

2. Pull an Agent-Optimized Model [1]

------------------------------------

AI agents require specific models trained heavily on structured function calls (tool calling) to operate your system properly. Highly recommended open models include Gemma 4 or Qwen 2.5. [2, 3, 6]

* Important Pro-Tip: In the [Reddit community](https://www.reddit.com/r/AIforDevs/comments/1stiqkj/hermes_agent_ollama_1minute_local_setup/) for r/hermesagent, it is recommended to set a minimum of 64k context length when running local Ollama instances to prevent the agent from cutting off mid-task. [4]

Download your chosen brain (for example, Google's Gemma 4): [7]
    ollama run gemma4

3. Install Hermes Agent [8]

---------------------------

Download and execute the official installer script hosted by Nous Research: [1, 9]
    curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

Once the installer concludes, reload your bash configuration so your terminal recognizes the global environment commands: [10, 11, 12]
    source ~/.bashrc

4. Link Hermes to your Ollama Endpoint

--------------------------------------

By default, Hermes Agent attempts to route queries to paid cloud providers like Anthropic's Claude. Force it to map directly to your machine's private background server: [2, 13]

1. Run the built-in model configuration wizard:
      hermes model

2. When prompted for a provider, select Ollama (or manually input an OpenAI-compatible custom endpoint).

3. For the Base URL, point it precisely to:  
   `http://127.0.0.1:11434/v1`

4. Type the exact string name of the model you downloaded in Step 2 (e.g., `gemma4`). Leave the API key field entirely blank. [1, 2, 7, 9, 13]

5. Launch the Dashboard

-----------------------

You can run the interactive agent environment right from the native command line, or boot its full interface: [13, 14]
    hermes desktop

If you prefer a clean web-browser interface to interact with your agent's historical memory logs and tool permissions, initiate the backend local server explicitly: [14]
    hermes dashboard --tui

Open your preferred Linux web browser and navigate to `http://localhost:9119` to view your new workspace. [14]

* * *

If you want to customize this further, let me know:

* What specific computer tasks do you want Hermes to automate? (e.g. web browsing, file management, coding)
* Do you want to connect it to an external app like Telegram or Discord for remote control? [13, 14, 15]
  
  

[1] [https://docs.ollama.com](https://docs.ollama.com/integrations/hermes)

[2] [https://openclawlaunch.com](https://openclawlaunch.com/guides/hermes-agent-ollama)

[3] [https://www.youtube.com](https://www.youtube.com/watch?v=NlmMudE20S0)

[4] [https://www.reddit.com](https://www.reddit.com/r/AIforDevs/comments/1stiqkj/hermes_agent_ollama_1minute_local_setup/)

[5] [https://build.nvidia.com](https://build.nvidia.com/spark/hermes-agent/instructions)

[6] [https://www.youtube.com](https://www.youtube.com/watch?v=aAQWB3-XD5s)

[7] [https://www.reddit.com](https://www.reddit.com/r/AISEOInsider/comments/1tz1f9u/hermes_ai_agent_ollama_free_1_click_setup/)

[8] [https://docs.openwebui.com](https://docs.openwebui.com/getting-started/quick-start/connect-an-agent/hermes-agent/)

[9] [https://hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/getting-started/installation)

[10] [https://medium.com](https://medium.com/data-science-in-your-pocket/hermes-agent-with-ollama-setup-b0a442f53241)

[11] [https://platform.xiaomimimo.com](https://platform.xiaomimimo.com/docs/en-US/integration/hermes-agent)

[12] [https://medium.com](https://medium.com/data-science-in-your-pocket/hermes-agent-with-ollama-setup-b0a442f53241)

[13] [https://medium.com](https://medium.com/data-science-collective/hermes-agent-ollama-fastest-way-to-install-locally-f2b13d958e32)

[14] [https://www.youtube.com](https://www.youtube.com/watch?v=JtiPB1Mg1ZA)

[15] [https://openclawlaunch.com](https://openclawlaunch.com/guides/install-hermes-agent)





Purpose: running process like creating research paper with external websearch and Youtube videos to include in the papers. Use telegram for remote control



To turn your Hermes Agent into a remotely controllable research assistant that can watch videos and browse the web, you need to configure three components: the Gateway (for Telegram), the Skills (for research/YouTube), and the Workflow (how to prompt it). [1, 2, 3]

1. Enable Remote Control (Telegram) [4]

---------------------------------------

The Hermes "Gateway" allows the agent to run as a background server that you can text from anywhere. [5, 6]

1. Create a Telegram Bot:
   
   * Open Telegram and search for @BotFather.
   * Send the message `/newbot`.
   * Name it (e.g., "MyResearchBot") and get your HTTP API Token. [7, 8, 9, 10, 11]

2. Get Your User ID:
   
   * Search for @userinfobot in Telegram and click Start.
   * Copy your numeric ID (e.g., `12345678`). You need this so _only you_ can control the bot. [12, 13, 14, 15]

3. Configure the Gateway:  
   Back in your Linux Mint terminal, run:
      hermes gateway setup
* Select Telegram from the list.
* Paste your API Token and User ID when prompted. [2, 4, 16, 17, 18]
4. Start the Listener:
      hermes gateway start
* _Tip:_ To keep this running 24/7 even if you close the terminal, run it inside a [tmux or systemd service](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram). [19]
2. Install Research Skills (Web & YouTube)

------------------------------------------

By default, Hermes has limited access to the outside world. You must explicitly "teach" it these skills. [20]

Run the skills menu:
    hermes skills

Search for and install these two critical skills:

* `browser-harness` (or `web-search`): This allows the agent to run google searches and read page content. [21]

* `youtube-skills` (or `youtube-content`):
  
  * _Note:_ The community-built `youtube-skills` (by therohitdas) is often better than the default because it can pull transcripts. This is essential for "watching" videos quickly.
  * If you don't see it in the menu, you may need to add it manually via the configuration file or by creating a custom skill file in `~/.hermes/skills/`. [1, 22]
3. The Research Workflow

------------------------

Once your agent is running and has skills, open your Telegram chat with your bot. You don't need to write code; you just need a robust prompt that forces the agent to use its new tools. [23, 24]

Copy-paste this prompt into Telegram:

> Task: Create a comprehensive research paper on [INSERT TOPIC HERE].
> 
> Process:
> 
> 1. Web Search: Find 3-5 authoritative articles on the topic. Summarize the key arguments.
> 
> 2. Video Analysis: Search YouTube for "[Topic] analysis" or "[Topic] documentary".
>    
>    * _Action:_ Use the YouTube tool to pull the transcripts of the top 2 videos.
>    * _Action:_ Extract unique insights or quotes from these transcripts that weren't in the articles.
> 
> 3. Synthesis: Write a structured report with the following sections:
>    
>    * Abstract: Brief summary of the findings.
>    * Literature Review: Insights from the web articles.
>    * Visual/Media Insights: Unique points from the video analysis.
>    * Conclusion: Your final synthesis.
> 
> Output: Send the final report as a markdown text message here.

4. Viewing the Output

---------------------

* Telegram: The agent will reply directly in the chat with the text of the paper.
* Files: If the paper is too long, tell the agent: _"Save this report to a file named 'research_paper.md' in my Documents folder."_ You can then access it on your Linux machine later. [25]

Troubleshooting:

* Context Window: If the YouTube transcripts are huge, the agent might "forget" earlier instructions. Ensure you are using a model with at least 32k or 64k context (like `command-r` or `qwen2.5`) in your Ollama setup. [26, 27]
* Speed: Reading transcripts and browsing takes time. The agent might take 2-5 minutes to reply. Do not send new messages while it is "typing" (processing).
  
  

[1] [https://github.com](https://github.com/0xNyk/awesome-hermes-agent)

[2] [https://www.remoteopenclaw.com](https://www.remoteopenclaw.com/blog/hermes-agent-telegram-setup)

[3] [https://www.instagram.com](https://www.instagram.com/reel/DWhAlCUD842/)

[4] [https://www.youtube.com](https://www.youtube.com/watch?v=S8kiLQbEL-0)

[5] [https://www.bluehost.com](https://www.bluehost.com/blog/run-hermes-agent-vps/)

[6] [https://medium.com](https://medium.com/@ishank.iandroid/hermes-agent-the-self-improving-ai-that-just-blew-my-mind-11fcfec8c30e)

[7] [https://www.grandlinux.com](https://www.grandlinux.com/en/blogs/hermes-agent-install.html)

[8] [https://www.digitalocean.com](https://www.digitalocean.com/community/tutorials/how-to-run-hermes-agent)

[9] [https://medium.com](https://medium.com/@anhaia.gabriel/how-to-control-claude-code-from-telegram-using-hermes-ide-3d81c6705f8c)

[10] [https://ai.gopubby.com](https://ai.gopubby.com/build-and-deploy-a-self-rag-based-llm-application-on-telegram-using-langgraph-and-aws-services-86fb674dfcd2)

[11] [https://hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant)

[12] [https://www.mindstudio.ai](https://www.mindstudio.ai/blog/hermes-agent-vps-telegram-setup-guide)

[13] [https://github.com](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/telegram.md)

[14] [https://hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram)

[15] [https://medium.com](https://medium.com/data-and-beyond/hermes-agent-setup-windows-2026-wsl-b19b536c7bb8)

[16] [https://www.binance.com](https://www.binance.com/en/square/post/312004119668065)

[17] [https://www.interserver.net](https://www.interserver.net/tips/kb/deploy-hermes-agent-on-your-vps-and-talk-to-it-from-telegram-24-7/)

[18] [https://medium.com](https://medium.com/@anhaia.gabriel/how-to-control-claude-code-from-telegram-using-hermes-ide-3d81c6705f8c)

[19] [https://www.bluehost.com](https://www.bluehost.com/blog/run-hermes-agent-vps/)

[20] [https://apidog.com](https://apidog.com/blog/use-hermes-agent/)

[21] [https://petronellatech.com](https://petronellatech.com/blog/hermes-agent-ai-guide/)

[22] [https://github.com](https://github.com/0xNyk/awesome-hermes-agent/blob/main/README.md)

[23] [https://www.interserver.net](https://www.interserver.net/tips/kb/deploy-hermes-agent-on-your-vps-and-talk-to-it-from-telegram-24-7/)

[24] [https://www.hostinger.com](https://www.hostinger.com/ph/tutorials/how-to-set-up-hermes-agent)

[25] [https://www.reddit.com](https://www.reddit.com/r/LocalLLM/comments/1tm7b8d/i_made_a_portable_version_of_hermes_agent_that/)

[26] [https://www.firecrawl.dev](https://www.firecrawl.dev/blog/hermes-agent)

[27] [https://blakecrosley.com](https://blakecrosley.com/guides/hermes)



Does it cost?



No, it does not cost anything. Running this setup is completely free.

Because you are using local tools on Linux Mint, you avoid all subscription fees and pay-per-use token charges.
Why It Is Free
--------------

* Ollama & Models: Ollama is open-source, and models like `gemma4` or `qwen2.5` are completely free to download and use.
* Hermes Agent: The software and its skills ecosystem are open-source and free.
* Telegram Bots: Creating and running a bot via Telegram's BotFather is a free service provided by Telegram.
* Web & YouTube Skills: The agent uses free web scraping and public transcript APIs to pull data. [1, 2, 3, 4, 5]

The Only "Hidden" Costs
-----------------------

* Electricity & Hardware: Running large AI models locally uses a lot of computer processing power. Your computer's power bill might rise slightly if you run heavy research tasks 24/7.
* Time: Because the model runs on your own hardware (instead of massive corporate data centers), generating a full research paper will be slower. It depends entirely on how powerful your computer's graphics card (GPU) or processor (CPU) is. [6]

* * *

If you want to make sure your system can handle this efficiently, tell me:

* What CPU and GPU (Graphics Card) do you have in your Linux Mint machine?
* How much System RAM does your computer have?

I can recommend the exact model size (e.g., 1.5B, 3B, 7B, or 8B parameters) that will run fastest on your specific hardware. [7, 8]



[1] [https://www.instagram.com](https://www.instagram.com/reel/DXE8XPxgk2o/)

[2] [https://priyalwalpita.medium.com](https://priyalwalpita.medium.com/4-open-source-ai-projects-that-will-change-how-you-ship-code-forever-dba72ec41c35)

[3] [https://dev.to](https://dev.to/challenges/hermes-agent-2026-05-15)

[4] [https://www.vellum.ai](https://www.vellum.ai/blog/best-workspace-agents-chatgpt-alternatives)

[5] [https://github.com](https://github.com/NousResearch/hermes-agent/blob/main/hermes-already-has-routines.md)

[6] [https://dev.to](https://dev.to/arshtechpro/hermes-agent-a-self-improving-ai-agent-that-runs-anywhere-2b7d)

[7] [https://telnyx.com](https://telnyx.com/llm-library/nous-hermes-2-mistral-7b-dpo)

[8] [https://vertu.com](https://vertu.com/ai-tools/nous-research-hermes-4-vs-hermes-3-deep-comparison-and-practical-guide)



My PC SPecs: CPU i7 with 16GB Ram



With an Intel Core i7 CPU and 16GB of system RAM, you do not have a dedicated graphics card (GPU) with its own Video RAM (VRAM) [r/hermesagent]. Because your processor has to handle both the AI model and your Linux Mint operating system, you must use smaller, highly optimized models to prevent your computer from freezing.
🌟 The Golden Rule for 16GB RAM
-------------------------------

To keep your system stable, the AI model should never take up more than 8GB to 10GB of space, leaving the remaining RAM for Linux Mint and your web browser.
🧊 Recommended Models for Your Setup
------------------------------------

Open your terminal and pull one of these specific, agent-friendly models:

* Option 1: Llama 3.2 (3B) — _Highly Recommended for Speed_  
  This model fits completely into your RAM, leaves plenty of room for long YouTube transcripts, and runs at a usable speed on a CPU.
  
      ollama run llama3.2

* Option 2: Qwen 2.5 (3B or 7B) — _Best for Deep Research_  
  The Qwen 2.5 family is elite at writing structured code and reasoning through complex data. The 3B version will be fast. The 7B version will give you much better research papers but will process text very slowly on your i7 CPU.
  
      ollama run qwen2.5:3b
  
  

⚡ Essential Optimization for CPU Running
----------------------------------------

Because you are running on a CPU rather than a GPU, a long YouTube transcript could slow the agent down significantly. Run this command to tell Ollama to utilize all available processor cores on your i7:
    echo "export OLLAMA_NUM_PARALLEL=1" >> ~/.bashrcsource ~/.bashrc

_(This limits Ollama to processing one intense request at a time, preventing your CPU from hitting 100% usage and lagging your entire desktop)._

* * *

Now that we know your hardware limits, we need to map Hermes to your new model. Would you like the quick terminal commands to swap your Hermes configuration from Gemma over to the faster `llama3.2` or `qwen2.5:3b` model?

With an Intel Core i7 CPU and 16GB of system RAM, you do not have a dedicated graphics card (GPU) with its own Video RAM (VRAM) [r/hermesagent]. Because your processor has to handle both the AI model and your Linux Mint operating system, you must use smaller, highly optimized models to prevent your computer from freezing.
🌟 The Golden Rule for 16GB RAM
-------------------------------

To keep your system stable, the AI model should never take up more than 8GB to 10GB of space, leaving the remaining RAM for Linux Mint and your web browser.
🧊 Recommended Models for Your Setup
------------------------------------

Open your terminal and pull one of these specific, agent-friendly models:

* Option 1: Llama 3.2 (3B) — _Highly Recommended for Speed_  
  This model fits completely into your RAM, leaves plenty of room for long YouTube transcripts, and runs at a usable speed on a CPU.
  
      ollama run llama3.2

* Option 2: Qwen 2.5 (3B or 7B) — _Best for Deep Research_  
  The Qwen 2.5 family is elite at writing structured code and reasoning through complex data. The 3B version will be fast. The 7B version will give you much better research papers but will process text very slowly on your i7 CPU.
  
      ollama run qwen2.5:3b
  
  

⚡ Essential Optimization for CPU Running
----------------------------------------

Because you are running on a CPU rather than a GPU, a long YouTube transcript could slow the agent down significantly. Run this command to tell Ollama to utilize all available processor cores on your i7:
    echo "export OLLAMA_NUM_PARALLEL=1" >> ~/.bashrcsource ~/.bashrc

_(This limits Ollama to processing one intense request at a time, preventing your CPU from hitting 100% usage and lagging your entire desktop)._

* * *

Now that we know your hardware limits, we need to map Hermes to your new model. Would you like the quick terminal commands to swap your Hermes configuration from Gemma over to the faster `llama3.2` or `qwen2.5:3b` model?

compare with free claude or Manus free, how is this model working?



To be honest, the local setup on your hardware (i7, 16GB RAM) will be significantly "dumber" than Claude or Manus, but it is unlimited, private, and uncensored. [1]

You are trading intelligence for control.

Because you are forced to use small models (3B or 7B parameters) to fit in your RAM, your agent will struggle with complex reasoning that Claude (likely 70B+ parameters) finds easy.
The Direct Comparison
---------------------

| Feature [2, 3, 4, 5, 6] | Local Hermes (Your Setup)           | Manus / Claude (Free)                      |
| ----------------------- | ----------------------------------- | ------------------------------------------ |
| Intelligence            | 🧠 Low (Like a smart high schooler) | 🧠 High (Like a PhD researcher)            |
| Cost                    | $0 (Unlimited 24/7 use)             | $0 (But strictly limited daily)            |
| Privacy                 | 🔒 100% Private (Data stays on PC)  | ❌ Zero (They train on your data)           |
| Speed                   | 🐢 Slow (Depends on your i7 CPU)    | ⚡ Fast (Runs on massive Cloud GPUs)        |
| Capabilities            | ✅ Web & YouTube (With setup)        | ⚠️ Limited (Claude Free can't browse deep) |
| Censorship              | ✅ None (You control the rules)      | ❌ High (Refuses "unsafe" topics)           |

* * *

1. The "Brain Size" Problem

---------------------------

This is the most critical difference.

* Your Local Model (Llama 3.2 3B): Has ~3 billion "neurons." It is great for summarizing text or simple commands, but if you ask it to _Synthesize a research paper from 3 conflicting sources_, it might get confused or hallucinate facts. [7]

* Manus / Claude: Likely runs on models with 70 billion to 400 billion neurons. They can hold complex logic in their head without forgetting the rules.
2. The "Free Tier" Trap (Manus & Claude)

----------------------------------------

While they are smarter, they put you in a cage:

* Manus Free: You get 300 credits per day. A single "deep research" task where it browses the web and writes a report could burn mostly all your daily credits in one go. If it makes a mistake, you have to wait 24 hours to try again. [8]

* Claude Free: You get very few messages (often 5-10) every few hours. Once you hit the limit, you are locked out. Also, the free version of Claude cannot browse the web or watch YouTube videos for you; it is text-only. [9]
3. Why Use Hermes Instead?

--------------------------

Even though it is "dumber," Hermes on Linux Mint is better for automation:

* Remote Control: You can't text Claude from Telegram to start a job while you are driving. You _can_ do that with Hermes.
* Looping: You can make Hermes try a task 100 times in a row until it gets it right. Doing that on Manus would cost $200+ in credits; on your Linux Mint, it just costs electricity.

My Recommendation
-----------------

Since you have an i7 and 16GB RAM:

1. Use Hermes/Ollama for "Drafting": Let it do the heavy lifting—reading 50 website articles, summarizing YouTube videos, and building the _outline_ of your paper. It reads for free. [10]
2. Use Claude for "Polishing": Take the rough text your local agent produced and paste it into Claude (Free) to rewrite it professionally. This saves your precious Claude messages for the final polish.

Would you like a "System Prompt" that tells Hermes to act as a _Researcher_ specifically designed to summarize content for a bigger model like Claude?



[1] [https://privatellm.app](https://privatellm.app/blog/eva-qwen-uncensored-ai-role-play-iphone-ipad-mac)

[2] [https://drlee.io](https://drlee.io/how-we-cut-our-clients-ai-costs-by-97-small-language-models-slms-using-phi-3-and-n8n-while-af2bbe0941fd)

[3] [https://www.igmguru.com](https://www.igmguru.com/blog/manus-ai)

[4] [https://www.xda-developers.com](https://www.xda-developers.com/claude-free-tier-review/)

[5] [https://aimaker.substack.com](https://aimaker.substack.com/p/manus-claude-code-agents-review)

[6] [https://www.binance.com](https://www.binance.com/en/square/post/24491105631345)

[7] [https://www.reddit.com](https://www.reddit.com/r/LocalLLaMA/comments/1giy3pt/your_best_3b_model_llama_32_kwen_25_or_phi_35/)

[8] 

[9] [https://www.eweek.com](https://www.eweek.com/artificial-intelligence/gpt4-vs-claude/)

[10] [https://spectrumailab.com](https://spectrumailab.com/blog/manus-ai-pricing-plans-cost-guide-2026)



Copy and paste the system prompt block below into your terminal using the Hermes model configuration tool, or send it directly as the first message to your Telegram bot.

This prompt is engineered to squeeze the absolute maximum performance out of a smaller 3B or 7B local model by forcing it to focus only on raw data gathering and extraction, rather than wasting its limited processing power trying to write fancy prose.
📝 The Core System Prompt
-------------------------

    You are an advanced, local Research Extraction Agent running on constrained hardware. Your single goal is to gather, verify, and structure raw data so it can be exported to a larger Cloud AI (like Claude) for final writing. Do not write flowery essays. Do not use conversational filler. Be highly dense, factual, and precise.When a user gives you a research topic, execute these strict steps:1. Use your browser/search tool to find the top 3-5 authoritative sources. Extract key data points, statistics, dates, and direct quotes.2. Use your YouTube tool to fetch transcripts of relevant videos. Extract unique insights, expert names, and case studies not found in the text articles.3. Organize all gathered information into a structured "Raw Research Brief" using the exact Markdown format below.### RAW RESEARCH BRIEF## 1. CORE THEMES & DATA- [Theme 1 Name]: [ Bulleted raw facts, statistics, and verifiable dates ]- [Theme 2 Name]: [ Bulleted raw facts, statistics, and verifiable dates ]## 2. WEB SOURCE EXTRACTS- URL: [Insert Link]  - Key Insights: [2-3 highly specific data points]  - Critical Quote: "[Paste verbatim quote for citations]"## 3. MULTIMEDIA & YOUTUBE EVIDENCE- Video Title/Channel: [Name]  - Transcript Takeaways: [Specific arguments or unique angles raised]  - Timeline/Context: [Any chronological data mentioned]## 4. ANOMALIES & CONTRADICTIONS- [List any conflicting facts found between the web sources and YouTube videos so the user can flag them].

* * *

⚙️ How to apply this to your setup
----------------------------------

Choose whichever method matches how you want to interact with your Hermes Agent:
Method A: Apply permanently in Linux terminal
---------------------------------------------

If you want Hermes to _always_ act this way when you boot it up locally:

1. Open your Linux Mint terminal.
2. Open your system prompts configuration file (usually located at `~/.hermes/system_prompt.txt` or modified during `hermes model` setup).
3. Paste the text block above into the file and save it.

Method B: Apply directly via Telegram
-------------------------------------

If you want to quickly toggle this on or off while controlling it remotely:

1. Open your private Telegram chat with your bot.
2. Simply paste the entire block above into the chat.
3. Follow it up immediately with your command, like: _"Now that you have your system instructions, please research the latest developments in solid-state batteries."_

* * *

Once your local agent finishes compiling this data-heavy markdown summary, you can simply copy and paste its output directly into the free tier of Claude. You can then ask Claude: _"Turn this raw research brief into a professionally polished, 5-page academic paper."_

Let me know if you would like me to help you test the connection to your Telegram bot or verify if your web search skills are firing properly!







Prompt: You are an advanced, local Research Extraction Agent running on constrained hardware. Your single goal is to gather, verify, and structure raw data so it can be exported to a larger Cloud AI (like Claude) for final writing. 

Do not write flowery essays. Do not use conversational filler. Be highly dense, factual, and precise.

When a user gives you a research topic, execute these strict steps:

1. Use your browser/search tool to find the top 3-5 authoritative sources. Extract key data points, statistics, dates, and direct quotes.
2. Use your YouTube tool to fetch transcripts of relevant videos. Extract unique insights, expert names, and case studies not found in the text articles.
3. Organize all gathered information into a structured "Raw Research Brief" using the exact Markdown format below.

### RAW RESEARCH BRIEF

## 1. CORE THEMES & DATA

- [Theme 1 Name]: [ Bulleted raw facts, statistics, and verifiable dates ]
- [Theme 2 Name]: [ Bulleted raw facts, statistics, and verifiable dates ]

## 2. WEB SOURCE EXTRACTS

- URL: [Insert Link]
  - Key Insights: [2-3 highly specific data points]
  - Critical Quote: "[Paste verbatim quote for citations]"

## 3. MULTIMEDIA & YOUTUBE EVIDENCE

- Video Title/Channel: [Name]
  - Transcript Takeaways: [Specific arguments or unique angles raised]
  - Timeline/Context: [Any chronological data mentioned]

## 4. ANOMALIES & CONTRADICTIONS

- [List any conflicting facts found between the web sources and YouTube videos so the user can flag them].
