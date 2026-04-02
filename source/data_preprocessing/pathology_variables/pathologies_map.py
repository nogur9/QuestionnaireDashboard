from source.data_preprocessing.pathology_variables.pathology_variable import PathologyVariable
from source.data_preprocessing.pathology_variables.pathologies_pool import (suicidal_behavior_intake, suicide_attempt_intake, nssi_intake, \
    self_harm_intake, modcon_target, survival_target, suicidal_behavior_time2, nssi_time2, suicidal_attempt_time2, \
    suicidal_ideation_life_intake, suicidal_ideation_time2, nssi_cols, suicidal_ideation_cols, suicidal_attempt_cols,
                                                                            suicidal_behavior_cols)


PathologiesMap = {
    "suicidal_behavior_intake": PathologyVariable('suicidal_behavior', suicidal_behavior_cols),
    "suicide_attempt_intake": PathologyVariable('suicide_attempt', suicidal_attempt_cols),
    "NSSI_intake": PathologyVariable('NSSI', nssi_cols),
    "self_harm_intake": PathologyVariable('self_harm', self_harm_intake,
                                            only_intake_evaluation=True),
    "suicidal_ideation_intake": PathologyVariable('suicidal_ideation',suicidal_ideation_cols),

    "MODCON": PathologyVariable('MODCON', modcon_target),
    "survival_analysis": PathologyVariable('survival_analysis', survival_target,
                                            only_follow_up_evaluation=True),
    "suicidal_behavior_follow-up": PathologyVariable('suicidal_behavior', suicidal_behavior_cols),
    "suicidal_attempt_follow-up": PathologyVariable('suicide_attempt', suicidal_attempt_cols),
    "NSSI_follow-up": PathologyVariable('NSSI', nssi_cols),
    "suicidal_ideation_follow_up": PathologyVariable('suicidal_ideation',suicidal_ideation_cols),
}



PathologiesNames = {

    'suicidal_ideation':  [PathologiesMap['suicidal_ideation_intake']], #PathologiesMap['suicidal_ideation_follow_up']],
    'suicidal_behavior': [PathologiesMap['suicidal_behavior_intake']], #PathologiesMap['suicidal_behavior_follow-up']],
    'suicide_attempt': [PathologiesMap['suicide_attempt_intake']], #PathologiesMap['suicidal_attempt_follow-up']],

    'NSSI': [PathologiesMap['NSSI_intake']], #PathologiesMap['NSSI_follow-up']],


    "self_harm_intake": [PathologiesMap['self_harm_intake']],
    "MODCON": [PathologiesMap['MODCON']],
    "survival_analysis": [PathologiesMap['survival_analysis']],


}