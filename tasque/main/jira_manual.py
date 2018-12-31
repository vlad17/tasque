"""
Ingests a CSV dump from IRA, then
displays classification interface.

Dumps CSV JIRA with column "manual_classification" into
the destination file.
"""

from absl import app, flags

from .. import log

flags.DEFINE_string(
    "dst", "./data/new.pkl", "path in which to save ingested input"
)

def _main(_argv):
    log.init()


if __name__ == "__main__":
    app.run(_main)
