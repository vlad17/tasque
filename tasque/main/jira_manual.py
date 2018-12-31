"""
Ingests a CSV dump from IRA, then
displays classification interface.

Dumps CSV JIRA with column "class" into
the destination file.
"""

import numpy as np
from absl import app, flags
import pandas as pd
import os

from .. import log
from ..interactive_classify import classify_list

flags.DEFINE_string(
    "src", None, "path from which to ingest the JIRA csv"
)
flags.mark_flag_as_required("src")

flags.DEFINE_string(
    "dst", "./data/classified_jira.pkl", "path in which to save ingested input"
)

def _main(_argv):
    log.init()

    log.debug("reading input CSV from {}", flags.FLAGS.src)
    srcdf = pd.read_csv(flags.FLAGS.src)
    isdone = srcdf["Resolution"] == "Done"
    log.debug("only inspecting {} of {} rows in src that are done",
              isdone.sum(), len(srcdf))
    srcdf = srcdf[isdone].reset_index(drop=True)

    if os.path.isfile(flags.FLAGS.dst):
        log.debug("existing dst {} found, warm-starting", flags.FLAGS.dst)
        df = pd.read_pickle(flags.FLAGS.dst)
        keys = df[~pd.isnull(df["class"])]["Issue key"].unique()
        present = srcdf["Issue key"].isin(keys)
        log.debug("found {} keys already classified, skipping those",
                  present.sum())
        old = srcdf["Issue key"].isin(df["Issue key"].unique())
        log.debug("found {} new keys to classify, adding those",
                  (~old).sum())
        df = pd.concat([df, srcdf[~old]], ignore_index=True, sort=False)
    else:
        df = srcdf
        df["class"] = np.nan

    unclassified = df[pd.isnull(df["class"])].copy()
    log.debug("{} items left to classify", len(unclassified))

    unclassified.fillna("<missing>", inplace=True)

    def _print_next():
        for _, row in unclassified.iterrows():
            yield (
                row["Issue key"] + ": " + row["Summary"] + "\n" +
                row["Issue Type"] + " " + row["Assignee"] + " " +
                row["Resolved"] + " " + row["Labels"] + "\n" +
                row["Sprint"] + " "  + row["Component/s"] + " " +
                row["Custom field (Swim Lane)"] + "\n" +
                (row["Description"] or "")[:160])

    initial_options = df[~pd.isnull(df["class"])]["class"].value_counts().to_dict()

    classifications = classify_list(
        initial_options, _print_next())

    log.debug("got {} new classifications", len(classifications))

    for idx, cls in zip(unclassified.index, classifications):
        df.loc[idx, "class"] = cls

    log.debug("saving results in {}", flags.FLAGS.dst)
    df.to_pickle(flags.FLAGS.dst)

if __name__ == "__main__":
    app.run(_main)
