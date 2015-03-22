from peewee import *
import os
import logging

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('peewee.log', mode='w'))

if (os.getenv('SERVER_SOFTWARE') and
    os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
    instance_name = 'future-glider-87801:nfl'
    database = MySQLDatabase('nfl',
                             unix_socket='/cloudsql/{}'.format(instance_name),
                             user='root')
else:
    # database = MySQLDatabase('nfl',
                             # **{'host': 'localhost',
                                # 'password': 'bOVE3kKsVpRq57eums8D',
                                # 'user': 'nfl_user', })
    database = MySQLDatabase('nfl',
                             **{'host': 'localhost',
                                'password': '',
                                'user': 'root', })


class UnknownField(object):
    pass


class BaseModel(Model):
    class Meta:
        database = database


class Stadium(BaseModel):
    stadium = PrimaryKeyField(db_column='stadium_id')
    name = CharField(null=True)
    team = CharField(null=True)
    location = CharField(null=True)
    latitude = FloatField()
    longitude = FloatField()

    class Meta:
        db_table = 'stadiums'

    def best_players_at(self, pos):

        q = (Player
             .select()
             .join(HighSchool)
             .join(Stadium, on=HighSchool.closest_stadium)
             .where((Player.pos == pos)
                    & (Player.active == True)
                    & (Stadium.stadium == self))
             .order_by(Player.weighted_av.desc())
             .limit(3))

        return [p for p in q]

    def abbr(self):
        return Team.select().where(Team.stadium == self.stadium)[0].abbr


class Team(BaseModel):
    team = PrimaryKeyField(db_column='team_id')
    stadium = ForeignKeyField(Stadium, related_name='teams')
    name = CharField(null=True)
    abbr = CharField(null=True)
    pfr_abbr = CharField(null=True)
    pfr_name = CharField(null=True)
    pri_color = CharField(null=True)
    sec_color = CharField(null=True)

    class Meta:
        db_table = 'teams'


class Position(BaseModel):
    position = PrimaryKeyField(db_column='position_id')
    name = CharField(null=True)

    class Meta:
        db_table = 'positions'

class HighSchool(BaseModel):
    high_school = PrimaryKeyField(db_column='high_school_id')
    closest_stadium = ForeignKeyField(
        Stadium,
        related_name='schools',
        to_field='stadium')
    name = CharField(null=True)
    city = CharField(null=True)
    state = CharField(null=True)
    full_address = CharField(null=True)
    country = CharField(null=True)
    pfr_high_school_id = CharField(null=True, unique=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)

    class Meta:
        db_table = 'high_schools'


class Player(BaseModel):
    player = PrimaryKeyField(db_column='player_id')
    pfr_high_school = ForeignKeyField(
        HighSchool,
        related_name='pfr_players',
        to_field='pfr_high_school_id')
    high_school = ForeignKeyField(
        HighSchool,
        related_name='players')
    birthday = CharField(null=True)
    birthplace = CharField(null=True)
    birth_city = CharField(null=True)
    birth_state = CharField(null=True)
    college = CharField(null=True)
    high_school_name = CharField(null=True)
    name = CharField(null=True)
    pfr_player_id = CharField(null=True)
    url = CharField(null=True)
    birthday_date = DateField(null=True)
    weighted_av = FloatField(null=True)
    pos = CharField(null=True)
    active = BooleanField()

    class Meta:
        db_table = 'players'


class StadiumPlayerPosition(BaseModel):
    stadium_player_position = PrimaryKeyField(db_column='stadium_player_position_id')
    player = ForeignKeyField(Player)
    stadium = ForeignKeyField(Stadium)
    position = ForeignKeyField(Position)
    order = IntegerField(null=True, db_column='ord')

    class Meta:
        db_table = 'stadium_player_positions'


class PlayerSeasons(BaseModel):
    player_seasons = PrimaryKeyField(db_column='player_seasons_id')
    player = ForeignKeyField(Player, related_name='seasons')
    pfr_player_id = CharField(null=True)
    year = IntegerField(null=True)
    av = IntegerField(null=True)
    defense_age = IntegerField(null=True)
    defense_av = IntegerField(null=True)
    defense_def_int = IntegerField(null=True)
    defense_def_int_long = IntegerField(null=True)
    defense_def_int_td = IntegerField(null=True)
    defense_def_int_yds = IntegerField(null=True)
    defense_fumbles = IntegerField(null=True)
    defense_fumbles_forced = IntegerField(null=True)
    defense_fumbles_rec = IntegerField(null=True)
    defense_fumbles_rec_td = IntegerField(null=True)
    defense_fumbles_rec_yds = IntegerField(null=True)
    defense_g = IntegerField(null=True)
    defense_gs = IntegerField(null=True)
    defense_pass_defended = IntegerField(null=True)
    defense_playoffs_age = IntegerField(null=True)
    defense_playoffs_def_int = IntegerField(null=True)
    defense_playoffs_def_int_long = IntegerField(null=True)
    defense_playoffs_def_int_td = IntegerField(null=True)
    defense_playoffs_def_int_yds = IntegerField(null=True)
    defense_playoffs_fumbles = IntegerField(null=True)
    defense_playoffs_fumbles_forced = IntegerField(null=True)
    defense_playoffs_fumbles_rec = IntegerField(null=True)
    defense_playoffs_fumbles_rec_td = IntegerField(null=True)
    defense_playoffs_fumbles_rec_yds = IntegerField(null=True)
    defense_playoffs_g = IntegerField(null=True)
    defense_playoffs_gs = IntegerField(null=True)
    defense_playoffs_pass_defended = IntegerField(null=True)
    defense_playoffs_pos = CharField(null=True)
    defense_playoffs_sacks = FloatField(null=True)
    defense_playoffs_safety_md = IntegerField(null=True)
    defense_playoffs_tackles_assists = IntegerField(null=True)
    defense_playoffs_tackles_solo = IntegerField(null=True)
    defense_playoffs_team = CharField(null=True)
    defense_playoffs_year_id = IntegerField(null=True)
    defense_pos = CharField(null=True)
    defense_sacks = FloatField(null=True)
    defense_safety_md = IntegerField(null=True)
    defense_tackles_assists = IntegerField(null=True)
    defense_tackles_solo = IntegerField(null=True)
    defense_team = CharField(null=True)
    defense_uniform_number = IntegerField(null=True)
    defense_year_id = CharField(null=True)
    kicking_age = IntegerField(null=True)
    kicking_av = IntegerField(null=True)
    kicking_fg_perc = CharField(null=True)
    kicking_fga = IntegerField(null=True)
    kicking_fga1 = IntegerField(null=True)
    kicking_fga2 = IntegerField(null=True)
    kicking_fga3 = IntegerField(null=True)
    kicking_fga4 = IntegerField(null=True)
    kicking_fga5 = IntegerField(null=True)
    kicking_fgm = IntegerField(null=True)
    kicking_fgm1 = IntegerField(null=True)
    kicking_fgm2 = IntegerField(null=True)
    kicking_fgm3 = IntegerField(null=True)
    kicking_fgm4 = IntegerField(null=True)
    kicking_fgm5 = IntegerField(null=True)
    kicking_g = IntegerField(null=True)
    kicking_gs = IntegerField(null=True)
    kicking_pos = CharField(null=True)
    kicking_punt = IntegerField(null=True)
    kicking_punt_blocked = IntegerField(null=True)
    kicking_punt_long = IntegerField(null=True)
    kicking_punt_yds = IntegerField(null=True)
    kicking_punt_yds_per_punt = FloatField(null=True)
    kicking_team = CharField(null=True)
    kicking_uniform_number = IntegerField(null=True)
    kicking_xp_perc = CharField(null=True)
    kicking_xpa = IntegerField(null=True)
    kicking_xpm = IntegerField(null=True)
    kicking_year_id = CharField(null=True)
    passing_advanced_age = IntegerField(null=True)
    passing_advanced_g = IntegerField(null=True)
    passing_advanced_gs = IntegerField(null=True)
    passing_advanced_pass_adj_net_yds_per_att_index = IntegerField(null=True)
    passing_advanced_pass_adj_yds_per_att_index = IntegerField(null=True)
    passing_advanced_pass_att = IntegerField(null=True)
    passing_advanced_pass_cmp_perc_index = IntegerField(null=True)
    passing_advanced_pass_int_perc_index = IntegerField(null=True)
    passing_advanced_pass_net_yds_per_att_index = IntegerField(null=True)
    passing_advanced_pass_rating_index = IntegerField(null=True)
    passing_advanced_pass_sacked_perc_index = IntegerField(null=True)
    passing_advanced_pass_td_perc_index = IntegerField(null=True)
    passing_advanced_pass_yds_per_att_index = IntegerField(null=True)
    passing_advanced_pos = CharField(null=True)
    passing_advanced_qb_rec = CharField(null=True)
    passing_advanced_team = CharField(null=True)
    passing_advanced_uniform_number = IntegerField(null=True)
    passing_advanced_year_id = CharField(null=True)
    passing_age = IntegerField(null=True)
    passing_av = IntegerField(null=True)
    passing_comebacks = IntegerField(null=True)
    passing_g = IntegerField(null=True)
    passing_gs = IntegerField(null=True)
    passing_gwd = IntegerField(null=True)
    passing_pass_adj_net_yds_per_att = FloatField(null=True)
    passing_pass_adj_yds_per_att = FloatField(null=True)
    passing_pass_att = IntegerField(null=True)
    passing_pass_cmp = IntegerField(null=True)
    passing_pass_cmp_perc = FloatField(null=True)
    passing_pass_int = IntegerField(null=True)
    passing_pass_int_perc = FloatField(null=True)
    passing_pass_long = IntegerField(null=True)
    passing_pass_net_yds_per_att = FloatField(null=True)
    passing_pass_rating = FloatField(null=True)
    passing_pass_sacked = IntegerField(null=True)
    passing_pass_sacked_perc = FloatField(null=True)
    passing_pass_sacked_yds = IntegerField(null=True)
    passing_pass_td = IntegerField(null=True)
    passing_pass_td_perc = FloatField(null=True)
    passing_pass_yds = IntegerField(null=True)
    passing_pass_yds_per_att = FloatField(null=True)
    passing_pass_yds_per_cmp = FloatField(null=True)
    passing_pass_yds_per_g = FloatField(null=True)
    passing_playoffs_age = IntegerField(null=True)
    passing_playoffs_comebacks = IntegerField(null=True)
    passing_playoffs_g = IntegerField(null=True)
    passing_playoffs_gs = IntegerField(null=True)
    passing_playoffs_gwd = IntegerField(null=True)
    passing_playoffs_pass_adj_net_yds_per_att = FloatField(null=True)
    passing_playoffs_pass_adj_yds_per_att = FloatField(null=True)
    passing_playoffs_pass_att = IntegerField(null=True)
    passing_playoffs_pass_cmp = IntegerField(null=True)
    passing_playoffs_pass_cmp_perc = FloatField(null=True)
    passing_playoffs_pass_int = IntegerField(null=True)
    passing_playoffs_pass_int_perc = FloatField(null=True)
    passing_playoffs_pass_long = IntegerField(null=True)
    passing_playoffs_pass_net_yds_per_att = FloatField(null=True)
    passing_playoffs_pass_rating = FloatField(null=True)
    passing_playoffs_pass_sacked = IntegerField(null=True)
    passing_playoffs_pass_sacked_perc = FloatField(null=True)
    passing_playoffs_pass_sacked_yds = IntegerField(null=True)
    passing_playoffs_pass_td = IntegerField(null=True)
    passing_playoffs_pass_td_perc = FloatField(null=True)
    passing_playoffs_pass_yds = IntegerField(null=True)
    passing_playoffs_pass_yds_per_att = FloatField(null=True)
    passing_playoffs_pass_yds_per_cmp = FloatField(null=True)
    passing_playoffs_pass_yds_per_g = FloatField(null=True)
    passing_playoffs_pos = CharField(null=True)
    passing_playoffs_qb_rec = CharField(null=True)
    passing_playoffs_team = CharField(null=True)
    passing_playoffs_year_id = IntegerField(null=True)
    passing_pos = CharField(null=True)
    passing_qb_rec = CharField(null=True)
    passing_qbr = FloatField(null=True)
    passing_team = CharField(null=True)
    passing_uniform_number = IntegerField(null=True)
    passing_year_id = CharField(null=True)
    receiving_and_rushing_age = IntegerField(null=True)
    receiving_and_rushing_av = IntegerField(null=True)
    receiving_and_rushing_fumbles = IntegerField(null=True)
    receiving_and_rushing_g = IntegerField(null=True)
    receiving_and_rushing_gs = IntegerField(null=True)
    receiving_and_rushing_playoffs_age = IntegerField(null=True)
    receiving_and_rushing_playoffs_fumbles = IntegerField(null=True)
    receiving_and_rushing_playoffs_g = IntegerField(null=True)
    receiving_and_rushing_playoffs_gs = IntegerField(null=True)
    receiving_and_rushing_playoffs_pos = CharField(null=True)
    receiving_and_rushing_playoffs_rec = IntegerField(null=True)
    receiving_and_rushing_playoffs_rec_long = IntegerField(null=True)
    receiving_and_rushing_playoffs_rec_per_g = FloatField(null=True)
    receiving_and_rushing_playoffs_rec_td = IntegerField(null=True)
    receiving_and_rushing_playoffs_rec_yds = IntegerField(null=True)
    receiving_and_rushing_playoffs_rec_yds_per_g = FloatField(null=True)
    receiving_and_rushing_playoffs_rec_yds_per_rec = FloatField(null=True)
    receiving_and_rushing_playoffs_rush_att = IntegerField(null=True)
    receiving_and_rushing_playoffs_rush_att_per_g = FloatField(null=True)
    receiving_and_rushing_playoffs_rush_long = IntegerField(null=True)
    receiving_and_rushing_playoffs_rush_receive_td = IntegerField(null=True)
    receiving_and_rushing_playoffs_rush_td = IntegerField(null=True)
    receiving_and_rushing_playoffs_rush_yds = IntegerField(null=True)
    receiving_and_rushing_playoffs_rush_yds_per_att = FloatField(null=True)
    receiving_and_rushing_playoffs_rush_yds_per_g = FloatField(null=True)
    receiving_and_rushing_playoffs_targets = IntegerField(null=True)
    receiving_and_rushing_playoffs_team = CharField(null=True)
    receiving_and_rushing_playoffs_yds_from_scrimmage = IntegerField(null=True)
    receiving_and_rushing_playoffs_year_id = IntegerField(null=True)
    receiving_and_rushing_pos = CharField(null=True)
    receiving_and_rushing_rec = IntegerField(null=True)
    receiving_and_rushing_rec_long = IntegerField(null=True)
    receiving_and_rushing_rec_per_g = FloatField(null=True)
    receiving_and_rushing_rec_td = IntegerField(null=True)
    receiving_and_rushing_rec_yds = IntegerField(null=True)
    receiving_and_rushing_rec_yds_per_g = FloatField(null=True)
    receiving_and_rushing_rec_yds_per_rec = FloatField(null=True)
    receiving_and_rushing_rush_att = IntegerField(null=True)
    receiving_and_rushing_rush_att_per_g = FloatField(null=True)
    receiving_and_rushing_rush_long = IntegerField(null=True)
    receiving_and_rushing_rush_receive_td = IntegerField(null=True)
    receiving_and_rushing_rush_td = IntegerField(null=True)
    receiving_and_rushing_rush_yds = IntegerField(null=True)
    receiving_and_rushing_rush_yds_per_att = FloatField(null=True)
    receiving_and_rushing_rush_yds_per_g = FloatField(null=True)
    receiving_and_rushing_targets = IntegerField(null=True)
    receiving_and_rushing_team = CharField(null=True)
    receiving_and_rushing_uniform_number = IntegerField(null=True)
    receiving_and_rushing_yds_from_scrimmage = IntegerField(null=True)
    receiving_and_rushing_year_id = CharField(null=True)
    returns_age = IntegerField(null=True)
    returns_all_purpose_yds = IntegerField(null=True)
    returns_av = IntegerField(null=True)
    returns_g = IntegerField(null=True)
    returns_gs = IntegerField(null=True)
    returns_kick_ret = IntegerField(null=True)
    returns_kick_ret_long = IntegerField(null=True)
    returns_kick_ret_td = IntegerField(null=True)
    returns_kick_ret_yds = IntegerField(null=True)
    returns_kick_ret_yds_per_ret = FloatField(null=True)
    returns_playoffs_age = IntegerField(null=True)
    returns_playoffs_all_purpose_yds = IntegerField(null=True)
    returns_playoffs_g = IntegerField(null=True)
    returns_playoffs_gs = IntegerField(null=True)
    returns_playoffs_kick_ret = IntegerField(null=True)
    returns_playoffs_kick_ret_long = IntegerField(null=True)
    returns_playoffs_kick_ret_td = IntegerField(null=True)
    returns_playoffs_kick_ret_yds = IntegerField(null=True)
    returns_playoffs_kick_ret_yds_per_ret = FloatField(null=True)
    returns_playoffs_pos = CharField(null=True)
    returns_playoffs_punt_ret = IntegerField(null=True)
    returns_playoffs_punt_ret_long = IntegerField(null=True)
    returns_playoffs_punt_ret_td = IntegerField(null=True)
    returns_playoffs_punt_ret_yds = IntegerField(null=True)
    returns_playoffs_punt_ret_yds_per_ret = FloatField(null=True)
    returns_playoffs_team = CharField(null=True)
    returns_playoffs_year_id = IntegerField(null=True)
    returns_pos = CharField(null=True)
    returns_punt_ret = IntegerField(null=True)
    returns_punt_ret_long = IntegerField(null=True)
    returns_punt_ret_td = IntegerField(null=True)
    returns_punt_ret_yds = IntegerField(null=True)
    returns_punt_ret_yds_per_ret = FloatField(null=True)
    returns_team = CharField(null=True)
    returns_uniform_number = IntegerField(null=True)
    returns_year_id = CharField(null=True)
    scoring_age = IntegerField(null=True)
    scoring_alltd = IntegerField(null=True)
    scoring_av = IntegerField(null=True)
    scoring_ditd = IntegerField(null=True)
    scoring_fgm = IntegerField(null=True)
    scoring_frtd = IntegerField(null=True)
    scoring_g = IntegerField(null=True)
    scoring_gs = IntegerField(null=True)
    scoring_krtd = IntegerField(null=True)
    scoring_otd = IntegerField(null=True)
    scoring_playoffs_age = IntegerField(null=True)
    scoring_playoffs_alltd = IntegerField(null=True)
    scoring_playoffs_ditd = IntegerField(null=True)
    scoring_playoffs_fgm = IntegerField(null=True)
    scoring_playoffs_frtd = IntegerField(null=True)
    scoring_playoffs_g = IntegerField(null=True)
    scoring_playoffs_gs = IntegerField(null=True)
    scoring_playoffs_krtd = IntegerField(null=True)
    scoring_playoffs_otd = IntegerField(null=True)
    scoring_playoffs_points_per_g = IntegerField(null=True)
    scoring_playoffs_pos = CharField(null=True)
    scoring_playoffs_prtd = IntegerField(null=True)
    scoring_playoffs_rectd = IntegerField(null=True)
    scoring_playoffs_rushtd = IntegerField(null=True)
    scoring_playoffs_safety_md = IntegerField(null=True)
    scoring_playoffs_scoring = IntegerField(null=True)
    scoring_playoffs_team = CharField(null=True)
    scoring_playoffs_two_pt_md = IntegerField(null=True)
    scoring_playoffs_xpm = IntegerField(null=True)
    scoring_playoffs_year_id = IntegerField(null=True)
    scoring_points_per_g = IntegerField(null=True)
    scoring_pos = CharField(null=True)
    scoring_prtd = IntegerField(null=True)
    scoring_rectd = IntegerField(null=True)
    scoring_rushtd = IntegerField(null=True)
    scoring_safety_md = IntegerField(null=True)
    scoring_scoring = IntegerField(null=True)
    scoring_team = CharField(null=True)
    scoring_two_pt_md = IntegerField(null=True)
    scoring_uniform_number = IntegerField(null=True)
    scoring_xpm = IntegerField(null=True)
    scoring_year_id = CharField(null=True)

    class Meta:
        db_table = 'player_seasons'


class Ratings(BaseModel):
    name = CharField()
    release_date = DateField()

    class Meta:
        db_table = 'ratings'


class HofPlayers(BaseModel):
    rk = IntegerField(db_column='Rk', null=True)
    career_av = IntegerField(db_column='career_AV', null=True)
    first_team_all_pros = IntegerField(null=True)
    games = IntegerField(null=True)
    inducted = IntegerField(null=True)
    name = CharField(null=True)
    passing_attempts = IntegerField(null=True)
    passing_completions = IntegerField(null=True)
    passing_interceptions = IntegerField(null=True)
    passing_long = IntegerField(null=True)
    passing_tds = IntegerField(null=True)
    passing_yards = IntegerField(null=True)
    played_from = IntegerField(null=True)
    played_to = IntegerField(null=True)
    position = CharField(null=True)
    pro_bowls = IntegerField(null=True)
    receiving_long = IntegerField(null=True)
    receiving_tds = IntegerField(null=True)
    receiving_yards = IntegerField(null=True)
    receptions = IntegerField(null=True)
    rushing_attempts = IntegerField(null=True)
    rushing_long = IntegerField(null=True)
    rushing_tds = IntegerField(null=True)
    rushing_yards = IntegerField(null=True)
    sacked = IntegerField(null=True)
    sacked_yards = IntegerField(null=True)
    starts = IntegerField(null=True)

    class Meta:
        db_table = 'hof_players'


class Madden(BaseModel):
    acceleration = IntegerField(null=True)
    agility = IntegerField(null=True)
    awareness = IntegerField(null=True)
    breaktackle = IntegerField(null=True)
    carrying = IntegerField(null=True)
    catching = IntegerField(null=True)
    firstname = CharField()
    jerseynum = IntegerField()
    jumping = IntegerField(null=True)
    kickaccuracy = IntegerField(null=True)
    kickpower = IntegerField(null=True)
    lastname = CharField()
    overallrating = IntegerField()
    passblock = IntegerField(null=True)
    position = CharField()
    runblock = IntegerField(null=True)
    speed = IntegerField(null=True)
    strength = IntegerField(null=True)
    tackle = IntegerField(null=True)
    throwaccuracy = IntegerField(null=True)
    throwpower = IntegerField(null=True)

    class Meta:
        db_table = 'madden'


class MaddenRatings(BaseModel):
    acceleration = IntegerField(null=True)
    agility = IntegerField(null=True)
    awareness = IntegerField(null=True)
    breaktackle = IntegerField(null=True)
    carrying = IntegerField(null=True)
    catching = IntegerField(null=True)
    firstname = CharField()
    jerseynum = IntegerField()
    jumping = IntegerField(null=True)
    kickaccuracy = IntegerField(null=True)
    kickpower = IntegerField(null=True)
    lastname = CharField()
    madden_rating = PrimaryKeyField(db_column='madden_rating_id')
    overallrating = IntegerField()
    passblock = IntegerField(null=True)
    position = CharField()
    runblock = IntegerField(null=True)
    speed = IntegerField(null=True)
    strength = IntegerField(null=True)
    tackle = IntegerField(null=True)
    team = CharField()
    throwaccuracy = IntegerField(null=True)
    throwpower = IntegerField(null=True)
    year = IntegerField()

    class Meta:
        db_table = 'madden_ratings'


class MockDraftPicks(BaseModel):
    mock_draft = IntegerField(db_column='mock_draft_id')
    mock_draft_pick = PrimaryKeyField(db_column='mock_draft_pick_id')
    name = CharField(null=True)
    position = CharField(null=True)
    rank = IntegerField()
    school = CharField(null=True)
    team = CharField(null=True)
    trade = CharField(null=True)

    class Meta:
        db_table = 'mock_draft_picks'


class MockDrafts(BaseModel):
    date = DateField(null=True)
    mock_draft = PrimaryKeyField(db_column='mock_draft_id')
    mocker = IntegerField(db_column='mocker_id', null=True)
    source = TextField(null=True)
    source_file = TextField(null=True)

    class Meta:
        db_table = 'mock_drafts'


class Mockers(BaseModel):
    email = CharField(null=True)
    mocker = PrimaryKeyField(db_column='mocker_id')
    name = CharField(null=True)
    publication = CharField(null=True)
    twitter = CharField(null=True)

    class Meta:
        db_table = 'mockers'


class NepMadden2005(BaseModel):
    acceleration = IntegerField(null=True)
    agility = IntegerField(null=True)
    awareness = IntegerField(null=True)
    breaktackle = IntegerField(null=True)
    carrying = IntegerField(null=True)
    catching = IntegerField(null=True)
    firstname = CharField()
    jerseynum = IntegerField()
    jumping = IntegerField(null=True)
    kickaccuracy = IntegerField(null=True)
    kickpower = IntegerField(null=True)
    lastname = CharField()
    overallrating = IntegerField()
    passblock = IntegerField(null=True)
    position = CharField()
    runblock = IntegerField(null=True)
    speed = IntegerField(null=True)
    strength = IntegerField(null=True)
    tackle = IntegerField(null=True)
    throwaccuracy = IntegerField(null=True)
    throwpower = IntegerField(null=True)

    class Meta:
        db_table = 'nep_madden_2005'


class Salary(BaseModel):
    cap = DecimalField(null=True)
    name = CharField()
    position = CharField()
    roster_bonus = DecimalField(null=True)
    salary = DecimalField(null=True)
    salary = PrimaryKeyField(db_column='salary_id')
    signing_bonus = DecimalField(null=True)
    team = CharField()
    year = IntegerField()

    class Meta:
        db_table = 'salary'


class SalaryData(BaseModel):
    name = CharField(db_column='Name')
    pos = CharField(db_column='POS')
    _2006_cap = DecimalField(db_column='_2006_Cap', null=True)
    _2006_rb = DecimalField(db_column='_2006_RB', null=True)
    _2006_sb = DecimalField(db_column='_2006_SB', null=True)
    _2006_salary = DecimalField(db_column='_2006_Salary', null=True)
    _2007_cap = DecimalField(db_column='_2007_Cap', null=True)
    _2007_rb = DecimalField(db_column='_2007_RB', null=True)
    _2007_sb = DecimalField(db_column='_2007_SB', null=True)
    _2007_salary = DecimalField(db_column='_2007_Salary', null=True)
    _2008_cap = DecimalField(db_column='_2008_Cap', null=True)
    _2008_rb = DecimalField(db_column='_2008_RB', null=True)
    _2008_sb = DecimalField(db_column='_2008_SB', null=True)
    _2008_salary = DecimalField(db_column='_2008_Salary', null=True)
    _2009_cap = DecimalField(db_column='_2009_Cap', null=True)
    _2009_rb = DecimalField(db_column='_2009_RB', null=True)
    _2009_sb = DecimalField(db_column='_2009_SB', null=True)
    _2009_salary = DecimalField(db_column='_2009_Salary', null=True)
    _2010_cap = DecimalField(db_column='_2010_Cap', null=True)
    _2010_rb = DecimalField(db_column='_2010_RB', null=True)
    _2010_sb = DecimalField(db_column='_2010_SB', null=True)
    _2010_salary = DecimalField(db_column='_2010_Salary', null=True)
    _2011_cap = DecimalField(db_column='_2011_Cap', null=True)
    _2011_rb = DecimalField(db_column='_2011_RB', null=True)
    _2011_sb = DecimalField(db_column='_2011_SB', null=True)
    _2011_salary = DecimalField(db_column='_2011_Salary', null=True)
    _2012_cap = DecimalField(db_column='_2012_Cap', null=True)
    _2012_rb = DecimalField(db_column='_2012_RB', null=True)
    _2012_sb = DecimalField(db_column='_2012_SB', null=True)
    _2012_salary = DecimalField(db_column='_2012_Salary', null=True)
    _2013_cap = DecimalField(db_column='_2013_Cap', null=True)
    _2013_rb = DecimalField(db_column='_2013_RB', null=True)
    _2013_sb = DecimalField(db_column='_2013_SB', null=True)
    _2013_salary = DecimalField(db_column='_2013_Salary', null=True)
    _2014_cap = DecimalField(db_column='_2014_Cap', null=True)
    _2014_rb = DecimalField(db_column='_2014_RB', null=True)
    _2014_sb = DecimalField(db_column='_2014_SB', null=True)
    _2014_salary = DecimalField(db_column='_2014_Salary', null=True)
    _2015_cap = DecimalField(db_column='_2015_Cap', null=True)
    _2015_rb = DecimalField(db_column='_2015_RB', null=True)
    _2015_sb = DecimalField(db_column='_2015_SB', null=True)
    _2015_salary = DecimalField(db_column='_2015_Salary', null=True)
    _2016_cap = DecimalField(db_column='_2016_Cap', null=True)
    _2016_rb = DecimalField(db_column='_2016_RB', null=True)
    _2016_sb = DecimalField(db_column='_2016_SB', null=True)
    _2016_salary = DecimalField(db_column='_2016_Salary', null=True)
    _2017_cap = DecimalField(db_column='_2017_Cap', null=True)
    _2017_rb = DecimalField(db_column='_2017_RB', null=True)
    _2017_sb = DecimalField(db_column='_2017_SB', null=True)
    _2017_salary = DecimalField(db_column='_2017_Salary', null=True)
    _2018_cap = DecimalField(db_column='_2018_Cap', null=True)
    _2018_rb = DecimalField(db_column='_2018_RB', null=True)
    _2018_sb = DecimalField(db_column='_2018_SB', null=True)
    _2018_salary = DecimalField(db_column='_2018_Salary', null=True)
    salary_data = PrimaryKeyField(db_column='salary_data_id')
    team = CharField()

    class Meta:
        db_table = 'salary_data'


class SalaryIn(BaseModel):
    name = CharField(db_column='Name')
    pos = CharField(db_column='POS')
    _2006_cap = DecimalField(db_column='_2006_Cap', null=True)
    _2006_rb = DecimalField(db_column='_2006_RB', null=True)
    _2006_sb = DecimalField(db_column='_2006_SB', null=True)
    _2006_salary = DecimalField(db_column='_2006_Salary', null=True)
    _2007_cap = DecimalField(db_column='_2007_Cap', null=True)
    _2007_rb = DecimalField(db_column='_2007_RB', null=True)
    _2007_sb = DecimalField(db_column='_2007_SB', null=True)
    _2007_salary = DecimalField(db_column='_2007_Salary', null=True)
    _2008_cap = DecimalField(db_column='_2008_Cap', null=True)
    _2008_rb = DecimalField(db_column='_2008_RB', null=True)
    _2008_sb = DecimalField(db_column='_2008_SB', null=True)
    _2008_salary = DecimalField(db_column='_2008_Salary', null=True)
    _2009_cap = DecimalField(db_column='_2009_Cap', null=True)
    _2009_rb = DecimalField(db_column='_2009_RB', null=True)
    _2009_sb = DecimalField(db_column='_2009_SB', null=True)
    _2009_salary = DecimalField(db_column='_2009_Salary', null=True)
    _2010_cap = DecimalField(db_column='_2010_Cap', null=True)
    _2010_rb = DecimalField(db_column='_2010_RB', null=True)
    _2010_sb = DecimalField(db_column='_2010_SB', null=True)
    _2010_salary = DecimalField(db_column='_2010_Salary', null=True)
    _2011_cap = DecimalField(db_column='_2011_Cap', null=True)
    _2011_rb = DecimalField(db_column='_2011_RB', null=True)
    _2011_sb = DecimalField(db_column='_2011_SB', null=True)
    _2011_salary = DecimalField(db_column='_2011_Salary', null=True)
    _2012_cap = DecimalField(db_column='_2012_Cap', null=True)
    _2012_rb = DecimalField(db_column='_2012_RB', null=True)
    _2012_sb = DecimalField(db_column='_2012_SB', null=True)
    _2012_salary = DecimalField(db_column='_2012_Salary', null=True)
    _2013_cap = DecimalField(db_column='_2013_Cap', null=True)
    _2013_rb = DecimalField(db_column='_2013_RB', null=True)
    _2013_sb = DecimalField(db_column='_2013_SB', null=True)
    _2013_salary = DecimalField(db_column='_2013_Salary', null=True)
    _2014_cap = DecimalField(db_column='_2014_Cap', null=True)
    _2014_rb = DecimalField(db_column='_2014_RB', null=True)
    _2014_sb = DecimalField(db_column='_2014_SB', null=True)
    _2014_salary = DecimalField(db_column='_2014_Salary', null=True)
    _2015_cap = DecimalField(db_column='_2015_Cap', null=True)
    _2015_rb = DecimalField(db_column='_2015_RB', null=True)
    _2015_sb = DecimalField(db_column='_2015_SB', null=True)
    _2015_salary = DecimalField(db_column='_2015_Salary', null=True)
    _2016_cap = DecimalField(db_column='_2016_Cap', null=True)
    _2016_rb = DecimalField(db_column='_2016_RB', null=True)
    _2016_sb = DecimalField(db_column='_2016_SB', null=True)
    _2016_salary = DecimalField(db_column='_2016_Salary', null=True)
    _2017_cap = DecimalField(db_column='_2017_Cap', null=True)
    _2017_rb = DecimalField(db_column='_2017_RB', null=True)
    _2017_sb = DecimalField(db_column='_2017_SB', null=True)
    _2017_salary = DecimalField(db_column='_2017_Salary', null=True)
    _2018_cap = DecimalField(db_column='_2018_Cap', null=True)
    _2018_rb = DecimalField(db_column='_2018_RB', null=True)
    _2018_sb = DecimalField(db_column='_2018_SB', null=True)
    _2018_salary = DecimalField(db_column='_2018_Salary', null=True)

    class Meta:
        db_table = 'salary_in'


class EspnRosterPlayer(BaseModel):
    espn_roster_player = PrimaryKeyField(db_column='espn_roster_player_id')
    age = CharField()
    college = CharField()
    exp = IntegerField()
    ht = IntegerField()
    name = CharField()
    no = IntegerField()
    pos = CharField()
    team = CharField()
    wt = IntegerField()

    class Meta:
        db_table = 'espn_roster_players'


class EspnDepthPosition(BaseModel):
    team = CharField()
    second = CharField()
    third = CharField()
    fourth = CharField()
    espn_depth_position = PrimaryKeyField(db_column='espn_depth_position_id')
    formation = CharField()
    position = CharField()
    starter = CharField()

    class Meta:
        db_table = 'espn_depth_positions'
