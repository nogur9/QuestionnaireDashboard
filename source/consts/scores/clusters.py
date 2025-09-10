
SDQ_clusters = {        # there are a lot of different clusters
        'SDQ_Conduct': ['sdq_5', 'sdq_7', 'sdq_12', 'sdq_18', 'sdq_22'],
        'SDQ_Emo': ['sdq_3', 'sdq_8', 'sdq_13', 'sdq_16', 'sdq_24'],
        'SDQ_Hyper': ['sdq_2', 'sdq_10', 'sdq_15', 'sdq_21', 'sdq_25'],
        'SDQ_Peer': ['sdq_6', 'sdq_11', 'sdq_14', 'sdq_19', 'sdq_23'],
        'SDQ_Prosocial_Behavior': ['sdq_1', 'sdq_4', 'sdq_9', 'sdq_17', 'sdq_20']
        # 'SDQ_Externalizing': conduct_columns + hyper_columns,
        # 'SDQ_Internalizing': emo_columns + peer_columns,
}



Clusters = {

    'sdq': SDQ_clusters,

    'ecrrc': {
        'ecr_rc_anxiety': ['erc_rc_1', 'erc_rc_2', 'erc_rc_3', 'erc_rc_4', 'erc_rc_5', 'erc_rc_6'],
        'ecr_rc_avoidance': ['erc_rc_7', 'erc_rc_8', 'erc_rc_9', 'erc_rc_10', 'erc_rc_11', 'erc_rc_12']
    },

    'mast': {
    'mast_al': ['mast_1', 'mast_5', 'mast_6', 'mast_13', 'mast_18', 'mast_19', 'mast_25', 'mast_28'],
    'mast_rl': ['mast_2', 'mast_9', 'mast_14', 'mast_15', 'mast_16', 'mast_21', 'mast_30'],
    'mast_ad': ['mast_8', 'mast_17', 'mast_22', 'mast_23', 'mast_26', 'mast_27', 'mast_29'],
    'mast_rd': ['mast_3', 'mast_4', 'mast_7', 'mast_10', 'mast_11', 'mast_12', 'mast_20', 'mast_24']},

    'erqca': {
        'Cognitive Reappraisal': ['erq_ca_1', 'erq_ca_3', 'erq_ca_5', 'erq_ca_7', 'erq_ca_8', 'erq_ca_10'],
        'Expressive Suppression': ['erq_ca_2', 'erq_ca_4', 'erq_ca_6', 'erq_ca_9'],
    },

    'ders': {
    'ders_Nonacceptance_Emotional': ['ders_11', 'ders_12', 'ders_21', 'ders_23', 'ders_25', 'ders_29'],
    'ders_Difficulty_Goal_Directed': ['ders_13', 'ders_18', 'ders_20', 'ders_26', 'ders_33'],
    'ders_Difficulty_Impulse_Control': ['ders_3', 'ders_14', 'ders_19', 'ders_24', 'ders_27', 'ders_32'],
    'ders_Lack_Emotional_Awareness': ['ders_2', 'ders_6', 'ders_8', 'ders_10', 'ders_17', 'ders_34'],
    'ders_Limited_Regulation_Strategies': ['ders_15', 'ders_16', 'ders_22', 'ders_28',
                                            'ders_30', 'ders_31', 'ders_35', 'ders_36'],
    'ders_Lack_Clarity': ['ders_1', 'ders_4', 'ders_5', 'ders_7', 'ders_9'],
    },

    'wai': {
    'wai_goal': ['wai_4', 'wai_6', 'wai_8', 'wai_11'],
    'wai_task': ['wai_1', 'wai_2', 'wai_10', 'wai_12'],
    'wai_bond': ['wai_3', 'wai_5', 'wai_7', 'wai_9'],
    },

    'wai_immirisk_clin': {
        'wai_goal': ['wai_t_immi_4_clin', 'wai_t_immi_6_clin', 'wai_t_immi_8_clin', 'wai_t_immi_11_clin'],
        'wai_task': ['wai_t_immi_1_clin', 'wai_t_immi_2_clin', 'wai_t_immi_10_clin', 'wai_t_immi_12_clin'],
        'wai_bond': ['wai_t_immi_3_clin', 'wai_t_immi_5_clin', 'wai_t_immi_7_clin', 'wai_t_immi_9_clin'],
    },

    'inq': {

    'INQ_Thwarted Belongingness': ['inq_7', 'inq_8',  'inq_9', 'inq_10',
                                    'inq_11', 'inq_12', 'inq_13',  'inq_14', 'inq_15'],
    'INQ_Perceived Burdensomeness': ['inq_1', 'inq_2',  'inq_3',
                                     'inq_4','inq_5', 'inq_6']
    },

    'swan_m':  {
        'attention_swan_m': [f'swan_{i}_m' for i in range(1, 10)],
        'impulsivity_swan_m': [f'swan_{i}_m' for i in range(10, 19)]
    },

    'ders_p_m': {
        'ders_p_m_Nonacceptance_Emotional': ['ders_11_p_m', 'ders_12_p_m', 'ders_21_p_m', 'ders_23_p_m',
                                         'ders_25_p_m', 'ders_29_p_m'],
        'ders_p_m_Difficulty_Goal_Directed': ['ders_13_p_m', 'ders_18_p_m', 'ders_20_p_m', 'ders_26_p_m',
                                          'ders_33_p_m'],
        'ders_p_m_Difficulty_Impulse_Control': ['ders_3_p_m', 'ders_14_p_m', 'ders_19_p_m', 'ders_24_p_m',
                                            'ders_27_p_m', 'ders_32_p_m'],
        'ders_p_m_Lack_Emotional_Awareness': ['ders_2_p_m', 'ders_6_p_m', 'ders_8_p_m', 'ders_10_p_m',
                                          'ders_17_p_m', 'ders_34_p_m'],
        'ders_p_m_Limited_Regulation_Strategies': ['ders_15_p_m', 'ders_16_p_m', 'ders_22_p_m', 'ders_28_p_m',
                                               'ders_30_p_m', 'ders_31_p_m', 'ders_35_p_m', 'ders_36_p_m'],
        'ders_p_m_Lack_Clarity': ['ders_1_p_m', 'ders_4_p_m', 'ders_5_p_m', 'ders_7_p_m', 'ders_9_p_m'],
    },

    'erq_m': {
        'Cognitive Reappraisal': ['erq_1_m', 'erq_3_m', 'erq_5_m', 'erq_7_m', 'erq_8_m', 'erq_10_m'],
        'Expressive Suppression': ['erq_2_m', 'erq_4_m', 'erq_6_m', 'erq_9_m'],
    },


    'dass_m': {
        'DASS_DEPRESSION': ['dass_3_m', 'dass_5_m', 'dass_10_m', 'dass_13_m',
                            'dass_16_m','dass_17_m','dass_21_m'],

        'DASS_ANXIETY': ['dass_2_m','dass_4_m','dass_7_m','dass_9_m',
                         'dass_15_m','dass_19_m','dass_20_m'],

        'DASS_STRESS': ['dass_1_m','dass_6_m','dass_8_m',
                        'dass_11_m','dass_12_m','dass_14_m','dass_18_m']
    },
}

