<h1>JellyChat</h2>

<p>
  <a href="https://defichainwiki.com/jellychat">
    <img
      src="https://badgen.net/badge/🚀%20Open/JellyChat?color=red"
    />
  </a>
  <a href="https://t.me/+nl8AbyS6izZjNjc0">
    <img
      src="https://badgen.net/badge/🗯%20Join%20us%20on/Telegram/1a98fc"
    />
  </a>
  <a>
    <img
      src="https://badgen.net/https/jellychat.fly.dev/human_message_count"
    />
  </a>
</p>

<h2>Deployments</h2>

<h3>Production</h3>

<p>
  <a
    href="https://github.com/0ptim/JellyChat/actions/workflows/fly_production.yml"
  >
    <img
      src="https://github.com/0ptim/JellyChat/actions/workflows/fly_production.yml/badge.svg"
    />
  </a>
  <a
    href="https://github.com/0ptim/JellyChat/actions/workflows/supabase_production.yml"
  >
    <img
      src="https://github.com/0ptim/JellyChat/actions/workflows/supabase_production.yml/badge.svg"
    />
  </a>
  <a
    href="https://github.com/0ptim/JellyChat/actions/workflows/wiki_scraping_production.yml"
  >
    <img
      src="https://github.com/0ptim/JellyChat/actions/workflows/wiki_scraping_production.yml/badge.svg"
    />
  </a>
</p>

<h3>Staging</h3>

<p>
  <a
    href="https://github.com/0ptim/JellyChat/actions/workflows/fly_staging.yml"
  >
    <img
      src="https://github.com/0ptim/JellyChat/actions/workflows/fly_staging.yml/badge.svg"
    />
  </a>
  <a
    href="https://github.com/0ptim/JellyChat/actions/workflows/supabase_staging.yml"
  >
    <img
      src="https://github.com/0ptim/JellyChat/actions/workflows/supabase_staging.yml/badge.svg"
    />
  </a>
  <a
    href="https://github.com/0ptim/JellyChat/actions/workflows/wiki_scraping_staging.yml"
  >
    <img
      src="https://github.com/0ptim/JellyChat/actions/workflows/wiki_scraping_staging.yml/badge.svg"
    />
  </a>
</p>

JellyChat is a project that aims to create a chatbot that can answer questions about DeFiChain and its ecosystem.

❗ There are many people which want to learn more about DeFiChain and its ecosystem. However, it is not always easy to find the right information. Also, many people struggle to take in information from various articles in a wiki.

✨ JellyChat aims to solve this by providing the ability for users to interactively ask questions and have an ongoing conversation.

## Main Objectives

- Make learning about DeFiChain fun.
- Be able to answer general questions about DeFiChain and its ecosystem.
- Be able to answer questions involving on-chain data.
- Behave like Jelly (the DeFiChain mascot).
- Feel like a friend that you can ask anything.

## Architecture

This gives a **high-level** overview of the architecture. For more details, please refer to the individual components.

[📂 Download diagram source](./docs/process.drawio)

### Accounts and History

Identification of accounts is done with a `user_token` which the client needs to store. The client then posts this `user_token` to `/history` and gets the history back if the account exists. If the account does not exist, a new one is created automatically.

![Architectural overview of accounts and history](./docs/process-Accounts-History.png)

### Input/Output Flow

The client posts a user message and a `user_token` to `/user_message`. A LangChain agent will be created for the specific `user_token` and the memory is filled from the history. The agent will then analyze the user's message and return an answer. The answer is then returned to the client and also added to the history.

![Architectural overview of input and output flow](./docs/process-Input-Output-Flow.png)

## Key Components

The Repository contains the following key components.

### 🌐 `/backend`

The backend is a Flask API that receives questions and returns answers. It uses a LangChain agent to analyze the question and then uses various tools to best answer the question.

[Details 🔎](./backend/README.md)

### 💽 `/data`

We use Supabase to store:

- Users
- Messages
- QA data
- Embeddings

[Details 🔎](./data/README.md)

### ⚡️ `/job`

Contains a script that is executed daily at 02:45 UTC via a GitHub action. However, it only runs if there have been changes to the [`/docs`](https://github.com/0ptim/DeFiChainWiki/tree/main/docs) directory within [0ptim/DeFiChainWiki](https://github.com/0ptim/DeFiChainWiki) in the past 24 hours. If changes are detected, the script scrapes the [DeFiChainWiki](defichainwiki.com) to generate new embeddings. These embeddings are then stored in Supabase in the table `embeddings`.

[Details 🔎](./job/README.md)

## Workflow and Environments

The `main` branch resembles the production code. When a feature is ready, a pull request is created onto `main`. This will trigger the staging actions so the changes can be tested on the staging environment.

- [💽 Staging Database](https://supabase.com/dashboard/project/iajfqvpslzrtmvekqwpv)
  - Endpoint: https://iajfqvpslzrtmvekqwpv.supabase.co
- [🌐 Staging Backend](https://fly.io/apps/jellychat-staging)
  - Endpoint: https://jellychat-staging.fly.dev

When the pull request is merged (changes are pushed to `main`), the production action will be triggered and the changes will be deployed to production.

- [💽 Production Database](https://supabase.com/dashboard/project/cofmxsabxteiidryklyg)
  - Endpoint: https://cofmxsabxteiidryklyg.supabase.co
- [🌐 Production Backend](https://fly.io/apps/jellychat)
  - Endpoint: https://jellychat.fly.dev
