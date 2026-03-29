from typing import List

from source.consts.enums import ScoringMethod, UniqueScoringMethod, C_SSRS_Scoring
from source.consts.scores.exceptions import Null_Scores, unknown, missing_scores, SCI, Unique_Scores
from source.consts.questionnaires_names import get_questionnaire

from source.data_etl.questionnaires_metadata.info_objects import ScoresList, ScoringInfo
from source.data_etl.questionnaires_metadata.stepped_care.scores.score_utils_loader import ScoreUtilsLoader
from source.consts.questionnaires_names import Questionnaire

class ScoresLoader:

    def __init__(self):
        self.scores_utils = ScoreUtilsLoader()
        self.scores_list = None

    def load(self):
        scores_collection = self._get_scores_list()
        #scores_collection = self.scores_utils.duplicate_mother_and_father(scores_collection, score_d_type='scores_info')
        extra_scores = self._add_extra_scores()
        scores_list = scores_collection + extra_scores
        self.scores_list = ScoresList(scores_list)
        return self.scores_list

    def _get_scores_list(self) -> List[ScoringInfo]:
        # Helper: map questionnaire identifier to the key used in scores_columns
        def _key(name: str):
            try:
                return get_questionnaire(name)
            except KeyError:
                return name

        return [



        ScoringInfo(
            questionnaire_name = Questionnaire.ATHENS, # renamed from - athens to ATHENS
            columns=self.scores_utils.scores_columns[Questionnaire.ATHENS],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            require_step_adj=True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.ATHENS)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.ARI_P_M, # renamed from - arippps_m to ARI_P_M
            columns=self.scores_utils.scores_columns[Questionnaire.ARI_P_M],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            ** self.scores_utils.add_min_max_scores(Questionnaire.ARI_P_M)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.ARI_S, # renamed from - aris to ARI_S
            columns=self.scores_utils.scores_columns[Questionnaire.ARI_S],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            ** self.scores_utils.add_min_max_scores(Questionnaire.ARI_S)
        ),


        ScoringInfo(
            questionnaire_name = Questionnaire.cdrsr_clin,  # review the name
                                                # remove un-scored columns, remove sum column
            columns=self.scores_utils.scores_columns[Questionnaire.cdrsr_clin],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.cdrsr_clin)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.cgi_s_clin,
            columns=self.scores_utils.scores_columns[Questionnaire.cgi_s_clin],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification=True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.cgi_s_clin)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.cps_clin,  # don't know how to calc
            columns=self.scores_utils.scores_columns[Questionnaire.cps_clin],
            aggregation_function = UniqueScoringMethod.SPC_CLIN_SCORING,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.cps_clin)
        ),

        ScoringInfo(
            questionnaire_name=Questionnaire.c_ssrs_intake,
            columns=self.scores_utils.scores_columns[Questionnaire.c_ssrs_intake],
            aggregation_function=UniqueScoringMethod.C_SSRS_Scoring,
            reversed_columns=[],
            clusters=self.scores_utils.clusters[Questionnaire.c_ssrs_intake],
            min_score = 0, max_score = 1,
        ),

            ScoringInfo(
                questionnaire_name=Questionnaire.c_ssrs,
                columns=self.scores_utils.scores_columns[Questionnaire.c_ssrs],
                aggregation_function=UniqueScoringMethod.C_SSRS_Scoring,
                reversed_columns=[],
                clusters={},
                min_score = 0, max_score = 1
            ),

        ScoringInfo(
            questionnaire_name = Questionnaire.cyberbulling,
            columns=self.scores_utils.scores_columns[Questionnaire.cyberbulling],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters ={},
            ** self.scores_utils.add_min_max_scores(Questionnaire.cyberbulling)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.cts_m,
            columns=self.scores_utils.scores_columns[Questionnaire.cts_m],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.cts_m)
        ),

