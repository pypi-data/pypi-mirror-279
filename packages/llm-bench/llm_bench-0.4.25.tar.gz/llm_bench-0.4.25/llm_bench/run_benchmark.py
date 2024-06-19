import argparse
import yaml
import subprocess
import datetime
import re

parser = argparse.ArgumentParser(
    prog="python3 check_models.py",
    description="Before running check_models.py, please make sure you installed ollama successfully \
        on macOS, Linux, or WSL2 on Windows. You can check the website: https://ollama.com")

parser.add_argument("-v",
                    "--verbose",
                    action="store_true",
                    help="this program helps you check whether you have ollama benchmark models installed")

parser.add_argument("-m",
                    "--models",
                    type=str,
                    help="provide benchmark models YAML file path. ex. ../data/benchmark_models.yml")

parser.add_argument("-b",
                    "--benchmark",
                    type=str,
                    help="provide benchmark YAML file path. ex. ../data/benchmark1.yml")

parser.add_argument("-t",
                    "--test",
                    action="store_true",
                    help="run in test mode with minimal output")

def parse_yaml(yaml_file_path):
    with open(yaml_file_path, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
    return data

def parse_duration(duration_str):
    """ Parse duration from strings in various formats (s, ms, µs, m+s) to seconds as a float. """
    if 'ms' in duration_str:
        return float(duration_str.replace('ms', '')) / 1000.0
    elif 'µs' in duration_str:
        return float(duration_str.replace('µs', '')) / 1000000.0
    elif 's' in duration_str:
        match = re.match(r'(?:(\d+)m)?(\d*\.?\d*)s', duration_str)
        if match:
            minutes = int(match.group(1)) if match.group(1) else 0
            seconds = float(match.group(2)) if match.group(2) else 0
            return 60 * minutes + seconds
        else:
            raise ValueError(f"Unsupported duration format: {duration_str}")
    else:
        raise ValueError("Unsupported duration format")

def run_benchmark(models_file_path, steps, benchmark_file_path, is_test, ollamabin):
    models_dict = parse_yaml(models_file_path)
    benchmark_dict = parse_yaml(benchmark_file_path)
    allowed_models = {e['model'] for e in models_dict['models']}
    ans = {}

    num_steps = steps
    prompt_dict = benchmark_dict['prompts']

    if is_test:
        prompt_dict = benchmark_dict["testPrompts"]
        num_steps = min(len(prompt_dict), steps)

    for model in models_dict['models']:
        model_name = model['model']
        if model_name in allowed_models:
            loc_dt = datetime.datetime.today()
            total_tokens = 0
            total_eval_duration = 0.0
            total_duration = 0.0
            eval_durations = []
            tokens_per_second = []

            if not is_test:
                print(f"Starting evaluation for model: {model_name}\n")

            for index, prompt in enumerate(prompt_dict[:num_steps], start=1):
                prompt_text = prompt['prompt']
                if not is_test:
                    print(f"Evaluating prompt {index}/{num_steps}")
                    print('-' * 10)

                try:
                    result = subprocess.run(
                        [ollamabin, 'run', model_name, prompt_text, '--verbose'],
                        capture_output=True,
                        text=True,
                        check=False,
                        encoding='utf-8'
                    )
                    std_err = result.stderr or ''

                    for line in std_err.split('\n'):
                        if line.lstrip().startswith("prompt"):
                            continue
                        if 'eval count:' in line:
                            tokens = int(line.split()[-2])
                            total_tokens += tokens
                            if not is_test:
                                print(f"Produced Tokens: {tokens}")
                        if 'eval duration:' in line:
                            duration_str = line.split(':')[-1].strip()
                            eval_duration = parse_duration(duration_str)
                            eval_durations.append(eval_duration)
                            tokens_per_second.append(tokens / eval_duration)
                            total_eval_duration += eval_duration
                            if not is_test:
                                print(f"Decoding Seconds: {eval_duration:.3f}s")
                                print(f"Tokens/Second: {tokens / eval_duration:.3f}")
                        if 'total duration:' in line:
                            duration_str = line.split(':')[-1].strip()
                            duration = parse_duration(duration_str)
                            total_duration += duration
                            if not is_test:
                                print(f"Total Inference Seconds: {duration:.3f}s")
                except subprocess.SubprocessError as e:
                    print(f"Error during subprocess execution: {e}")

                if not is_test:
                    print('-' * 10 + "\n")

            if total_eval_duration > 0:
                average_eval_rate = total_tokens / total_eval_duration
                ans[model_name] = {
                    'average_token_per_second': f"{average_eval_rate:.3f}",
                    'total_tokens': total_tokens,
                    'total_decoding_seconds': f"{total_eval_duration:.3f}",
                    'total_inference_seconds': f"{total_duration:.3f}",
                }
                if not is_test:
                    print(f"Results for {model_name}: {ans[model_name]}")
                    print('-' * 10 + "\n")

    if is_test:
        print("Test run successful.")

    return ans

if __name__ == "__main__": 
    args = parser.parse_args()
    if args.models and args.benchmark:
        run_benchmark(args.models, 10, args.benchmark, args.test, 'ollama')
        if not args.test:
            print('-' * 40)
