def kelly_criterion(win_probability, bookmaker_odds=2, fraction=0.5):
    return (win_probability * bookmaker_odds - 1) / (bookmaker_odds - 1) * fraction


def suggest_bets(report, bankroll, min_probability=0.6, team_or_draw_probability=0.6):
    def message(event, probability):
        amount_to_bet = round(
            kelly_criterion(probability, bookmaker_odds=2, fraction=0.2) * bankroll, 2
        )
        print(f"{event}, bet ${amount_to_bet}, probability {probability}")

    for _, row in report.iterrows():
        print(row.home_team, "-", row.away_team)
        if row.btts >= min_probability:
            message("Btts", row.btts)
        if row.btts_no >= min_probability:
            message("BttsNo", row.btts_no)
        if row.over >= min_probability:
            message("Over", row.over)
        if row.under >= min_probability:
            message("Under", row.under)
        if row.home_team_win + row.draw >= team_or_draw_probability:
            message("Team1 or X", row.home_team_win + row.draw)
        if row.away_team_win + row.draw >= team_or_draw_probability:
            message("Team2 or X", row.away_team_win + row.draw)
        print(" ")
