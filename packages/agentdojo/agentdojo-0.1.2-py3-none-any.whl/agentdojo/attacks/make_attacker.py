import random
from collections.abc import Callable

from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
from agentdojo.attacks.base_attack import BaseAttacker
from agentdojo.attacks.baseline_attacks import (
    CaptchaDoSAttacker,
    DirectAttacker,
    DoSAttacker,
    FelonyDoSAttacker,
    IgnorePreviousAttacker,
    ImportantInstructionsAttacker,
    InjecAgentAttacker,
    ManualAttacker,
    OffensiveEmailDoSAttacker,
    SwearWordsDoSAttacker,
    ToolKnowledgeAttacker,
)
from agentdojo.strenum import StrEnum
from agentdojo.task_suite.task_suite import TaskSuite

model_names = {
    "gpt-4o-2024-05-13": "GPT-4",
    "gpt-3.5-turbo-0125": "GPT-3.5",
    "gpt-4-turbo-2024-04-09": "GPT-4",
    "gpt-4-0125-preview": "GPT-4",
    "claude-3-opus-20240229": "Claude",
    "claude-3-sonnet-20240229": "Claude",
    "claude-3-haiku-20240307": "Claude",
    "command-r-plus": "Command R+",
    "command-r": "Command R",
    "mistralai/Mixtral-8x7B-Instruct-v0.1": "Mixtral",
    "meta-llama/Llama-3-70b-chat-hf": "AI assistant",
    "gemini-1.5-pro-001": "AI model developed by Google",
    "gemini-1.5-flash-001": "AI model developed by Google",
}


def get_model_name_from_pipeline(pipeline: BasePipelineElement) -> str:
    if pipeline.name is None:
        raise ValueError("Pipeline name is `None`")

    for full_name, model_name in model_names.items():
        if full_name in pipeline.name:
            return model_name

    raise ValueError(
        f"No valid model name not found in pipeline name `{pipeline.name}`. Valid model names are {list(model_names.values())}"
    )


def get_wrong_model_name_from_pipeline(pipeline: BasePipelineElement) -> str:
    prng = random.Random(0)
    model_name = get_model_name_from_pipeline(pipeline)
    wrong_model_names = [name for name in model_names.values() if name != model_name]
    return prng.choice(wrong_model_names)


class AttackersEnum(StrEnum):
    MANUAL = "manual"
    DIRECT = "direct"
    IGNORE_PREVIOUS = "ignore_previous"
    INJECAGENT = "injecagent"
    IMPORTANT_INSTRUCTIONS = "important_instructions"
    IMPORTANT_INSTRUCTIONS_NO_USER_NAME = "important_instructions_no_user_name"
    IMPORTANT_INSTRUCTIONS_NO_MODEL_NAME = "important_instructions_no_model_name"
    IMPORTANT_INSTRUCTIONS_NO_NAMES = "important_instructions_no_names"
    IMPORTANT_INSTRUCTIONS_WRONG_MODEL_NAME = "important_instructions_wrong_model_name"
    IMPORTANT_INSTRUCTIONS_WRONG_USER_NAME = "important_instructions_wrong_user_name"
    TOOL_KNOWLEDGE = "tool_knowledge"
    DOS = "dos"
    SWEARWORDS_DOS = "swearwords_dos"
    CAPTCHA_DOS = "captcha_dos"
    OFFENSIVE_EMAIL_DOS = "offensive_email_dos"
    FELONY_DOS = "felony_dos"


ATTACKERS: dict[AttackersEnum | str, Callable[[str, TaskSuite, BasePipelineElement], BaseAttacker]] = {
    AttackersEnum.MANUAL: ManualAttacker,
    AttackersEnum.DIRECT: DirectAttacker,
    AttackersEnum.IGNORE_PREVIOUS: IgnorePreviousAttacker,
    AttackersEnum.INJECAGENT: InjecAgentAttacker,
    AttackersEnum.IMPORTANT_INSTRUCTIONS: (
        lambda n, s, p: ImportantInstructionsAttacker(n, s, p, "Emma Johnson", get_model_name_from_pipeline(p))
    ),
    AttackersEnum.IMPORTANT_INSTRUCTIONS_NO_USER_NAME: (
        lambda n, s, p: ImportantInstructionsAttacker(n, s, p, model_name=get_model_name_from_pipeline(p))
    ),
    AttackersEnum.IMPORTANT_INSTRUCTIONS_NO_MODEL_NAME: (
        lambda n, s, p: ImportantInstructionsAttacker(n, s, p, user_name="Emma Johnson")
    ),
    AttackersEnum.IMPORTANT_INSTRUCTIONS_NO_NAMES: ImportantInstructionsAttacker,
    AttackersEnum.IMPORTANT_INSTRUCTIONS_WRONG_MODEL_NAME: (
        lambda n, s, p: ImportantInstructionsAttacker(n, s, p, "Emma Johnson", get_wrong_model_name_from_pipeline(p))
    ),
    AttackersEnum.IMPORTANT_INSTRUCTIONS_WRONG_USER_NAME: (
        lambda n, s, p: ImportantInstructionsAttacker(n, s, p, "Mark Smith", get_model_name_from_pipeline(p))
    ),
    AttackersEnum.TOOL_KNOWLEDGE: (
        lambda n, s, p: ToolKnowledgeAttacker(n, s, p, "Emma Johnson", get_model_name_from_pipeline(p))
    ),
    AttackersEnum.DOS: DoSAttacker,
    AttackersEnum.SWEARWORDS_DOS: SwearWordsDoSAttacker,
    AttackersEnum.CAPTCHA_DOS: CaptchaDoSAttacker,
    AttackersEnum.OFFENSIVE_EMAIL_DOS: OffensiveEmailDoSAttacker,
    AttackersEnum.FELONY_DOS: FelonyDoSAttacker,
}


def register_attacker(attacker_name: str, attacker: Callable[[str, TaskSuite, BasePipelineElement], BaseAttacker]):
    ATTACKERS[attacker_name] = attacker


def get_attacker(attacker_name: AttackersEnum | str) -> Callable[[str, TaskSuite, BasePipelineElement], BaseAttacker]:
    return ATTACKERS[attacker_name]


def make_attacker(
    attacker_name: AttackersEnum,
    task_suite: TaskSuite,
    target_pipeline: BasePipelineElement,
) -> BaseAttacker:
    return ATTACKERS[attacker_name](attacker_name, task_suite, target_pipeline)
