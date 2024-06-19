import ast
import json
import logging
import re
import traceback
from typing import Any

json_warning = False

def set_json_warning(warning: bool):
    json_warning = warning

def json_loads(content: Any) -> Any:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        c = ( content.strip()
            .replace('\n{', '{').replace('{\n', '{').replace('\n}', '}').replace('}\n', '}')
            .replace(',\n', ',')
            .replace('\n[', '[').replace('[\n', '[').replace('\n]', ']').replace(']\n', ']')
        )
        c = re.sub(r"\"\n\s*}", "\"}", c)
        c = c.replace('\n', '\\n').replace('\t', '\\t')
        try:
            return json.loads(c)
        except json.JSONDecodeError as e:
            try:
                if json_warning:
                    logging.warn(f"### JSON Failed to parse content as JSON: {content}\tERROR: {e}\n{c}")
                    logging.warn(traceback.extract_stack())
                return ast.literal_eval(c)
            except Exception:
                if not json_warning:
                    logging.warn(f"Failed to parse content by AST: {content}")
                    logging.warn(traceback.extract_stack())
                return {}
