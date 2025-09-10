from typing import List
from source.consts.enums import ScoringMethod, UniqueScoringMethod, C_SSRS_Scoring
from source.consts.scores.exceptions import CSSRS, Null_Scores, unknown, missing_scores, SCI, Unique_Scores
from source.scores.score_utils_loader import ScoreUtilsLoader
from source.utils.info_objects import ScoresList, ScoringInfo

class ScoresLoader:

    def __init__(self):
        self.scores_utils = ScoreUtilsLoader()
        self.scores_list = None

    def load(self):
        scores_collection = self._get_scores_list()
        scores_collection = self.scores_utils.duplicate_mother_and_father(scores_collection, score_d_type='scores_info')
        extra_scores = self._add_extra_scores()
        scores_list = scores_collection + extra_scores
        self.scores_list = ScoresList(scores_list)
        return self.scores_list

    def _get_scores_list(self) -> List[ScoringInfo]:
        return [

        ScoringInfo(
            questionnaire_name = 'mfq_short',
            columns = self.scores_utils.scores_columns['mfq_short'], # These questions don't participate in the scores                                                               # 34, 35, 36, 37
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            require_step_adj = True,
            ** self.scores_utils.add_min_max_scores('mfq_short')
        ),
        ScoringInfo(
            questionnaire_name = 'siq',
            columns=self.scores_utils.scores_columns['siq'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('siq')
        ),
        ScoringInfo(
            questionnaire_name = 'sdq',
            columns=self.scores_utils.scores_columns['sdq'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items['sdq'],
            clusters = self.scores_utils.clusters['sdq'],
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('sdq')
        ),
        ScoringInfo(
            questionnaire_name = 'sciafca',
            columns=self.scores_utils.scores_columns['sciafca'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('sciafca')
        ),
        ScoringInfo(
            questionnaire_name = 'scared',
            columns=self.scores_utils.scores_columns['scared'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            require_step_adj = True,
            ** self.scores_utils.add_min_max_scores('scared')
        ),
        ScoringInfo(
            questionnaire_name = 'sas',
            columns=self.scores_utils.scores_columns['sas'],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('sas')
        ),
        ScoringInfo(
            questionnaire_name = 'ecrrc',   # should be ecr_rc
            columns=self.scores_utils.scores_columns['ecrrc'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items['ecrrc'],
            clusters = self.scores_utils.clusters['ecrrc'],
            need_clarification = True,
            **self.scores_utils.add_min_max_scores('ecrrc')
        ),
        ScoringInfo(
            questionnaire_name = 'aris',
            columns=self.scores_utils.scores_columns['aris'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('aris')
        ),
        ScoringInfo(
            questionnaire_name = 'mast',
            columns=self.scores_utils.scores_columns['mast'],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters = self.scores_utils.clusters['mast'],
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('mast')
        ),
        ScoringInfo(
            questionnaire_name = 'athens',
            columns=self.scores_utils.scores_columns['athens'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            require_step_adj=True,
            ** self.scores_utils.add_min_max_scores('athens')
        ),

        #  Check if my column name are correct
        ScoringInfo(
            questionnaire_name = 'piu',
            columns=self.scores_utils.scores_columns['piu'],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters ={},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores('piu')
        ),
        ScoringInfo(
            questionnaire_name = 'cyberbulling',
            columns=self.scores_utils.scores_columns['cyberbulling'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters ={},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores('cyberbulling')
        ),
        ScoringInfo(
            questionnaire_name = 'erqca',
            columns=self.scores_utils.scores_columns['erqca'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = self.scores_utils.clusters['erqca'],
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('erqca')
        ),
        ScoringInfo(
            questionnaire_name = 'ders',
            columns=self.scores_utils.scores_columns['ders'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items['ders'],
            clusters = self.scores_utils.clusters['ders'],
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('ders')
        ),
        ScoringInfo(
            questionnaire_name = 'wai',
            columns=self.scores_utils.scores_columns['wai'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items['wai'],
            clusters = self.scores_utils.clusters['wai'],
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('wai')
        ),
        ScoringInfo(
            questionnaire_name = 'estimation_and_satisfaction',
            columns=self.scores_utils.scores_columns['estimation_and_satisfaction'],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            require_step_adj = True,
            ** self.scores_utils.add_min_max_scores('satis')
        ),

        ScoringInfo(
            questionnaire_name = 'cts_c',
            columns = self.scores_utils.scores_columns['cts_c'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('cts_c')
        ),
        ScoringInfo(
            questionnaire_name = 'dshi_pre', # separate into pre & post
            columns=self.scores_utils.scores_columns['dshi_pre'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores('dshi_pre')
        ),
        ScoringInfo(
            questionnaire_name='dshi_post',  # separate into pre & post
            columns=self.scores_utils.scores_columns['dshi_post'],
            aggregation_function=ScoringMethod.SUM,
            reversed_columns=[],
            clusters={},
            need_clarification=True,
            **self.scores_utils.add_min_max_scores('dshi_post')
        ),
        ScoringInfo(
            questionnaire_name = 'inq',
            columns=self.scores_utils.scores_columns['inq'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items['inq'],
            clusters = self.scores_utils.clusters['inq'],
            need_clarification = False,
            **self.scores_utils.add_min_max_scores('inq')
        ),
        ScoringInfo(
            questionnaire_name = 'swan_m', # I need to define this scoring method
            columns=self.scores_utils.scores_columns['swan_m'],
            aggregation_function = UniqueScoringMethod.SWAN_SCORING,
            reversed_columns = [],
            clusters = self.scores_utils.clusters['swan_m'],
            need_clarification = True,
            **self.scores_utils.add_min_max_scores('swan_m')
        ),
        ScoringInfo(
            questionnaire_name = 'scip_m',
            columns=self.scores_utils.scores_columns['scip_m'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('scip_m')
        ),
        ScoringInfo(
            questionnaire_name = 'sdq_parents_m', # Need help with the scoring
            columns=self.scores_utils.scores_columns['sdq_parents_m'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores('sdq_parents_m')
        ),
        ScoringInfo(
            questionnaire_name = 'ders_p_m',
            columns=self.scores_utils.scores_columns['ders_p_m'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('ders_p_m')
        ),
        ScoringInfo(
            questionnaire_name = 'erq_m',
            columns=self.scores_utils.scores_columns['erq_m'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = self.scores_utils.clusters['erq_m'],
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('erq_m')
        ),
        ScoringInfo(
            questionnaire_name = 'arippps_m',
            columns=self.scores_utils.scores_columns['arippps_m'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('arippps_m')
        ),
        ScoringInfo(
            questionnaire_name = 'ecr_m',  # clusters - anxiety - 1 - 18,
                                           # avoidance - 19 -36,
                                           # and there are reverse
            columns=self.scores_utils.scores_columns['ecr_m'],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores('ecr_m')
        ),
        ScoringInfo(
            questionnaire_name = 'cts_m',
            columns=self.scores_utils.scores_columns['cts_m'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('cts_m')
        ),
        ScoringInfo(
            questionnaire_name = 'moas_m',  # Oren didn't find how to calculate
            columns=self.scores_utils.scores_columns['moas_m'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores('moas_m')
        ),
        ScoringInfo(
            questionnaire_name = 'wai_immirisk_clin',
            columns=self.scores_utils.scores_columns['wai_immirisk_clin'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('wai_immirisk_clin')
        ),
        ScoringInfo(
            questionnaire_name = 'trqsfmarisclin',
            columns=self.scores_utils.scores_columns['trqsfmarisclin'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('trqsfmarisclin')
        ),
        ScoringInfo(
            questionnaire_name = 'trqsfmaris_stu',
            columns=self.scores_utils.scores_columns['trqsfmaris_stu'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items['trqsfmaris_stu'],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('trqsfmaris_stu')
        ),
        ScoringInfo(
            questionnaire_name = 'cgi_s_clin',
            columns=self.scores_utils.scores_columns['cgi_s_clin'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('cgi_s_clin')
        ),
        ScoringInfo(
            questionnaire_name = 'cps_clin',  # don't know how to calc
            columns=self.scores_utils.scores_columns['cps_clin'],
            aggregation_function = UniqueScoringMethod.SPC_CLIN_SCORING,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores('cps_clin')
        ),
        ScoringInfo(
            questionnaire_name = 'cdrsr_clin',  # review the name
                                                # remove un-scored columns, remove sum column
            columns=self.scores_utils.scores_columns['cdrsr_clin'],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores('cdrsr_clin')
        )
]

    def _add_missing_implementation_scores(self):
        missing_scores_objs = []
        for questionnaire_name in missing_scores + SCI:
            missing_scores_objs.append(
                ScoringInfo(
                    questionnaire_name = questionnaire_name,  # review the name
                                                        # remove un-scored columns, remove sum column
                    columns=[],
                    aggregation_function = ScoringMethod.Missing_Implementation_Scoring,
                    reversed_columns = [],
                    clusters = {},
                    need_clarification = False,
                    )
            )
        return missing_scores_objs


    def _add_unique_scores(self):
        unique_scores_objs = []
        for questionnaire_name in Unique_Scores:
            unique_scores_objs.append(
                ScoringInfo(
                    questionnaire_name = questionnaire_name,
                    columns=[],
                    aggregation_function = UniqueScoringMethod.from_questionnaire(questionnaire_name),
                    reversed_columns = [],
                    clusters = {},
                    need_clarification = False,
                    )
            )
        return unique_scores_objs


    def _add_null_scores(self):
        null_scores_objs = []
        for questionnaire_name in Null_Scores + unknown:
            null_scores_objs.append(
                ScoringInfo(
                    questionnaire_name = questionnaire_name,
                    columns=[],
                    aggregation_function = ScoringMethod.No_Scoring,
                    reversed_columns = [],
                    clusters = {},
                    need_clarification = False,
                    )
            )
        return null_scores_objs


    def _add_c_ssrs_scores(self):
        c_ssrs_scores_objs = []
        for questionnaire_name in CSSRS:
            c_ssrs_scores_objs.append(
                ScoringInfo(
                    questionnaire_name = questionnaire_name,
                    columns=[],
                    aggregation_function = C_SSRS_Scoring.from_questionnaire(questionnaire_name),
                    reversed_columns = [],
                    clusters = {},
                    need_clarification = False,
                    )
            )
        return c_ssrs_scores_objs


    def _add_extra_scores(self):
        extra_scores = (
            self._add_null_scores()) + \
            self._add_c_ssrs_scores() + \
            self._add_unique_scores() + \
            self._add_missing_implementation_scores()

        return extra_scores



if __name__ == "__main__":
    sl = ScoresLoader()
    results = sl.load()