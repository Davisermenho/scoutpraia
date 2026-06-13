---
doc_id: DEPR_S03_OpenAI_Evals
title: "Working with OpenAI Evals (DEPRECADO)"
status: deprecated
category: REF
authority_level: 1
owner: OpenAI (external)
last_updated: "2026-06-13"
deprecation_reason: "OpenAI está desativando a plataforma Evals. Shutdown: novembro 2026. ScoutPraia não usa OpenAI Evals — usa Claude SDK. Este documento não deve ser usado para orientar implementação."
skip_for_agents: true
---

# Working with evals (DEPRECADO — NÃO USAR PARA IMPLEMENTAÇÃO)

Evaluations (often called **evals**) test model outputs to ensure they meet style and content criteria that you specify. Writing evals to understand how your LLM applications are performing against your expectations, especially when upgrading or trying new models, is an essential component to building reliable applications.

In this guide, we will focus on **configuring evals programmatically using the [Evals API](https://developers.openai.com/api/docs/api-reference/evals)**. If you prefer, you can also configure evals [in the OpenAI dashboard](https://platform.openai.com/evaluations).

> **Deprecação:** OpenAI is deprecating the Evals platform. Existing evals content remains available during the transition window. Evals will become read-only for existing users on October 31, 2026, and the platform is scheduled to shut down on November 30, 2026. See the [deprecations page](https://developers.openai.com/api/docs/deprecations#2026-06-03-evals-platform) for the current timeline.
>
> If you're new to evaluations, or want a more iterative environment to experiment in as you build your eval, consider trying [Datasets](https://developers.openai.com/api/docs/guides/evaluation-getting-started) instead.

Broadly, there are three steps to build and run evals for your LLM application.

1. Describe the task to be done as an eval
1. Run your eval with test inputs (a prompt and input data)
1. Analyze the results, then iterate and improve on your prompt

This process is somewhat similar to behavior-driven development (BDD), where you begin by specifying how the system should behave before implementing and testing the system. Let's see how we would complete each of the steps above using the [Evals API](https://developers.openai.com/api/docs/api-reference/evals).

## Create an eval for a task

Creating an eval begins by describing a task to be done by a model. Let's say that we would like to use a model to classify the contents of IT support tickets into one of three categories: `Hardware`, `Software`, or `Other`.

To implement this use case, you can use either the [Chat Completions API](https://developers.openai.com/api/docs/api-reference/chat) or the [Responses API](https://developers.openai.com/api/docs/api-reference/responses). Both examples below combine a [developer message](https://developers.openai.com/api/docs/guides/text) with a user message containing the text of a support ticket.


**Categorize IT support tickets**

```bash
curl https://api.openai.com/v1/responses \\
    -H "Authorization: Bearer $OPENAI_API_KEY" \\
    -H "Content-Type: application/json" \\
    -d '{
        "model": "gpt-5.5",
        "input": [
            {
                "role": "developer",
                "content": "Categorize the following support ticket into one of Hardware, Software, or Other."
            },
            {
                "role": "user",
                "content": "My monitor wont turn on - help!"
            }
        ]
    }'
```

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const instructions = \`
You are an expert in categorizing IT support tickets. Given the support
ticket below, categorize the request into one of "Hardware", "Software",
or "Other". Respond with only one of those words.
\`;

const ticket = "My monitor won't turn on - help!";

const response = await client.responses.create({
    model: "gpt-5.5",
    input: [
        { role: "developer", content: instructions },
        { role: "user", content: ticket },
    ],
});

console.log(response.output_text);
```

```python
from openai import OpenAI
client = OpenAI()

instructions = """
You are an expert in categorizing IT support tickets. Given the support
ticket below, categorize the request into one of "Hardware", "Software",
or "Other". Respond with only one of those words.
"""

ticket = "My monitor won't turn on - help!"

response = client.responses.create(
    model="gpt-5.5",
    input=[
        {"role": "developer", "content": instructions},
        {"role": "user", "content": ticket},
    ],
)

print(response.output_text)
```





Let's set up an eval to test this behavior [via API](https://developers.openai.com/api/docs/api-reference/evals). An eval needs two key ingredients:

- `data_source_config`: A schema for the test data you will use along with the eval.
- `testing_criteria`: The [graders](https://developers.openai.com/api/docs/guides/graders) that determine if the model output is correct.

**Create an eval**

```bash
curl https://api.openai.com/v1/evals \\
    -H "Authorization: Bearer $OPENAI_API_KEY" \\
    -H "Content-Type: application/json" \\
    -d '{
        "name": "IT Ticket Categorization",
        "data_source_config": {
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": {
                    "ticket_text": { "type": "string" },
                    "correct_label": { "type": "string" }
                },
                "required": ["ticket_text", "correct_label"]
            },
            "include_sample_schema": true
        },
        "testing_criteria": [
            {
                "type": "string_check",
                "name": "Match output to human label",
                "input": "{{ sample.output_text }}",
                "operation": "eq",
                "reference": "{{ item.correct_label }}"
            }
        ]
    }'
```

```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const evalObj = await openai.evals.create({
    name: "IT Ticket Categorization",
    data_source_config: {
        type: "custom",
        item_schema: {
            type: "object",
            properties: {
                ticket_text: { type: "string" },
                correct_label: { type: "string" }
            },
            required: ["ticket_text", "correct_label"],
        },
        include_sample_schema: true,
    },
    testing_criteria: [
        {
            type: "string_check",
            name: "Match output to human label",
            input: "{{ sample.output_text }}",
            operation: "eq",
            reference: "{{ item.correct_label }}",
        },
    ],
});

console.log(evalObj);
```

```python
from openai import OpenAI
client = OpenAI()

eval_obj = client.evals.create(
    name="IT Ticket Categorization",
    data_source_config={
        "type": "custom",
        "item_schema": {
            "type": "object",
            "properties": {
                "ticket_text": {"type": "string"},
                "correct_label": {"type": "string"},
            },
            "required": ["ticket_text", "correct_label"],
        },
        "include_sample_schema": True,
    },
    testing_criteria=[
        {
            "type": "string_check",
            "name": "Match output to human label",
            "input": "{{ sample.output_text }}",
            "operation": "eq",
            "reference": "{{ item.correct_label }}",
        }
    ],
)

print(eval_obj)
```


**Explanation: `data_source_config` parameter**

Running this eval will require a test data set that represents the type of data you expect your prompt to work with (more on creating the test data set later in this guide). In our `data_source_config` parameter, we specify that each **item** in the data set will conform to a [JSON schema](https://json-schema.org/) with two properties:

- `ticket_text`: a string of text with the contents of a support ticket
- `correct_label`: a "ground truth" output that the model should match, provided by a human

Since we will be referencing a **sample** in our test criteria (the output generated by a model given our prompt), we also set `include_sample_schema` to `true`.

```json
{
  "type": "custom",
  "item_schema": {
    "type": "object",
    "properties": {
      "ticket": { "type": "string" },
      "category": { "type": "string" }
    },
    "required": ["ticket", "category"]
  },
  "include_sample_schema": true
}
```

**Explanation: `testing_criteria` parameter**

In our `testing_criteria`, we define how we will conclude if the model output satisfies our requirements for each item in the data set. In this case, we just want the model to output one of three category strings based on the input ticket. The string it outputs should exactly match the human-labeled `correct_label` field in our test data. So in this case, we will want to use a `string_check` grader to evaluate the output.

In the test configuration, we will introduce template syntax, represented by the `{{` and `}}` brackets below. This is how we will insert dynamic content into the test for this eval.

- `{{ item.correct_label }}` refers to the ground truth value in our test data.
- `{{ sample.output_text }}` refers to the content we will generate from a model to evaluate our prompt - we'll show how to do that when we actually kick off the eval run.

```json
{
  "type": "string_check",
  "name": "Category string match",
  "input": "{{ sample.output_text }}",
  "operation": "eq",
  "reference": "{{ item.category }}"
}
```

After creating the eval, it will be assigned a UUID that you will need to address it later when kicking off a run.

```json
{
  "object": "eval",
  "id": "eval_67e321d23b54819096e6bfe140161184",
  "data_source_config": {
    "type": "custom",
    "schema": { ... omitted for brevity... }
  },
  "testing_criteria": [
    {
      "name": "Match output to human label",
      "id": "Match output to human label-c4fdf789-2fa5-407f-8a41-a6f4f9afd482",
      "type": "string_check",
      "input": "{{ sample.output_text }}",
      "reference": "{{ item.correct_label }}",
      "operation": "eq"
    }
  ],
  "name": "IT Ticket Categorization",
  "created_at": 1742938578,
  "metadata": {}
}
```

Now that we've created an eval that describes the desired behavior of our application, let's test a prompt with a set of test data.

## Test a prompt with your eval

Now that we have defined how we want our app to behave in an eval, let's construct a prompt that reliably generates the correct output for a representative sample of test data.

### Uploading test data

There are several ways to provide test data for eval runs, but it may be convenient to upload a [JSONL](https://jsonlines.org/) file that contains data in the schema we specified when we created our eval. A sample JSONL file that conforms to the schema we set up is below:

```json
{ "item": { "ticket_text": "My monitor won't turn on!", "correct_label": "Hardware" } }
{ "item": { "ticket_text": "I'm in vim and I can't quit!", "correct_label": "Software" } }
{ "item": { "ticket_text": "Best restaurants in Cleveland?", "correct_label": "Other" } }
```

This data set contains both test inputs and ground truth labels to compare model outputs against.

Next, let's upload our test data file to the OpenAI platform so we can reference it later. You can upload files [in the dashboard here](https://platform.openai.com/storage/files), but it's possible to [upload files via API](https://developers.openai.com/api/docs/api-reference/files/create) as well. The samples below assume you are running the command in a directory where you saved the sample JSON data above to a file called `tickets.jsonl`:

**Upload a test data file**

```bash
curl https://api.openai.com/v1/files \\
  -H "Authorization: Bearer $OPENAI_API_KEY" \\
  -F purpose="evals" \\
  -F file="@tickets.jsonl"
```

```javascript
import fs from "fs";
import OpenAI from "openai";

const openai = new OpenAI();

const file = await openai.files.create({
    file: fs.createReadStream("tickets.jsonl"),
    purpose: "evals",
});

console.log(file);
```

```python
from openai import OpenAI
client = OpenAI()

file = client.files.create(
    file=open("tickets.jsonl", "rb"),
    purpose="evals"
)

print(file)
```


When you upload the file, make note of the unique `id` property in the response payload (also available in the UI if you uploaded via the browser) - we will need to reference that value later:

```json
{
  "object": "file",
  "id": "file-CwHg45Fo7YXwkWRPUkLNHW",
  "purpose": "evals",
  "filename": "tickets.jsonl",
  "bytes": 208,
  "created_at": 1742834798,
  "expires_at": null,
  "status": "processed",
  "status_details": null
}
```

### Creating an eval run

With our test data in place, let's evaluate a prompt and see how it performs against our test criteria. Via API, we can do this by [creating an eval run](https://developers.openai.com/api/docs/api-reference/evals/createRun).

Make sure to replace `YOUR_EVAL_ID` and `YOUR_FILE_ID` with the unique IDs of the eval configuration and test data files you created in the steps above.


**Create an eval run**

```bash
curl https://api.openai.com/v1/evals/YOUR_EVAL_ID/runs \\
    -H "Authorization: Bearer $OPENAI_API_KEY" \\
    -H "Content-Type: application/json" \\
    -d '{
        "name": "Categorization text run",
        "data_source": {
            "type": "responses",
            "model": "gpt-4.1",
            "input_messages": {
                "type": "template",
                "template": [
                    {"role": "developer", "content": "You are an expert in categorizing IT support tickets. Given the support ticket below, categorize the request into one of Hardware, Software, or Other. Respond with only one of those words."},
                    {"role": "user", "content": "{{ item.ticket_text }}"}
                ]
            },
            "source": { "type": "file_id", "id": "YOUR_FILE_ID" }
        }
    }'
```

```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const run = await openai.evals.runs.create("YOUR_EVAL_ID", {
    name: "Categorization text run",
    data_source: {
        type: "responses",
        model: "gpt-4.1",
        input_messages: {
            type: "template",
            template: [
                { role: "developer", content: "You are an expert in categorizing IT support tickets. Given the support ticket below, categorize the request into one of 'Hardware', 'Software', or 'Other'. Respond with only one of those words." },
                { role: "user", content: "{{ item.ticket_text }}" },
            ],
        },
        source: { type: "file_id", id: "YOUR_FILE_ID" },
    },
});

console.log(run);
```

```python
from openai import OpenAI
client = OpenAI()

run = client.evals.runs.create(
    "YOUR_EVAL_ID",
    name="Categorization text run",
    data_source={
        "type": "responses",
        "model": "gpt-4.1",
        "input_messages": {
            "type": "template",
            "template": [
                {"role": "developer", "content": "You are an expert in categorizing IT support tickets. Given the support ticket below, categorize the request into one of 'Hardware', 'Software', or 'Other'. Respond with only one of those words."},
                {"role": "user", "content": "{{ item.ticket_text }}"},
            ],
        },
        "source": {"type": "file_id", "id": "YOUR_FILE_ID"},
    },
)

print(run)
```





When we create the run, we set up a prompt using either a [Chat Completions](https://developers.openai.com/api/docs/guides/text?api-mode=chat) messages array or a [Responses](https://developers.openai.com/api/docs/api-reference/responses) input. This prompt is used to generate a model response for every line of test data in your data set. We can use the double curly brace syntax to template in the dynamic variable `item.ticket_text`, which is drawn from the current test data item.

If the eval run is successfully created, you'll receive an API response that looks like this:


```json
{
    "object": "eval.run",
    "id": "evalrun_67e44c73eb6481909f79a457749222c7",
    "eval_id": "eval_67e44c5becec81909704be0318146157",
    "report_url": "https://platform.openai.com/evaluation/evals/abc123",
    "status": "queued",
    "model": "gpt-4.1",
    "name": "Categorization text run",
    "created_at": 1743015028,
    "result_counts": { ... },
    "per_model_usage": null,
    "per_testing_criteria_results": null,
    "data_source": {
        "type": "responses",
        "source": {
            "type": "file_id",
            "id": "file-J7MoX9ToHXp2TutMEeYnwj"
        },
        "input_messages": {
            "type": "template",
            "template": [
                {
                    "type": "message",
                    "role": "developer",
                    "content": {
                        "type": "input_text",
                        "text": "You are an expert in...."
                    }
                },
                {
                    "type": "message",
                    "role": "user",
                    "content": {
                        "type": "input_text",
                        "text": "{{item.ticket_text}}"
                    }
                }
            ]
        },
        "model": "gpt-4.1",
        "sampling_params": null
    },
    "error": null,
    "metadata": {}
}
```




Your eval run has now been queued, and it will execute asynchronously as it processes every row in your data set, generating responses for testing with the prompt and model we specified.

## Analyze the results

To receive updates when a run succeeds, fails, or is canceled, create a webhook endpoint and subscribe to the `eval.run.succeeded`, `eval.run.failed`, and `eval.run.canceled` events. See the [webhooks guide](https://developers.openai.com/api/docs/guides/webhooks) for more details.

Depending on the size of your dataset, the eval run may take some time to complete. You can view current status in the dashboard, but you can also [fetch the current status of an eval run via API](https://developers.openai.com/api/docs/api-reference/evals/getRun):

**Retrieve eval run status**

```bash
curl https://api.openai.com/v1/evals/YOUR_EVAL_ID/runs/YOUR_RUN_ID \\
    -H "Authorization: Bearer $OPENAI_API_KEY" \\
    -H "Content-Type: application/json"
```

```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const run = await openai.evals.runs.retrieve("YOUR_RUN_ID", {
    eval_id: "YOUR_EVAL_ID",
});
console.log(run);
```

```python
from openai import OpenAI
client = OpenAI()

run = client.evals.runs.retrieve("YOUR_EVAL_ID", "YOUR_RUN_ID")
print(run)
```


You'll need the UUID of both your eval and eval run to fetch its status. When you do, you'll see eval run data that looks like this:


```json
{
    "object": "eval.run",
    "id": "evalrun_67e44c73eb6481909f79a457749222c7",
    "eval_id": "eval_67e44c5becec81909704be0318146157",
    "report_url": "https://platform.openai.com/evaluation/evals/xxx",
    "status": "completed",
    "model": "gpt-4.1",
    "name": "Categorization text run",
    "created_at": 1743015028,
    "result_counts": {
        "total": 3,
        "errored": 0,
        "failed": 0,
        "passed": 3
    },
    "per_model_usage": [
        {
            "model_name": "gpt-4o-2024-08-06",
            "invocation_count": 3,
            "prompt_tokens": 166,
            "completion_tokens": 6,
            "total_tokens": 172,
            "cached_tokens": 0
        }
    ],
    "per_testing_criteria_results": [
        {
            "testing_criteria": "Match output to human label-40d67441-5000-4754-ab8c-181c125803ce",
            "passed": 3,
            "failed": 0
        }
    ],
    "data_source": {
        "type": "responses",
        "source": {
            "type": "file_id",
            "id": "file-J7MoX9ToHXp2TutMEeYnwj"
        },
        "input_messages": {
            "type": "template",
            "template": [
                {
                    "type": "message",
                    "role": "developer",
                    "content": {
                        "type": "input_text",
                        "text": "You are an expert in categorizing IT support tickets. Given the support ticket below, categorize the request into one of Hardware, Software, or Other. Respond with only one of those words."
                    }
                },
                {
                    "type": "message",
                    "role": "user",
                    "content": {
                        "type": "input_text",
                        "text": "{{item.ticket_text}}"
                    }
                }
            ]
        },
        "model": "gpt-4.1",
        "sampling_params": null
    },
    "error": null,
    "metadata": {}
}
```




The API response contains granular information about test criteria results, API usage for generating model responses, and a `report_url` property that takes you to a page in the dashboard where you can explore the results visually.

In our simple test, the model reliably generated the content we wanted for a small test case sample. In reality, you will often have to run your eval with more criteria, different prompts, and different data sets. But the process above gives you all the tools you need to build robust evals for your LLM apps!

## Next steps

Now you know how to create and run evals via API, and using the dashboard! Here are a few other resources that may be useful to you as you continue to improve your model results.

- [Keep tabs on the performance of your prompts as you iterate on them.](https://cookbook.openai.com/examples/evaluation/use-cases/regression)
- [Compare the results of many different prompts and models at once.](https://cookbook.openai.com/examples/evaluation/use-cases/bulk-experimentation)
- [Examine stored completions to test for prompt regressions.](https://cookbook.openai.com/examples/evaluation/use-cases/completion-monitoring)
- [Improve a model's ability to generate responses tailored to your use case.](https://developers.openai.com/api/docs/guides/fine-tuning)
- [Learn how to distill large model results to smaller, cheaper, and faster models.](https://developers.openai.com/api/docs/guides/distillation)

# Evaluations Example: Push Notifications Summarizer Prompt Regression,

Evals are **task oriented** and iterative, they're the best way to check how your LLM integration is doing and improve it.

In the following eval, we are going to focus on the task of **detecting if my prompt change is a regression**.

Our use-case is:
1. I have an llm integration that takes a list of push notifications and summarizes them into a single condensed statement.
2. I want to detect if a prompt change regresses the behavior

## Evals structure

Evals have two parts, the "Eval" and the "Run". An "Eval" holds the configuration for your testing criteria and the structure of the data for your "Runs". An Eval can have many runs that are evaluated by your testing criteria.

```python
import openai
from openai.types.chat import ChatCompletion
import pydantic
import os

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "your-api-key")
```

## Use-case

We're testing the following integration, a push notifications summary, which takes in multiple push notifications and collapses them into a single one, this is a chat completions call.

```python
class PushNotifications(pydantic.BaseModel):
    notifications: str

print(PushNotifications.model_json_schema())
```

```python
DEVELOPER_PROMPT = """
You are a helpful assistant that summarizes push notifications.
You are given a list of push notifications and you need to collapse them into a single one.
Output only the final summary, nothing else.
"""

def summarize_push_notification(push_notifications: str) -> ChatCompletion:
    result = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": DEVELOPER_PROMPT},
            {"role": "user", "content": push_notifications},
        ],
    )
    return result

example_push_notifications_list = PushNotifications(notifications="""
- Alert: Unauthorized login attempt detected.
- New comment on your blog post: "Great insights!"
- Tonight's dinner recipe: Pasta Primavera.
""")
result = summarize_push_notification(example_push_notifications_list.notifications)
print(result.choices[0].message.content)
```

# Setting up your eval

An Eval holds the configuration that is shared across multiple *Runs*, it has two components:
1. Data source configuration `data_source_config` - the schema (columns) that your future *Runs* conform to.
    - The `data_source_config` uses JSON Schema to define what variables are available in the Eval.
2. Testing Criteria `testing_criteria` - How you'll determine if your integration is working for each *row* of your data source.

For this use-case, we want to test if the push notification summary completion is good, so we'll set-up our eval with this in mind.

```python
# We want our input data to be available in our variables, so we set the item_schema to
# PushNotifications.model_json_schema()
data_source_config = {
    "type": "custom",
    "item_schema": PushNotifications.model_json_schema(),
    # We're going to be uploading completions from the API, so we tell the Eval to expect this
    "include_sample_schema": True,
}
```

This data_source_config defines what variables are available throughout the eval.

This item schema:
```json
{
  "properties": {
    "notifications": {
      "title": "Notifications",
      "type": "string"
    }
  },
  "required": ["notifications"],
  "title": "PushNotifications",
  "type": "object"
}
```
Means that we'll have the variable `{{item.notifications}}` available in our eval.

`"include_sample_schema": True`
Mean's that we'll have the variable `{{sample.output_text}}` available in our eval.

**Now, we'll use those variables to set up our test criteria.**

```python
GRADER_DEVELOPER_PROMPT = """
Label the following push notification summary as either correct or incorrect.
The push notification and the summary will be provided below.
A good push notificiation summary is concise and snappy.
If it is good, then label it as correct, if not, then incorrect.
"""
GRADER_TEMPLATE_PROMPT = """
Push notifications: {{item.notifications}}
Summary: {{sample.output_text}}
"""
push_notification_grader = {
    "name": "Push Notification Summary Grader",
    "type": "label_model",
    "model": "o3-mini",
    "input": [
        {
            "role": "developer",
            "content": GRADER_DEVELOPER_PROMPT,
        },
        {
            "role": "user",
            "content": GRADER_TEMPLATE_PROMPT,
        },
    ],
    "passing_labels": ["correct"],
    "labels": ["correct", "incorrect"],
}
```

The `push_notification_grader` is a model grader (llm-as-a-judge), which looks at the input `{{item.notifications}}` and the generated summary `{{sample.output_text}}` and labels it as "correct" or "incorrect".
We then instruct via. the "passing_labels", what constitutes a passing answer.

Note: under the hood, this uses structured outputs so that labels are always valid.

**Now we'll create our eval!, and start adding data to it**

```python
eval_create_result = openai.evals.create(
    name="Push Notification Summary Workflow",
    metadata={
        "description": "This eval checks if the push notification summary is correct.",
    },
    data_source_config=data_source_config,
    testing_criteria=[push_notification_grader],
)

eval_id = eval_create_result.id
```

# Creating runs

Now that we have our eval set-up with our test_criteria, we can start to add a bunch of runs!
We'll start with some push notification data.

```python
push_notification_data = [
        """
- New message from Sarah: "Can you call me later?"
- Your package has been delivered!
- Flash sale: 20% off electronics for the next 2 hours!
""",
        """
- Weather alert: Thunderstorm expected in your area.
- Reminder: Doctor's appointment at 3 PM.
- John liked your photo on Instagram.
""",
        """
- Breaking News: Local elections results are in.
- Your daily workout summary is ready.
- Check out your weekly screen time report.
""",
        """
- Your ride is arriving in 2 minutes.
- Grocery order has been shipped.
- Don't miss the season finale of your favorite show tonight!
""",
        """
- Event reminder: Concert starts at 7 PM.
- Your favorite team just scored!
- Flashback: Memories from 3 years ago.
""",
        """
- Low battery alert: Charge your device.
- Your friend Mike is nearby.
- New episode of "The Tech Hour" podcast is live!
""",
        """
- System update available.
- Monthly billing statement is ready.
- Your next meeting starts in 15 minutes.
""",
        """
- Alert: Unauthorized login attempt detected.
- New comment on your blog post: "Great insights!"
- Tonight's dinner recipe: Pasta Primavera.
""",
        """
- Special offer: Free coffee with any breakfast order.
- Your flight has been delayed by 30 minutes.
- New movie release: "Adventures Beyond" now streaming.
""",
        """
- Traffic alert: Accident reported on Main Street.
- Package out for delivery: Expected by 5 PM.
- New friend suggestion: Connect with Emma.
"""]
```

Our first run will be our default grader from the completions function above `summarize_push_notification`
We'll loop through our dataset, make completions calls, and then submit them as a run to be graded.

```python
run_data = []
for push_notifications in push_notification_data:
    result = summarize_push_notification(push_notifications)
    run_data.append({
        "item": PushNotifications(notifications=push_notifications).model_dump(),
        "sample": result.model_dump()
    })

eval_run_result = openai.evals.runs.create(
    eval_id=eval_id,
    name="baseline-run",
    data_source={
        "type": "jsonl",
        "source": {
            "type": "file_content",
            "content": run_data,
        }
    },
)
print(eval_run_result)
# Check out the results in the UI
print(eval_run_result.report_url)
```

Now let's simulate a regression, here's our original prompt, let's simulate a developer breaking the prompt.

```python
DEVELOPER_PROMPT = """
You are a helpful assistant that summarizes push notifications.
You are given a list of push notifications and you need to collapse them into a single one.
Output only the final summary, nothing else.
"""
```

```python
DEVELOPER_PROMPT = """
You are a helpful assistant that summarizes push notifications.
You are given a list of push notifications and you need to collapse them into a single one.
You should make the summary longer than it needs to be and include more information than is necessary.
"""

def summarize_push_notification_bad(push_notifications: str) -> ChatCompletion:
    result = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": DEVELOPER_PROMPT},
            {"role": "user", "content": push_notifications},
        ],
    )
    return result
```

```python
run_data = []
for push_notifications in push_notification_data:
    result = summarize_push_notification_bad(push_notifications)
    run_data.append({
        "item": PushNotifications(notifications=push_notifications).model_dump(),
        "sample": result.model_dump()
    })

eval_run_result = openai.evals.runs.create(
    eval_id=eval_id,
    name="regression-run",
    data_source={
        "type": "jsonl",
        "source": {
            "type": "file_content",
            "content": run_data,
        }
    },
)
print(eval_run_result.report_url)
```

If you view that report, you'll see that it has a score that's much lower than the baseline-run.

## Congratulations, you just prevented a bug from shipping to users

Quick note:
Evals doesn't yet support the `responses` api natively, however, you can transform it to the `completions` format with the following code.

```python
def summarize_push_notification_responses(push_notifications: str):
    result = openai.responses.create(
                model="gpt-4o",
                input=[
                    {"role": "developer", "content": DEVELOPER_PROMPT},
                    {"role": "user", "content": push_notifications},
                ],
            )
    return result
def transform_response_to_completion(response):
    completion = {
        "model": response.model,
        "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": response.output_text
        },
        "finish_reason": "stop",
    }]
    }
    return completion

run_data = []
for push_notifications in push_notification_data:
    response = summarize_push_notification_responses(push_notifications)
    completion = transform_response_to_completion(response)
    run_data.append({
        "item": PushNotifications(notifications=push_notifications).model_dump(),
        "sample": completion
    })

report_response = openai.evals.runs.create(
    eval_id=eval_id,
    name="responses-run",
    data_source={
        "type": "jsonl",
        "source": {
            "type": "file_content",
            "content": run_data,
        }
    },
)
print(report_response.report_url)
```

# Evaluations Example: Push Notifications Bulk Experimentation 

Evals are **task oriented** and iterative, they're the best way to check how your LLM integration is doing and improve it.

In the following eval, we are going to focus on the task of **testing many variants of models and prompts**.

Our use-case is:
1. I want to get the best possible performance out of my push notifications summarizer

## Evals structure

Evals have two parts, the "Eval" and the "Run". An "Eval" holds the configuration for your testing criteria and the structure of the data for your "Runs". An Eval `has_many` runs, that are evaluated by your testing criteria.

```python
import pydantic
import openai
from openai.types.chat import ChatCompletion
import os

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "your-api-key")
```

## Use-case

We're testing the following integration, a push notifications summarizer, which takes in multiple push notifications and collapses them into a single message.

```python
class PushNotifications(pydantic.BaseModel):
    notifications: str

print(PushNotifications.model_json_schema())
```

```python
DEVELOPER_PROMPT = """
You are a helpful assistant that summarizes push notifications.
You are given a list of push notifications and you need to collapse them into a single one.
Output only the final summary, nothing else.
"""

def summarize_push_notification(push_notifications: str) -> ChatCompletion:
    result = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": DEVELOPER_PROMPT},
            {"role": "user", "content": push_notifications},
        ],
    )
    return result

example_push_notifications_list = PushNotifications(notifications="""
- Alert: Unauthorized login attempt detected.
- New comment on your blog post: "Great insights!"
- Tonight's dinner recipe: Pasta Primavera.
""")
result = summarize_push_notification(example_push_notifications_list.notifications)
print(result.choices[0].message.content)
```

# Setting up your eval

An Eval holds the configuration that is shared across multiple *Runs*, it has two components:
1. Data source configuration `data_source_config` - the schema (columns) that your future *Runs* conform to.
    - The `data_source_config` uses JSON Schema to define what variables are available in the Eval.
2. Testing Criteria `testing_criteria` - How you'll determine if your integration is working for each *row* of your data source.

For this use-case, we want to test if the push notification summary completion is good, so we'll set-up our eval with this in mind.

```python
# We want our input data to be available in our variables, so we set the item_schema to
# PushNotifications.model_json_schema()
data_source_config = {
    "type": "custom",
    "item_schema": PushNotifications.model_json_schema(),
    # We're going to be uploading completions from the API, so we tell the Eval to expect this
    "include_sample_schema": True,
}
```

This data_source_config defines what variables are available throughout the eval.

This item schema:
```json
{
  "properties": {
    "notifications": {
      "title": "Notifications",
      "type": "string"
    }
  },
  "required": ["notifications"],
  "title": "PushNotifications",
  "type": "object"
}
```
Means that we'll have the variable `{{item.notifications}}` available in our eval.

`"include_sample_schema": True`
Mean's that we'll have the variable `{{sample.output_text}}` available in our eval.

**Now, we'll use those variables to set up our test criteria.**

```python
GRADER_DEVELOPER_PROMPT = """
Categorize the following push notification summary into the following categories:
1. concise-and-snappy
2. drops-important-information
3. verbose
4. unclear
5. obscures-meaning
6. other 

You'll be given the original list of push notifications and the summary like this:

<push_notifications>
...notificationlist...
</push_notifications>
<summary>
...summary...
</summary>

You should only pick one of the categories above, pick the one which most closely matches and why.
"""
GRADER_TEMPLATE_PROMPT = """
<push_notifications>{{item.notifications}}</push_notifications>
<summary>{{sample.output_text}}</summary>
"""
push_notification_grader = {
    "name": "Push Notification Summary Grader",
    "type": "label_model",
    "model": "o3-mini",
    "input": [
        {
            "role": "developer",
            "content": GRADER_DEVELOPER_PROMPT,
        },
        {
            "role": "user",
            "content": GRADER_TEMPLATE_PROMPT,
        },
    ],
    "passing_labels": ["concise-and-snappy"],
    "labels": [
        "concise-and-snappy",
        "drops-important-information",
        "verbose",
        "unclear",
        "obscures-meaning",
        "other",
    ],
}
```

The `push_notification_grader` is a model grader (llm-as-a-judge) which looks at the input `{{item.notifications}}` and the generated summary `{{sample.output_text}}` and labels it as "correct" or "incorrect"
We then instruct via the "passing_labels" what constitutes a passing answer.

Note: under the hood, this uses structured outputs so that labels are always valid.

**Now we'll create our eval, and start adding data to it!**

```python
eval_create_result = openai.evals.create(
    name="Push Notification Bulk Experimentation Eval",
    metadata={
        "description": "This eval tests many prompts and models to find the best performing combination.",
    },
    data_source_config=data_source_config,
    testing_criteria=[push_notification_grader],
)
eval_id = eval_create_result.id
```

# Creating runs

Now that we have our eval set-up with our testing_criteria, we can start to add a bunch of runs!
We'll start with some push notification data.

```python
push_notification_data = [
        """
- New message from Sarah: "Can you call me later?"
- Your package has been delivered!
- Flash sale: 20% off electronics for the next 2 hours!
""",
        """
- Weather alert: Thunderstorm expected in your area.
- Reminder: Doctor's appointment at 3 PM.
- John liked your photo on Instagram.
""",
        """
- Breaking News: Local elections results are in.
- Your daily workout summary is ready.
- Check out your weekly screen time report.
""",
        """
- Your ride is arriving in 2 minutes.
- Grocery order has been shipped.
- Don't miss the season finale of your favorite show tonight!
""",
        """
- Event reminder: Concert starts at 7 PM.
- Your favorite team just scored!
- Flashback: Memories from 3 years ago.
""",
        """
- Low battery alert: Charge your device.
- Your friend Mike is nearby.
- New episode of "The Tech Hour" podcast is live!
""",
        """
- System update available.
- Monthly billing statement is ready.
- Your next meeting starts in 15 minutes.
""",
        """
- Alert: Unauthorized login attempt detected.
- New comment on your blog post: "Great insights!"
- Tonight's dinner recipe: Pasta Primavera.
""",
        """
- Special offer: Free coffee with any breakfast order.
- Your flight has been delayed by 30 minutes.
- New movie release: "Adventures Beyond" now streaming.
""",
        """
- Traffic alert: Accident reported on Main Street.
- Package out for delivery: Expected by 5 PM.
- New friend suggestion: Connect with Emma.
"""]
```

Now we're going to set up a bunch of prompts to test.

We want to test a basic prompt, with a couple of variations:
1. In one variation, we'll just have the basic prompt
2. In the next one, we'll include some positive examples of what we want the summaries to look like
3. In the final one, we'll include both positive and negative examples.

We'll also include a list of models to use.

```python
PROMPT_PREFIX = """
You are a helpful assistant that takes in an array of push notifications and returns a collapsed summary of them.
The push notification will be provided as follows:
<push_notifications>
...notificationlist...
</push_notifications>

You should return just the summary and nothing else.
"""

PROMPT_VARIATION_BASIC = f"""
{PROMPT_PREFIX}

You should return a summary that is concise and snappy.
"""

PROMPT_VARIATION_WITH_EXAMPLES = f"""
{PROMPT_VARIATION_BASIC}

Here is an example of a good summary:
<push_notifications>
- Traffic alert: Accident reported on Main Street.- Package out for delivery: Expected by 5 PM.- New friend suggestion: Connect with Emma.
</push_notifications>
<summary>
Traffic alert, package expected by 5pm, suggestion for new friend (Emily).
</summary>
"""

PROMPT_VARIATION_WITH_NEGATIVE_EXAMPLES = f"""
{PROMPT_VARIATION_WITH_EXAMPLES}

Here is an example of a bad summary:
<push_notifications>
- Traffic alert: Accident reported on Main Street.- Package out for delivery: Expected by 5 PM.- New friend suggestion: Connect with Emma.
</push_notifications>
<summary>
Traffic alert reported on main street. You have a package that will arrive by 5pm, Emily is a new friend suggested for you.
</summary>
"""

prompts = [
    ("basic", PROMPT_VARIATION_BASIC),
    ("with_examples", PROMPT_VARIATION_WITH_EXAMPLES),
    ("with_negative_examples", PROMPT_VARIATION_WITH_NEGATIVE_EXAMPLES),
]

models = ["gpt-4o", "gpt-4o-mini", "o3-mini"]
```

**Now we can just loop through all prompts and all models to test a bunch of configurations at once!**

We'll use the 'completion' run data source with template variables for our push notification list.

OpenAI will handle making the completions calls for you and populating "sample.output_text"

```python
for prompt_name, prompt in prompts:
    for model in models:
        run_data_source = {
            "type": "completions",
            "input_messages": {
                "type": "template",
                "template": [
                    {
                        "role": "developer",
                        "content": prompt,
                    },
                    {
                        "role": "user",
                        "content": "<push_notifications>{{item.notifications}}</push_notifications>",
                    },
                ],
            },
            "model": model,
            "source": {
                "type": "file_content",
                "content": [
                    {
                        "item": PushNotifications(notifications=notification).model_dump()
                    }
                    for notification in push_notification_data
                ],
            },
        }

        run_create_result = openai.evals.runs.create(
            eval_id=eval_id,
            name=f"bulk_{prompt_name}_{model}",
            data_source=run_data_source,
        )
        print(f"Report URL {model}, {prompt_name}:", run_create_result.report_url)
```



## Congratulations, you just tested 9 different prompt and model variations across your dataset!

# Evaluations Example: Push Notifications Summarizer Monitoring

Evals are **task-oriented** and iterative, they're the best way to check how your LLM integration is doing and improve it.

In the following eval, we are going to focus on the task of **detecting our prompt changes for regressions**.

Our use-case is:
1. We have been logging chat completion requests by setting `store=True` in our production chat completions requests. Note that you can also enable "on by default" logging in your admin panel (https://platform.openai.com/settings/organization/data-controls/data-retention).
2. We want to see whether our prompt changes have introduced regressions.

## Evals structure

Evals have two parts, the "Eval" and the "Run". An "Eval" holds the configuration for your testing criteria and the structure of the data for your "Runs". An Eval can have many Runs, which are each evaluated using your testing criteria.

```python
from openai import AsyncOpenAI
import os
import asyncio

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "your-api-key")
client = AsyncOpenAI()
```

## Use-case

We're testing the following integration, a push notifications summary, which takes in multiple push notifications and collapses them into a single one, this is a chat completions call.

# Generate our test data

I'm going to produce simulated production chat completions requests with two different prompt versions to test how each performs. The first is a "good" prompt, the second is a "bad" prompt. These will have different metadata which we'll use later.

```python
push_notification_data = [
        """
- New message from Sarah: "Can you call me later?"
- Your package has been delivered!
- Flash sale: 20% off electronics for the next 2 hours!
""",
        """
- Weather alert: Thunderstorm expected in your area.
- Reminder: Doctor's appointment at 3 PM.
- John liked your photo on Instagram.
""",
        """
- Breaking News: Local elections results are in.
- Your daily workout summary is ready.
- Check out your weekly screen time report.
""",
        """
- Your ride is arriving in 2 minutes.
- Grocery order has been shipped.
- Don't miss the season finale of your favorite show tonight!
""",
        """
- Event reminder: Concert starts at 7 PM.
- Your favorite team just scored!
- Flashback: Memories from 3 years ago.
""",
        """
- Low battery alert: Charge your device.
- Your friend Mike is nearby.
- New episode of "The Tech Hour" podcast is live!
""",
        """
- System update available.
- Monthly billing statement is ready.
- Your next meeting starts in 15 minutes.
""",
        """
- Alert: Unauthorized login attempt detected.
- New comment on your blog post: "Great insights!"
- Tonight's dinner recipe: Pasta Primavera.
""",
        """
- Special offer: Free coffee with any breakfast order.
- Your flight has been delayed by 30 minutes.
- New movie release: "Adventures Beyond" now streaming.
""",
        """
- Traffic alert: Accident reported on Main Street.
- Package out for delivery: Expected by 5 PM.
- New friend suggestion: Connect with Emma.
"""]
```

```python
PROMPTS = [
    (
        """
        You are a helpful assistant that summarizes push notifications.
        You are given a list of push notifications and you need to collapse them into a single one.
        Output only the final summary, nothing else.
        """,
        "v1"
    ),
    (
        """
        You are a helpful assistant that summarizes push notifications.
        You are given a list of push notifications and you need to collapse them into a single one.
        The summary should be longer than it needs to be and include more information than is necessary.
        Output only the final summary, nothing else.
        """,
        "v2"
    )
]

tasks = []
for notifications in push_notification_data:
    for (prompt, version) in PROMPTS:
        tasks.append(client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer", "content": prompt},
                {"role": "user", "content": notifications},
            ],
            store=True,
            metadata={"prompt_version": version, "usecase": "push_notifications_summarizer"},
        ))
await asyncio.gather(*tasks)
```

You can view the completions you just created at https://platform.openai.com/logs. 

**Make sure that the chat completions show up, as they are necessary for the next step.**

```python
completions = await client.chat.completions.list()
assert completions.data, "No completions found. You may need to enable logs in your admin panel."
completions.data[0]
```

# Setting up your eval

An Eval holds the configuration that is shared across multiple *Runs*, it has two components:
1. Data source configuration `data_source_config` - the schema (columns) that your future *Runs* conform to.
    - The `data_source_config` uses JSON Schema to define what variables are available in the Eval.
2. Testing Criteria `testing_criteria` - How you'll determine if your integration is working for each *row* of your data source.

For this use-case, we're using stored-completions, so we'll set up that data_source_config

**Important**
You are likely to have many different stored completions use-cases, metadata is the best way to keep track of this for evals to keep them focused and task oriented.

```python
# We want our input data to be available in our variables, so we set the item_schema to
# PushNotifications.model_json_schema()
data_source_config = {
    "type": "stored_completions",
    "metadata": {
        "usecase": "push_notifications_summarizer"
    }
}
```

This data_source_config defines what variables are available throughout the eval.

The stored completions config provides two variables for you to use throughout your eval:
1. {{item.input}} - the messages sent to the completions call
2. {{sample.output_text}} - the text response from the assistant

**Now, we'll use those variables to set up our test criteria.**

```python
GRADER_DEVELOPER_PROMPT = """
Label the following push notification summary as either correct or incorrect.
The push notification and the summary will be provided below.
A good push notificiation summary is concise and snappy.
If it is good, then label it as correct, if not, then incorrect.
"""
GRADER_TEMPLATE_PROMPT = """
Push notifications: {{item.input}}
Summary: {{sample.output_text}}
"""
push_notification_grader = {
    "name": "Push Notification Summary Grader",
    "type": "label_model",
    "model": "o3-mini",
    "input": [
        {
            "role": "developer",
            "content": GRADER_DEVELOPER_PROMPT,
        },
        {
            "role": "user",
            "content": GRADER_TEMPLATE_PROMPT,
        },
    ],
    "passing_labels": ["correct"],
    "labels": ["correct", "incorrect"],
}
```

The `push_notification_grader` is a model grader (llm-as-a-judge), which looks at the input `{{item.input}}` and the generated summary `{{sample.output_text}}` and labels it as "correct" or "incorrect".

Note: under the hood, this uses structured outputs so that labels are always valid.

**Now we'll create our eval!, and start adding data to it**

```python
eval_create_result = await client.evals.create(
    name="Push Notification Completion Monitoring",
    metadata={"description": "This eval monitors completions"},
    data_source_config=data_source_config,
    testing_criteria=[push_notification_grader],
)

eval_id = eval_create_result.id
```

# Creating runs

Now that we have our eval set-up with our test_criteria, we can start adding runs.
I want to compare the performance between my two **prompt versions**

To do this, we just define our source as "stored_completions" with a metadata filter for each of our prompt versions.

```python
# Grade prompt_version=v1
eval_run_result = await client.evals.runs.create(
    eval_id=eval_id,
    name="v1-run",
    data_source={
        "type": "completions",
        "source": {
            "type": "stored_completions",
            "metadata": {
                "prompt_version": "v1",
            }
        }
    }
)
print(eval_run_result.report_url)
```

```python
# Grade prompt_version=v2
eval_run_result_v2 = await client.evals.runs.create(
    eval_id=eval_id,
    name="v2-run",
    data_source={
        "type": "completions",
        "source": {
            "type": "stored_completions",
            "metadata": {
                "prompt_version": "v2",
            }
        }
    }
)
print(eval_run_result_v2.report_url)
```

Just for to be thorough, let's see how this prompt would do with 4o, instead of 4o-mini, with both prompt versions as the starting point.

All we have to do is reference the input messages ({{item.input}}) and set the model to 4o. Since we don't already have any stored completions for 4o, this eval run will generate new completions.

```python
tasks = []
for prompt_version in ["v1", "v2"]:
    tasks.append(client.evals.runs.create(
        eval_id=eval_id,
        name=f"post-fix-new-model-run-{prompt_version}",
        data_source={
            "type": "completions",
            "input_messages": {
                "type": "item_reference",
                "item_reference": "item.input",
            },
            "model": "gpt-4o",
            "source": {
                "type": "stored_completions",
                "metadata": {
                    "prompt_version": prompt_version,
                }
            }
        },
    ))
result = await asyncio.gather(*tasks)
for run in result:
    print(run.report_url)
```

If you view that report, you'll see that we can see that prompt_version=v2 has a regression!

## Congratulations, you just discovered a bug, you could revert it, or make another prompt change, etc.!

# Model optimization




LLM output is non-deterministic, and model behavior changes between model snapshots and families. Developers must constantly measure and tune the performance of LLM applications to ensure they're getting the best results. In this guide, we explore the techniques and OpenAI platform tools you can use to ensure high quality outputs from the model.

> **Nota:** This guide covers evals and fine-tuning workflows that are being moved into legacy documentation. See the [deprecations page](https://developers.openai.com/api/docs/deprecations) for the current timelines for the affected platform surfaces.

## Model optimization workflow

Optimizing model output requires a combination of **evals**, **prompt engineering**, and **fine-tuning**, creating a flywheel of feedback that leads to better prompts and better training data for fine-tuning. The optimization process usually goes something like this.

1. Write [evals](https://developers.openai.com/api/docs/guides/evals) that measure model output, establishing a baseline for performance and accuracy.
1. [Prompt the model](https://developers.openai.com/api/docs/guides/text) for output, providing relevant context data and instructions.
1. For some use cases, it may be desirable to [fine-tune](#fine-tune-a-model) a model for a specific task.
1. Run evals using test data that is representative of real world inputs. Measure the performance of your prompt and fine-tuned model.
1. Tweak your prompt or fine-tuning dataset based on eval feedback.
1. Repeat the loop continuously to improve your model results.

Here's an overview of the major steps, and how to do them using the OpenAI platform.

## Build evals

In the OpenAI platform, you can [build and run evals](https://developers.openai.com/api/docs/guides/evals) either via API or in the [dashboard](https://platform.openai.com/evaluations). You might even consider writing evals _before_ you start writing prompts, taking an approach akin to behavior-driven development (BDD).

Run your evals against test inputs like you expect to see in production. Using one of several available [graders](https://developers.openai.com/api/docs/guides/graders), measure the results of a prompt against your test data set.

[Run tests on your model outputs to ensure you're getting the right results.](https://developers.openai.com/api/docs/guides/evals)

## Write effective prompts

With evals in place, you can effectively iterate on [prompts](https://developers.openai.com/api/docs/guides/text). The prompt engineering process may be all you need in order to get great results for your use case. Different models may require different prompting techniques, but there are several best practices you can apply across the board to get better results.

- **Include relevant context** - in your instructions, include text or image content that the model will need to generate a response from outside its training data. This could include data from private databases or current, up-to-the-minute information.
- **Provide clear instructions** - your prompt should contain clear goals about what kind of output you want. Start with [`gpt-5.5`](https://developers.openai.com/api/docs/models/gpt-5.5) for new work, and use [reasoning model guidance](https://developers.openai.com/api/docs/guides/reasoning) to tune outcome-level instructions, reasoning effort, and verbosity.
- **Provide example outputs** - give the model a few examples of correct output for a given prompt (a process called few-shot learning). The model can extrapolate from these examples how it should respond for other prompts.

[Learn the basics of writing good prompts for the model.](https://developers.openai.com/api/docs/guides/text)

## Fine-tune a model

> **Deprecação:** OpenAI is winding down the fine-tuning platform. The platform is no longer accessible to new users, but existing users of the fine-tuning platform will be able to create training jobs for the coming months. All fine-tuned models will remain available for inference until their base models are [deprecated](https://developers.openai.com/api/docs/deprecations). The full timeline is [here](https://developers.openai.com/api/docs/deprecations).

OpenAI models are already pre-trained to perform across a broad range of subjects and tasks. Fine-tuning lets you take an OpenAI base model, provide the kinds of inputs and outputs you expect in your application, and get a model that excels in the tasks you'll use it for.

Fine-tuning can be a time-consuming process, but it can also enable a model to consistently format responses in a certain way or handle novel inputs. You can use fine-tuning with [prompt engineering](https://developers.openai.com/api/docs/guides/text) to realize a few more benefits over prompting alone:

- You can provide more example inputs and outputs than could fit within the context window of a single request, enabling the model handle a wider variety of prompts.
- You can use shorter prompts with fewer examples and context data, which saves on token costs at scale and can be lower latency.
- You can train on proprietary or sensitive data without having to include it via examples in every request.
- You can train a smaller, cheaper, faster model to excel at a particular task where a larger model is not cost-effective.

Visit our [pricing page](https://openai.com/api/pricing) to learn more about how fine-tuned model training and usage are billed.

### Fine-tuning methods

These are the fine-tuning methods supported in the OpenAI platform today.

### How fine-tuning works

In the OpenAI platform, you can create fine-tuned models either in the [dashboard](https://platform.openai.com/finetune) or [with the API](https://developers.openai.com/api/docs/api-reference/fine-tuning). This is the general shape of the fine-tuning process:

1. Collect a dataset of examples to use as training data
1. Upload that dataset to OpenAI, formatted in JSONL
1. Create a fine-tuning job using one of the methods above, depending on your goals—this begins the fine-tuning training process
1. In the case of RFT, you'll also define a grader to score the model's behavior
1. Evaluate the results

Get started with [supervised fine-tuning](https://developers.openai.com/api/docs/guides/supervised-fine-tuning), [vision fine-tuning](https://developers.openai.com/api/docs/guides/vision-fine-tuning), [direct preference optimization](https://developers.openai.com/api/docs/guides/direct-preference-optimization), or [reinforcement fine-tuning](https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning).

## Learn from experts

Model optimization is a complex topic, and sometimes more art than science. Check out the videos below from members of the OpenAI team on model optimization techniques.



**Cost/accuracy/latency:** [Watch on YouTube](https://www.youtube.com/watch?v=Bx6sUDRMx-8)

**Distillation:** [Watch on YouTube](https://www.youtube.com/watch?v=CqWpJFK-hOo)

**Optimizing LLM Performance:** [Watch on YouTube](https://www.youtube.com/watch?v=ahnGLM-RC1Y)

