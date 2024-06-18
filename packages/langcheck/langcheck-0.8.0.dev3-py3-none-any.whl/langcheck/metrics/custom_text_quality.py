from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, Template, meta

from langcheck.metrics._validation import validate_parameters_custom_evaluator
from langcheck.metrics.eval_clients import EvalClient
from langcheck.metrics.metric_value import MetricValue


def custom_evaluator(generated_outputs: list[str] | str | None,
                     prompts: list[str] | str | None,
                     sources: list[str] | str | None,
                     reference_outputs: list[str] | str | None,
                     eval_model: EvalClient, metric_name: str,
                     score_map: dict[str, float], template_path: str,
                     language: str) -> MetricValue[float | None]:
    '''Calculates the scores of a custom evaluator. The EvalClient will first
    assess the provided inputs using the prompt template, and then convert those
    assessments into scores using the score map.

    The prompt template should be a Jinja2 file (file extension .j2) that
    specifies the criteria that an LLM (as configured in the Eval Client) should
    follow when evaluating an instance. The template is allowed to have
    placeholders for the following variables (NOTE: not all are required):
    - `gen_output`: The generated output
    - `user_query`: The prompt
    - `src`: The source text
    - `ref_output`: The reference output

    The prompt template should also specify the final available assessments for
    the LLM evaluator, e.g. "Good", "Bad", "Neutral", etc. The score map should
    then map each of those available assessments to a numerical score. E.g. if
    the available assessments in the prompt template are "Good", "Bad", and
    "Neutral", the score map should be something like:
    ``score_map = {'Good': 1.0, 'Neutral': 0.5, 'Bad': 0.0}``

    NOTE: We have found that LLM models sometimes behave weirdly when the
    assessments are non-ascii characters (see
    https://github.com/citadel-ai/langcheck/pull/84 as an example). So, we
    recommend making the final assessments ascii characters, even when the rest
    of the prompt template contains non-ascii characters (e.g. Japanese).

    Args:
        generated_outputs: The model generated output(s)
        prompts: The prompts used to generate the output(s)
        sources: The source(s) of the generated output(s)
        reference_outputs: The reference output(s)
        eval_model: The EvalClient instance used for the evaluation
        metric_name: The name of the metric
        score_map: A dictionary mapping the evaluator's assessments to scores
        template_path: The path to the prompt template file. This should be a
            Jinja2 file (file extension .j2).
        language: The language that the evaluator will use ('en', 'ja', or 'de')

    Returns:
        A MetricValue object
    '''
    generated_outputs, prompts, reference_outputs, sources = validate_parameters_custom_evaluator(  # NOQA: E501
        generated_outputs, prompts, reference_outputs, sources)
    # Find the length of the first non-None list (they are guaranteed to all be
    # the same length)
    num_examples = next(
        (len(lst)
         for lst in [generated_outputs, prompts, reference_outputs, sources]
         if lst is not None), 0)

    if language not in ['en', 'ja', 'de']:
        raise ValueError(f'Unsupported language: {language}')

    assert Path(template_path).exists(
    ), f'Prompt template file {template_path} does not exist.'
    assert template_path.endswith('.j2'), \
        'The prompt template file must be a Jinja2 template file with the extension ".j2"'  # NOQA: E501

    prompt_template_source = Path(template_path).read_text()
    prompt_template = Template(prompt_template_source)

    # Validate the expected parameters in the prompt template
    env = Environment()
    expected_params = meta.find_undeclared_variables(
        env.parse(prompt_template_source))
    allowed_params = ['gen_output', 'user_query', 'src', 'ref_output']
    assert all(param in allowed_params for param in expected_params), \
        f'The prompt template contains invalid parameters. The allowed parameters are {allowed_params} but the prompt template expects the parameters {expected_params}'  # NOQA: E501
    expected_param_to_arg = {
        'gen_output': generated_outputs,
        'user_query': prompts,
        'src': sources,
        'ref_output': reference_outputs,
    }
    for param in expected_params:
        assert expected_param_to_arg[param] is not None, \
            f'The prompt template expects the parameter "{param}" but it is not provided.'  # NOQA: E501

    def _args_to_prompt_param(generated_outputs, prompts, sources,
                              reference_outputs, index):
        prompt_param = {}
        if generated_outputs is not None:
            prompt_param['gen_output'] = generated_outputs[index]
        if prompts is not None:
            prompt_param['user_query'] = prompts[index]
        if sources is not None:
            prompt_param['src'] = sources[index]
        if reference_outputs is not None:
            prompt_param['ref_output'] = reference_outputs[index]
        return prompt_param

    populated_prompts = []
    for i in range(num_examples):
        prompt_param = _args_to_prompt_param(generated_outputs, prompts,
                                             sources, reference_outputs, i)
        populated_prompts.append(prompt_template.render(prompt_param))

    scores, explanations = eval_model.get_score(
        metric_name=metric_name,
        language=language,
        prompts=populated_prompts,
        score_map=score_map,
    )

    return MetricValue(metric_name=metric_name,
                       prompts=prompts,
                       generated_outputs=generated_outputs,
                       reference_outputs=reference_outputs,
                       sources=sources,
                       explanations=explanations,
                       metric_values=scores,
                       language=language)
