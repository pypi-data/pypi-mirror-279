import logging

import pandas as pd

from ranking_table_tennis import helpers, models
from ranking_table_tennis.configs import ConfigManager

logger = logging.getLogger(__name__)


def print_rating_context(
    tournaments: models.Tournaments,
    players: models.Players,
    initial_ranking: models.Rankings,
    name: str,
    tid: str,
) -> None:
    # Helper to assign an initial rating to name
    print("# Information that should help you assign rating")
    print("\n# Matches")

    cfg = ConfigManager().current_config

    # Print matches results for the unknown player
    matches = tournaments.get_matches(tid, False, [])
    matches_selected = matches[(matches.player_a == name) | (matches.player_b == name)].copy()
    print(matches_selected[["winner", "winner_pid", "loser", "loser_pid", "round", "category"]])

    matches_as_winner = matches[(matches.winner == name)].copy()
    fill_rating_column(matches_as_winner, tournaments, initial_ranking, "loser_pid")
    print("winner matches")
    print(matches_as_winner[["winner", "winner_pid", "loser", "loser_pid", "round", "category", "rating"]])


    matches_as_loser = matches[(matches.loser == name)].copy()
    fill_rating_column(matches_as_loser, tournaments, initial_ranking, "winner_pid")
    print("loser matches")
    print(matches_as_loser[["winner", "winner_pid", "loser", "loser_pid", "round", "category", "rating"]])

    # # Print rating of known players, if available
    # try:
    #     known_rankings = helpers.load_from_pickle(cfg.io.pickle.rankings)
    # except (FileNotFoundError):
    #     logger.warn(
    #         "WARNING: Previous rankings are not available. Initial rankings will be loaded."
    #     )
    #     known_rankings = initial_ranking

    # try:
    #     tids = [cfg.initial_metadata.initial_tid] + [t for t in tournaments]  # to use prev_tid
    #     pids_with_rating = known_rankings.get_entries(tids[-2]).pid.to_list()
    #     pids_selected = (
    #         pd.concat([matches_selected.winner_pid, matches_selected.loser_pid], ignore_index=True)
    #         .dropna()
    #         .pipe(lambda s: s[s.isin(pids_with_rating)])  # filter pids with known rating
    #         .unique()
    #     )
    #     print(f"\n# Known ratings (categories thresholds: {cfg.compute.categories_thresholds})")
    #     for pid in pids_selected:
    #         print(
    #             f"# {tids[-2]}, {players[pid]['name']}, "
    #             f"rating: {known_rankings.get_entries(tids[-2], pid).get('rating')}"
    #         )
    # except AttributeError:
    #     logger.warn("Sorry, no previous ranking is available to help you")

def fill_rating_column(matches_df, tournaments, initial_rankings, rival_pid_col):
    matches_df["rating"] = pd.NA

    cfg = ConfigManager().current_config
    tids = [cfg.initial_metadata.initial_tid] + [t for t in tournaments]  # to use prev_tid
    prev_tid = tids[-2]
    known_rankings = helpers.load_from_pickle(cfg.io.pickle.rankings)
    initial_rankings

    for ix, row in matches_df.iterrows():
        try:
            known_rankings.get_entries(tids[-2], row[rival_pid_col]).get('rating')

        # matches_df.loc[ix, "rating"]



# def get_rating_to_compare(row, initial_ranking, tournaments, rival_pid_col):
#     rating = pd.NA
#     pid = row[rival_pid_col]
#     if pid:
#         cfg = ConfigManager().current_config

#         known_rankings = helpers.load_from_pickle(cfg.io.pickle.rankings)
#         tids = [cfg.initial_metadata.initial_tid] + [t for t in tournaments]  # to use prev_tid
#         rating = known_rankings.get_entries(tids[-2], pid).get('rating')

#     return rating
