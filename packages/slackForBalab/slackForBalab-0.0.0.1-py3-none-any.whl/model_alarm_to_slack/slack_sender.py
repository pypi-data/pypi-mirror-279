from typing import List
import os
import datetime
import traceback
import functools
import json
import socket
import requests
import dotenv

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def slack_sender(name: str, user_mentions: List[str] = []):
    """
    Original code is from https://github.com/huggingface/knockknock in slack_sender.py

    Slack sender wrapper: execute func, send a Slack notification with the end status
    (sucessfully finished or crashed) at the end. Also send a Slack notification before
    executing func.

    'name': str
        The name as registered in the Slack workspace.
    """

    dotenv.load_dotenv()
    webhook_url = os.environ.get(name)

    dump = {}

    def decorator_sender(func):
        @functools.wraps(func)
        def wrapper_sender(*args, **kwargs):

            start_time = datetime.datetime.now()
            host_name = socket.gethostname()
            func_name = func.__name__

            # Handling distributed training edge case.
            # In PyTorch, the launch of `torch.distributed.launch` sets up a RANK environment variable for each process.
            # This can be used to detect the master process.
            # See https://github.com/pytorch/pytorch/blob/master/torch/distributed/launch.py#L211
            # Except for errors, only the master process will send notifications.
            if 'RANK' in os.environ:
                master_process = (int(os.environ['RANK']) == 0)
                host_name += ' - RANK: %s' % os.environ['RANK']
            else:
                master_process = True

            if master_process:
                contents = [
                    f"{name}'s training has started 🚀",
                    f"Main call\n • {func_name}",
                    f"Starting date\n • {start_time.strftime(DATE_FORMAT)}",
                    "============================"
                ]
                contents.append(' '.join(user_mentions))
                dump['text'] = '\n'.join(contents)
                dump['icon_emoji'] = ':rocket:'
                requests.post(webhook_url, json.dumps(dump))

            try:
                value = func(*args, **kwargs)

                if master_process:
                    end_time = datetime.datetime.now()
                    elapsed_time = end_time - start_time
                    contents = [
                        f"{name}'s training is complete 🎉",
                        f"[Main call]\n • {func_name}",
                        f"[Starting date]\n • {start_time.strftime(DATE_FORMAT)}",
                        f"[End date]\n • {end_time.strftime(DATE_FORMAT)}",
                        f"[Training duration]\n • {str(elapsed_time)}"
                    ]   

                    try:
                        str_value = str(value)
                        contents.append(f"[Main call returned value]\n • {str_value}")
                    except:
                        contents.append(f"[Main call returned value]\n • ERROR - Couldn\'t str the returned value.")

                    contents.append(' '.join(user_mentions))
                    dump['text'] = '\n'.join(contents)
                    dump['icon_emoji'] = ':tada:'
                    requests.post(webhook_url, json.dumps(dump))

                return value

            except Exception as ex:
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                contents = [
                    f"{name}'s training has crashed ☠️",
                    f"[Machine name]\n • {host_name}",
                    f"[Main call]\n • {func_name}",
                    f"[Starting date]\n • {start_time.strftime(DATE_FORMAT)}",
                    f"[Crash date]\n • {end_time.strftime(DATE_FORMAT)}",
                    f"[Crashed training duration]\n • {str(elapsed_time)}\n\n",
                    "Here's the error:",
                    f"• {ex}\n\n",
                    "Traceback:",
                    f"• {traceback.format_exc()}"
                ]
                contents.append(' '.join(user_mentions))
                dump['text'] = '\n'.join(contents)
                dump['icon_emoji'] = ':skull_and_crossbones:'
                requests.post(webhook_url, json.dumps(dump))
                raise ex

        return wrapper_sender

    return decorator_sender