ScoringInfo(
            questionnaire_name = Questionnaire.cts_c, # missing in Oren's syntax
            columns = self.scores_utils.scores_columns[Questionnaire.cts_c],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.cts_c)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.dass_m,
            columns=self.scores_utils.scores_columns[Questionnaire.dass_m],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = self.scores_utils.clusters[Questionnaire.dass_m],
            ** self.scores_utils.add_min_max_scores(Questionnaire.dass_m)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.dshi_pre,
            columns=self.scores_utils.scores_columns[Questionnaire.dshi_pre],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            ** self.scores_utils.add_min_max_scores(Questionnaire.dshi_pre)
        ),
        ScoringInfo(
            questionnaire_name=Questionnaire.dshi_post,
            columns=self.scores_utils.scores_columns[Questionnaire.dshi_post],
            aggregation_function=ScoringMethod.SUM,
            reversed_columns=[],
            clusters={},
            **self.scores_utils.add_min_max_scores(Questionnaire.dshi_post)
        ),
            ScoringInfo(
                questionnaire_name=Questionnaire.ders,
                columns=self.scores_utils.scores_columns[Questionnaire.ders],
                aggregation_function=ScoringMethod.SUM,
                reversed_columns=self.scores_utils.reverse_items[Questionnaire.ders],
                clusters=self.scores_utils.clusters[Questionnaire.ders],
                **self.scores_utils.add_min_max_scores(Questionnaire.ders)
            ),

        # ScoringInfo(
        #     questionnaire_name = Questionnaire.ders_p_m,
        #     columns=self.scores_utils.scores_columns[Questionnaire.ders_p_m],
        #     aggregation_function = ScoringMethod.SUM,
        #     reversed_columns = [],
        #     clusters = {},
        #     ** self.scores_utils.add_min_max_scores(Questionnaire.ders_p_m)
        # ),
        #
        # ScoringInfo(
        #     questionnaire_name = Questionnaire.ders_p_f,
        #     columns=self.scores_utils.scores_columns[Questionnaire.ders_p_f],
        #     aggregation_function = ScoringMethod.SUM,
        #     reversed_columns = [],
        #     clusters = {},
        #     ** self.scores_utils.add_min_max_scores(Questionnaire.ders_p_f)
        # ),



        ScoringInfo(
            questionnaire_name = Questionnaire.ecr_f,  # clusters - anxiety - 1 - 18,
                                           # avoidance - 19 -36,
                                           # and there are reverse
            columns=self.scores_utils.scores_columns[Questionnaire.ecr_f],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters = {},
            #need_clarification=True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.ecr_f)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.ecr_m,  # clusters - anxiety - 1 - 18,
                                           # avoidance - 19 -36,
                                           # and there are reverse
            columns=self.scores_utils.scores_columns[Questionnaire.ecr_m],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters = {},
            need_clarification=True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.ecr_m)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.erq_m,
            columns=self.scores_utils.scores_columns[Questionnaire.erq_m],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = self.scores_utils.clusters[Questionnaire.erq_m],
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.erq_m)
        ),
            ScoringInfo(
                questionnaire_name=Questionnaire.estimation_and_satisfaction,  # check name - satis
                columns=self.scores_utils.scores_columns[Questionnaire.estimation_and_satisfaction],
                aggregation_function=ScoringMethod.AVERAGE,
                reversed_columns=[],
                clusters={},
                need_clarification=True,
                require_step_adj=True,
                **self.scores_utils.add_min_max_scores(Questionnaire.estimation_and_satisfaction)
            ),
            ScoringInfo(
            questionnaire_name = Questionnaire.erq_ca,  # renamed from - erqca to erq_ca
            columns=self.scores_utils.scores_columns[Questionnaire.erq_ca],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = self.scores_utils.clusters[Questionnaire.erq_ca],
            ** self.scores_utils.add_min_max_scores(Questionnaire.erq_ca)
        ),

            ScoringInfo(
                questionnaire_name=Questionnaire.erc_rc,  # renamed from - ecrrc  # should be ecr_rc
                columns=self.scores_utils.scores_columns[Questionnaire.erc_rc],
                aggregation_function=ScoringMethod.SUM,
                reversed_columns=self.scores_utils.reverse_items[Questionnaire.erc_rc],
                clusters=self.scores_utils.clusters[Questionnaire.erc_rc],
                need_clarification=True,
                **self.scores_utils.add_min_max_scores(Questionnaire.erc_rc)
            ),

        ScoringInfo(
            questionnaire_name = Questionnaire.inq,
            columns=self.scores_utils.scores_columns[Questionnaire.inq],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items[Questionnaire.inq],
            clusters = self.scores_utils.clusters[Questionnaire.inq],
            **self.scores_utils.add_min_max_scores(Questionnaire.inq)
        ),
            ScoringInfo(
                questionnaire_name=Questionnaire.mast,
                columns=self.scores_utils.scores_columns[Questionnaire.mast],
                aggregation_function=ScoringMethod.AVERAGE,
                reversed_columns=[],
                clusters=self.scores_utils.clusters[Questionnaire.mast],
                **self.scores_utils.add_min_max_scores(Questionnaire.mast)
            ),

            ScoringInfo(
                questionnaire_name=Questionnaire.maris_y_scars_clin,
                columns=self.scores_utils.scores_columns[Questionnaire.maris_y_scars_clin],
                aggregation_function=ScoringMethod.AVERAGE,
                reversed_columns=[],
                clusters={},
                need_clarification=True,
                **self.scores_utils.add_min_max_scores(Questionnaire.maris_y_scars_clin)
            ),

        ScoringInfo(
            questionnaire_name = Questionnaire.mfq, # renamed from - mfq_short \ mfq
            columns = self.scores_utils.scores_columns[Questionnaire.mfq], # These questions don't participate in the scores                                                               # 34, 35, 36, 37
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            require_step_adj = True,
            need_clarification=True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.mfq)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.moas_m,  # Oren didn't find how to calculate
            columns=self.scores_utils.scores_columns[Questionnaire.moas_m],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.moas_m)
        ),
        ScoringInfo( #  Check if my column name are correct
            questionnaire_name = Questionnaire.piu,
            columns=self.scores_utils.scores_columns[Questionnaire.piu],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters ={},
            ** self.scores_utils.add_min_max_scores(Questionnaire.piu)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.sci_mother,
            columns=self.scores_utils.scores_columns[Questionnaire.sci_mother],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            ** self.scores_utils.add_min_max_scores(Questionnaire.sci_mother)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.siq,
            columns=self.scores_utils.scores_columns[Questionnaire.siq],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            ** self.scores_utils.add_min_max_scores(Questionnaire.siq)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.sdq,
            columns=self.scores_utils.scores_columns[Questionnaire.sdq],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items[Questionnaire.sdq],
            clusters = self.scores_utils.clusters[Questionnaire.sdq],
            ** self.scores_utils.add_min_max_scores(Questionnaire.sdq)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.sci_af_ca, # renamed from - sciafca \ sci_af_ca
            columns=self.scores_utils.scores_columns[Questionnaire.sci_af_ca],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.sci_af_ca)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.scared,
            columns=self.scores_utils.scores_columns[Questionnaire.scared],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            require_step_adj = True,
            need_clarification=True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.scared)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.SAS, # renamed from - sas, SAS
            columns=self.scores_utils.scores_columns[Questionnaire.SAS],
            aggregation_function = ScoringMethod.AVERAGE,
            reversed_columns = [],
            clusters = {},
            ** self.scores_utils.add_min_max_scores(Questionnaire.SAS)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.swan_m, # I need to define this scoring method
            columns=self.scores_utils.scores_columns[Questionnaire.swan_m],
            aggregation_function = UniqueScoringMethod.SWAN_SCORING,
            reversed_columns = [],
            clusters = self.scores_utils.clusters[Questionnaire.swan_m],
            need_clarification = True,
            **self.scores_utils.add_min_max_scores(Questionnaire.swan_m)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.sdq_parents_m, # Need help with the scoring
            columns=self.scores_utils.scores_columns[Questionnaire.sdq_parents_m],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = [],
            clusters = {},
            need_clarification = True,
            min_score=0, max_score=10
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.trq_sf_maris_clin,
            columns=self.scores_utils.scores_columns[Questionnaire.trq_sf_maris_clin],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items[Questionnaire.trq_sf_maris_clin],
            clusters = {},
            ** self.scores_utils.add_min_max_scores(Questionnaire.trq_sf_maris_clin)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.trq_sf_maris_stu,
            columns=self.scores_utils.scores_columns[Questionnaire.trq_sf_maris_stu],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items[Questionnaire.trq_sf_maris_stu],
            clusters = {},
            need_clarification = False,
            ** self.scores_utils.add_min_max_scores(Questionnaire.trq_sf_maris_stu)
        ),
        ScoringInfo(
            questionnaire_name = Questionnaire.wai,
            columns=self.scores_utils.scores_columns[Questionnaire.wai],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items[Questionnaire.wai],
            clusters = self.scores_utils.clusters[Questionnaire.wai],
            ** self.scores_utils.add_min_max_scores(Questionnaire.wai)
        ),

        ScoringInfo(
            questionnaire_name = Questionnaire.wai_immirisk_clin,
            columns=self.scores_utils.scores_columns[Questionnaire.wai_immirisk_clin],
            aggregation_function = ScoringMethod.SUM,
            reversed_columns = self.scores_utils.reverse_items[Questionnaire.wai_immirisk_clin],
            clusters = {},
            need_clarification=True,
            ** self.scores_utils.add_min_max_scores(Questionnaire.wai_immirisk_clin)
        ),



            ########## up to here


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
        for questionnaire_name in Null_Scores : # + unknown
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

    #
    # def _add_c_ssrs_scores(self):
    #     c_ssrs_scores_objs = []
    #     for questionnaire_name in CSSRS:
    #         c_ssrs_scores_objs.append(
    #             ScoringInfo(
    #                 questionnaire_name = questionnaire_name,
    #                 columns=[],
    #                 aggregation_function = C_SSRS_Scoring.from_questionnaire(questionnaire_name),
    #                 reversed_columns = [],
    #                 clusters = {},
    #                 need_clarification = False,
    #                 )
    #         )
    #     return c_ssrs_scores_objs


    def _add_extra_scores(self):
        extra_scores = (self._add_null_scores())# + \
            # self._add_c_ssrs_scores() + \
            # self._add_unique_scores() + \
            # self._add_missing_implementation_scores()

        return extra_scores



if __name__ == "__main__":
    sl = ScoresLoader()
    results = sl.load()