import json
from typing import Optional, Dict, Text, Any

import sys

from pathlib import Path


def check_if_pr_has_release_milestone(event: Optional[Dict[Text, Any]]):
    if (
        not event
        or not event.get("pull_request")
        or not event["pull_request"].get("milestone")
    ):
        return False

    milestone = event["pull_request"]["milestone"]
    milestone_title = milestone.get("title", "")
    return milestone_title.startswith("Rasa X")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "You need to pass in the path to the github event as a "
            "parameter to this script."
        )
        sys.exit(1)
    path_to_event = sys.argv[1]
    with Path(path_to_event).open() as f:
        event = json.load(f)

    if check_if_pr_has_release_milestone(event):
        print("Found a milestone on the PR!")
    else:
        print(
            "Did NOT find a milestone on the PR! Please make sure to add this"
            "PR to a release milestone."
        )
        print(f"Event: \n{json.dumps(event, indent=2)}")
        sys.exit(1)
