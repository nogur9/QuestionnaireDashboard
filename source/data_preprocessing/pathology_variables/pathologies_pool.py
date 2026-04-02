
# Only intake evaluations

suicidal_behavior_intake = [
    'c_ssrs_t_11_life_clin',
    'c_ssrs_t_12_life_clin',
    'c_ssrs_t_13_life_clin',
    'c_ssrs_t_14_life_clin',
    'c_ssrs_t_15_life_clin',

    'c_ssrs_6_life', 'mfq_34', 'mfq_36', 'c_ssrs_6_2weeks',
    'c_ssrs_6_3month'
]

suicide_attempt_intake = [
    'mfq_36', 'mfq_34',
    'c_ssrs_t_11_life_clin',
    'c_ssrs_t_12_life_clin',
    'c_ssrs_t_13_life_clin',
    'chameleon_attempt_stu',
]

nssi_intake = [
    'c_ssrs_t_16_life_clin', 'mfq_35', 'mfq_37', 'chameleon_nssi_stu'
]

self_harm_intake = list(set(suicide_attempt_intake + nssi_intake + suicidal_behavior_intake))

# sub niches of suicide ideation
suicidal_ideation_2weeks_intake = [
    #'c_ssrs_t_2weeks_1_clin',
    'c_ssrs_t_2weeks_2_clin',
    'c_ssrs_t_2weeks_3_clin',
    'c_ssrs_t_2weeks_4_clin',
    'c_ssrs_t_2weeks_5_clin',

    'c_ssrs_1_2weeks',
    'c_ssrs_2_2weeks',
    'c_ssrs_3_2weeks',
    'c_ssrs_4_2weeks',
    'c_ssrs_5_2weeks',
]

suicidal_ideation_life_intake = [

    'c_ssrs_t_life_1_clin',
    'c_ssrs_t_life_2_clin',
    'c_ssrs_t_life_3_clin',
    'c_ssrs_t_life_4_clin',
    'c_ssrs_t_life_5_clin',

   # 'c_ssrs_t_2weeks_1_clin',
    'c_ssrs_t_2weeks_2_clin',
    'c_ssrs_t_2weeks_3_clin',
    'c_ssrs_t_2weeks_4_clin',
    'c_ssrs_t_2weeks_5_clin',

    'c_ssrs_1_life',
    'c_ssrs_2_life',
    'c_ssrs_3_life',
    'c_ssrs_4_life',
    'c_ssrs_5_life',

    'c_ssrs_1_2weeks',
    'c_ssrs_2_2weeks',
    'c_ssrs_3_2weeks',
    'c_ssrs_4_2weeks',
    'c_ssrs_5_2weeks',
    'chameleon_ideation_stu'

]



# Only Follow-up Evaluations

modcon_target = [
    'chameleon_attempt_stu',
    'chameleon_psychiatric_stu',
     'chameleon_suicide_er_stu',
     'mfq_36',
    #
    # 'c_ssrs_6',
    #  'c_ssrs_last_visit_6',
    # 'chameleon_behavior_stu',
    # 'suicidal_behavior_last_11_clin',
    # 'suicidal_behavior_last_12_clin',
    # 'suicidal_behavior_last_13_clin',
    # 'suicidal_behavior_last_14_clin',
    # 'suicidal_behavior_last_15_clin'
    ]

survival_target = [
    # 'c_ssrs_6',
    # 'c_ssrs_last_visit_6',
    'chameleon_attempt_stu',
    # 'chameleon_behavior_stu',
    'mfq_36',
    'chameleon_suicide_er_stu',
    'chameleon_psychiatric_stu',
    # 'suicidal_behavior_last_11_clin',
    # 'suicidal_behavior_last_12_clin',
    # 'suicidal_behavior_last_13_clin',
    # 'suicidal_behavior_last_14_clin',
    # 'suicidal_behavior_last_15_clin'
    ]

suicidal_behavior_time2 = [
    'suicidal_behavior_last_11_clin',
    'suicidal_behavior_last_12_clin',
    'suicidal_behavior_last_13_clin',
    'suicidal_behavior_last_14_clin',
    'suicidal_behavior_last_15_clin',

    'c_ssrs_6', 'mfq_36',
    'c_ssrs_last_visit_6',
    'chameleon_behavior_stu',
    'chameleon_attempt_stu',
]

suicidal_attempt_time2 = [
    'suicidal_behavior_last_11_clin',
    'suicidal_behavior_last_12_clin',
    'suicidal_behavior_last_13_clin',
    'mfq_36',
    'chameleon_attempt_stu',
]

nssi_time2 = [
    'suicidal_behavior_last_16_clin', 'mfq_37', 'chameleon_nssi_stu'
]

suicidal_ideation_time2 = [

    'c_ssrs_t_last_1_clin',
    'c_ssrs_t_last_2_clin',
    'c_ssrs_t_last_3_clin',
    'c_ssrs_t_last_4_clin',
    'c_ssrs_t_last_5_clin',

    #'c_ssrs_t_2weeks_1_clin',
    'c_ssrs_t_2weeks_2_clin',
    'c_ssrs_t_2weeks_3_clin',
    'c_ssrs_t_2weeks_4_clin',
    'c_ssrs_t_2weeks_5_clin',

    'c_ssrs_1',
    'c_ssrs_2',
    'c_ssrs_3',
    'c_ssrs_4',
    'c_ssrs_5',

    'chameleon_ideation_stu'
]


suicidal_ideation_cols = list(set(suicidal_ideation_life_intake + suicidal_ideation_time2))
suicidal_behavior_cols = list(set(suicidal_behavior_time2 + suicidal_behavior_intake))
suicidal_attempt_cols = list(set(suicidal_attempt_time2+suicide_attempt_intake))
nssi_cols = list(set(nssi_time2+nssi_intake))