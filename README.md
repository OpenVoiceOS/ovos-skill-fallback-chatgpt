# ChatGPT Fallback Skill

When in doubt, ask ChatGPT, powered by [OpenAI Solver](https://github.com/OpenVoiceOS/ovos-solver-plugin-openai-persona).

You need to configure a `key`, get it at https://platform.openai.com/api-keys

Or use a LocalAI (see example below)

## About

Capabilities:

- Remembers what user said earlier in the conversation
- Trained to decline inappropriate requests

Limitations:

- May occasionally generate incorrect information
- May occasionally produce harmful instructions or biased content
- Limited knowledge of world and events after 2021

## Configuration

Under skill settings (`.config/mycroft/skills/skill-ovos-fallback-chatgpt.openvoiceos/settings.json`) you can tweak some parameters for chatGPT.

| Option          | Value                                                                   | Description                                                                           |
| --------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `key`           | `sk-XXXYYYZZZAAABBB123`                                                 | Your `api_key` to access OpenAI API                                                   |
| `persona`       | `You are a helpful assistant who gives very short but factual answers.` | Give a personality to chatGPT                                                         |
| `model`         | `gpt-3.5-turbo`                                                         | LLM model to use, see all the options [here](https://platform.openai.com/docs/models) |
| `api_url`       | `https://llama.smartgic.io/v1`                                          | Optional and **only** required with a local AI server                                 |
| `enable_memory` | `true`                                                                  | Remember the last generated outputs                                                   |
| `memory_size`   | `15`                                                                    | How many memories to keep                                                             |
| `name`          | `Chat G.P.T.`                                                           | Name to give to the AI assistant                                                      |
| `confirmation`  | `true`                                                                  | Spoken confirmation will be triggered when a request is sent to the AI                |

The default persona is `You are a helpful voice assistant with a friendly tone and fun sense of humor. You respond in 40 words or fewer.`

## Configurations

The skill utilizes the `~/.config/mycroft/skills/skill-ovos-fallback-chatgpt.openvoiceos/settings.json` file which allows you to configure it.

### Configuration for use with OpenAI **(ChatGPT)**

```json
{
  "key": "sk-XXXYYYZZZAAABBB123",
  "model": "gpt-3.5-turbo",
  "persona": "You are a helpful voice assistant with a friendly tone and fun sense of humor. You respond in 40 words or fewer.",
  "enable_memory": true,
  "memory_size": 15,
  "__mycroft_skill_firstrun": false
}
```

### Configuration for use with Local AI

When using a local AI server instead of OpenAI, the `api_url` has to redirect to an alternative/local server compatible with OpenAI API. When using local AI, the `key` can be anything, but it has to exist. Read more about it in the OVOS technical manual, page [persona server](https://openvoiceos.github.io/ovos-technical-manual/persona_server/#compatible-projects)

Hint: If you're running an ollama server, you can use `http://localhost:11434/v1` as the api_url. 

```json
{
  "api_url": "https://llama.smartgic.io/v1",
  "key": "sk-xxx",
  "model": "llama3:latest",
  "persona": "You are a helpful voice assistant with a friendly tone and fun sense of humor. You respond in 40 words or fewer.",
  "enable_memory": true,
  "memory_size": 15,
  "name": "A.I.",
  "confirmation": false,
  "__mycroft_skill_firstrun": false
}
```

## See also

- [OVOS OpenAI Persona Plugin](https://github.com/OpenVoiceOS/ovos-solver-openai-persona-plugin) - The underlying plugin that powers this skill's integration with various AI models.
- [Ollama OpenAI Compatibility](https://ollama.com/blog/openai-compatibility).
- [Other compatible servers in the OVOS docs](https://openvoiceos.github.io/ovos-technical-manual/202-persona_server/#compatible-projects)

## Examples

- "Explain quantum computing in simple terms"
- "Got any creative ideas for a 10 year old’s birthday?"
