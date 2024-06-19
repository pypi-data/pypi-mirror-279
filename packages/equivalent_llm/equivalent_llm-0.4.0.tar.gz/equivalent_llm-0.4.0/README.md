# Validation tool to compare a generated context by sLLM to reference context

Generated sentence by sLLM is compared to the reference sentence to check whether the generated sentence is equivalent to the reference sentence or not.

## Validataion criteria

### Equivalence test

Tests whether the generated sentence is equivalent to the reference sentence or not

> eg. 신설동 주변 영화관 vs 신설동 근처 극장

### Consistency test

Tests whether the generated sentence is consistent with the given information or not

> eg. 2024 5/10 이후 주말 -> 2024-05-11 00:00:00 - 2024-05-12 23:59:59

### Grammar test

Tests whether the generated sentence is grammatically correct or not

> eg. "배트맨 영화는 고담 시티에서 범죄를 억류하는 두 년 만에, 달마다 살인범 리더(다노)를 추적하는 중에 도시의 부패를 밝혀내는 과정에서 시민을 위협하는 실제 형사를 찾아내는 책임을 맡게 됩니다." (???) -> "배트맨 영화는 고담 시티에서 범죄와 싸우는 지 2년 된 배트맨이 리들러라는 연쇄 살인범을 추적하면서 도시의 부패를 밝혀내는 내용입니다."

### Elegant test

Tests whether the generated sentence is firmly well-structed to human readablity or not

> eg. "내일 '아쿠아맨과 로스트 킹덤'을 관람하실 수 있는 시간을 조회했습니다. 어느 시간에 예약을 도와드릴까요?" -> "홍대입구 상영관에서 '아쿠아맨과 로스트 킹덤' 영화 예약을 도와드릴까요? 언제 관람하시길 원하세요?"

### Etc

-   Function name matching
-   Arugments matching
-   Required arguments

## Input data format

Three kinds of information are required for the validation. The input data is composed of the following 3 items.

-   Context: The context of previously processed sentences
-   Reference (a.k.a. Answer): The reference sentence for function call or reservation board (a.k.a. formatted output) related message
-   Generated: The generated sentence for function call or reservation board related message

### JSON string

Example

```json
{
    "context": "<s>[INST] <<SYS>>\nYou are a helpful and respectful movie ticketing assistant.\nYou\"re actively involved in a three-way conversation with \"user\", \"function\" (the function helper other than you), ...",
    "answer": "{\"function_call\": {\"name\": \"extract_date_time\", \"arguments\": \"{\\\"query\\\":\\\"현재 시간을 알려주세요~\\\"}\"}, \"role\": \"assistant\", \"content\": null} ",
    "generated": "{\"function_call\": {\"name\": \"extract_date_time\", \"arguments\": \"{\\\"query\\\":\\\"현재 시간을 알려주세요\\\"}\"}, \"role\": \"assistant\", \"content\": null} "
}
```

### CSV file

```csv
index, context, answer, generated
0,<s>[INST] <<SYS>>\nYou are a...,{"function_call": {...,{"function_call": {...
```

### Supported LLM models

-   Llama 3 (default)
-   Llama 2
-   Mistral
-   A.X

## Installation

```bash
pip install equivalent_llm
```

## Prompt Engines

### Azure@GIP

It uses Prompt Engineering Tool (PET) based on Azure@GIP. You need to set your configurations. You can set the API key in two ways: in command line or in python.

If PET_ID, PET_URL, or PET_TIMEOUT is not set, default values are used.
PET_ID is related to OpenAI model directly. Default PET_ID uses ChatGPT 4 (gpt-4-1106).
Default PET_URL is only accessible on restricted network (eg. DeDVI).

In command line:

```bash
export PET_URL="pet_ip:port"
export PET_ID="your-id"
export PET_TIMEOUT=60
```

In python:

```python
import os
os.environ["PET_URL"] = "pet_ip:port"
os.environ["PET_ID"] = "your-id"
os.environ["PET_TIMEOUT"] = "60"
```

### OpenAI API key (deprecated)

It uses ChatGPT 4-turbo API on default. You need to set your API key to use this tool. You can set the API key in two ways: in command line or in python.

In command line:

```bash
export OPENAI_API_KEY="your-api-key"
```

In python:

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"
```

Also, you should run commands with **prompt_engine='OpenAI'** option.

## Usage

For the validation set, you can use the following code:

```python
import equivalent_llm

# Validation from CSV file
validated = equivalent_llm.validate("data.csv")

json_list = validated["input_data"]
validation_results = validated["validations"]

# Validation from JSON list
equivalent_llm.validate(json_list)

# If you want to validate only subset of data, which can set as list of indexes
equivalent_llm.validate(json_list, indexes=[1,3,5])
# If you want to validate only one
equivalent_llm.validate(json_list, indexes=4)
# If you want to validate some range
equivalent_llm.validate(json_list, indexes=range(0, 15, 3))
```

If you want to validate with prompts, you can use the following code:

```python
import logging
debug_logger = logging.getLogger('debug_logger')
debug_logger.setLevel(logging.DEBUG)
index = 6
equivalent_llm.EquvalentLLM(json_list[index]['context'], json_list[index]['answer'], json_list[index]['generated'], logger=debug_logger)
```

## Output

### Function call (Task 1)

```json
{
  "target": "extract_date_time",
  "tests": {
    "equivalence": [{"argument": "query", "passed": true, "score": 98, "evidence": "The target sentence is equivalent to the reference sentence, with the only difference being the omission of a tilde (~) which is often used to soften the tone in informal contexts. This does not change the meaning of the sentence."}],
    "consistency": [{"argument": "query", "passed": true, "score": 100, "evidence": "..."}],
    "grammar": [{"argument": "query", "passed": true, "score": 100, "evidence": "..."}],
    "elegance": [],
    "function_name": {"passed": true},
    "required": {"passed": true},
    "paired_arguments": {"passed": true}},
  "passed": true,
  "count": {
  "total": {"passed": 3, "total": 3},
    "equivalence": {"passed": 1, "total": 1},
    "consistency": {"passed": 1, "total": 1},
    "grammar": {"passed": 1, "total": 1},
    "elegance": {"passed": 0, "total": 0},
    "etc": {"passed": 3, "total": 3}
  },
  "reference": {...},
  "generated": {...},
  "given_information": [...],
  "index": 0}
```

## Reservation board (a.k.a Formatted output) (Task 2)

```json
{
    "target": "reservation_board",
    "tests": {
        "equivalence": [{"element": "answer", "passed": true, "evidence": "..."}, {"element": "template", "passed": true, "evidence": "..."}],
    "consistency": [{"element": "answer", "passed": true, "score": 100, "evidence": "..."}],
    "grammar": [{"element": "answer", "passed": true, "score": 100, "evidence": "..."}],
    "elegance": [{"element": "answer", "passed": true, "score": 100, "evidence": "...", "alternative": "현재 시간은 14시 36분입니다."}]
  },
  "passed": true,
  "count": {
    "total": {"passed": 5, "total": 5},
    "equivalence": {"passed": 2, "total": 2},
    "consistency": {"passed": 1, "total": 1},
    "grammar": {"passed": 1, "total": 1},
    "elegance": {"passed": 1, "total": 1}
  },
  "reference": {...},
  "generated": {...},
  "given_information": [...],
  "index": 1}
```

## Build a package

1. Install [PDM](https://pdm-project.org/en/latest/) package
2. Build and install a package

```bash
# pdm build (or pdm build --release)
pdm install
```
