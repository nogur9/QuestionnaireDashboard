
# qualtrics redcap - map
TRANSFORMATION_RULES = {

    'opening_child_pre': 'EXTRA QUESTIONS IN QUALTRICS', # age_child_pre_first

    'c_ssrs_clin': 'EXTRA QUESTIONS IN REDCAP',
    'c_ssrs_stu': 'EXTRA QUESTIONS IN REDCAP',
    'er_questionnaire_clin': 'EXTRA QUESTIONS IN REDCAP',


    'moas_m': 'REDCAP_ONLY',
    'ffq': 'REDCAP_ONLY',
    'moas_f': 'REDCAP_ONLY',
    'screening_form': 'REDCAP_ONLY',
    # 'ps_demographics_m': 'REDCAP_ONLY',
    # 'parental_self_stigma_scale_m': 'REDCAP_ONLY',
    # 'parental_self_efficacy_m': 'REDCAP_ONLY',
    # 'the_illness_cognitions_questionnaire_m': 'REDCAP_ONLY',
	# 'isi_m': 'REDCAP_ONLY',
	# 'the_caregiver_strain_questionnaire_m': 'REDCAP_ONLY',
	# 'the_impact_of_event_scalerevised_m': 'REDCAP_ONLY',
	# 'ps_demographics_f': 'REDCAP_ONLY',
    # 'parental_self_stigma_scale_f': 'REDCAP_ONLY',
	# 'parental_self_efficacy_f': 'REDCAP_ONLY',
	# 'the_illness_cognitions_questionnaire_f': 'REDCAP_ONLY',
	# 'isi_f': 'REDCAP_ONLY',
	# 'the_caregiver_strain_questionnaire_f': 'REDCAP_ONLY',
	# 'the_impact_of_event_scalerevised_f': 'REDCAP_ONLY',
	# 'fhs': 'REDCAP_ONLY',


    'opening': 'DEFAULT',
    'siq': 'DEFAULT',
    'mfq': 'DEFAULT',
    'c_ssrs_intake': 'DEFAULT',
    'c_ssrs': 'DEFAULT',
    'sdq': 'DEFAULT',
    'scared': 'DEFAULT',
    'ATHENS': 'DEFAULT',
    'SAS': 'DEFAULT',
    'sci_af_ca': 'DEFAULT',
    'scs_clin': 'DEFAULT',
    'scs_stu': 'DEFAULT',
    'sci_mother': 'DEFAULT',
    'sci_father': 'DEFAULT',
    'mast': 'DEFAULT',
    'maris_sci_sf': 'DEFAULT',
    'maris_soq_sf': 'DEFAULT',
    'ARI_P_M': 'DEFAULT',
    'ARI_S': 'DEFAULT',
    'demographics_f': 'DEFAULT',
    'demographics_m': 'DEFAULT',
    'swan_m': 'DEFAULT',
    'swan_f': 'DEFAULT',
    'dass_f': 'DEFAULT',
    'ecr_f': 'DEFAULT',
    'c_ssrs_fu_maya': 'DEFAULT',
    'trq_sf_maris_clin': 'DEFAULT',
    'covid19': 'DEFAULT',
    'erc_rc': 'DEFAULT',
    'piu': 'DEFAULT',
    'cyberbulling': 'DEFAULT',
    'erq_ca': 'DEFAULT',
    'ders': 'DEFAULT',
    'wai': 'DEFAULT',
    'cshq_m': 'DEFAULT',
    'sdq_parents_m': 'DEFAULT',
    'dass_m': 'DEFAULT',
    'ders_p_m': 'DEFAULT',
    'ecr_m': 'DEFAULT',
    'cshq_f': 'DEFAULT',
    'erq_f': 'DEFAULT',
    'ARI_P_F': 'DEFAULT',
    'opening_clinicians': 'DEFAULT',
    'wai_immirisk_clin': 'DEFAULT',
    'remote_clin': 'DEFAULT',
    'sdq_parents_f': 'DEFAULT',
    'suicide_form_clin': 'DEFAULT',
    'mini_kid_sum_clin': 'DEFAULT',
    'trq_sf_maris_stu': 'DEFAULT',
    'mini_kid_sum_stu': 'DEFAULT',
    'chameleon': 'DEFAULT',
    'erq_m': 'DEFAULT',
    'cts_m': 'DEFAULT',
    'ending_parent_m': 'DEFAULT',
    'opening_parents_f': 'DEFAULT',
    'ders_p_f': 'DEFAULT',
    'cdrsr_clin': 'DEFAULT',
    'opening_students': 'DEFAULT',
    'cgi_s_stu': 'DEFAULT',
    'remote_stu': 'DEFAULT',
    'cps_stu': 'DEFAULT',
    'cps_clin': 'DEFAULT',
    'cgi_s_clin': 'DEFAULT',
    'opening_therapist_battery': 'DEFAULT',
    'maris_y_scars_clin': 'DEFAULT',
    'ending_parent_f': 'DEFAULT',
    'cts_f': 'DEFAULT',
    'cts_c': 'DEFAULT',
    'dshi_pre': 'DEFAULT',
    'dshi_post': 'DEFAULT',
    'inq': 'DEFAULT',
    'ending': 'DEFAULT',
    'opening_parents_m': 'DEFAULT',
    'estimation_and_satisfaction': 'DEFAULT',
    'intro': 'DEFAULT'
}



Stepped_Care_Extras  = {
 'cors_c': 'STEPPED_ONLY',
 'cssrs_c_intake': 'STEPPED_ONLY',
 'cssrs_c_measurs': 'STEPPED_ONLY',
 'derss_c': 'STEPPED_ONLY',
 'cpss_c': 'STEPPED_ONLY',
 'chs': 'STEPPED_ONLY',
 'mspss': 'STEPPED_ONLY',
 'csq4_c': 'STEPPED_ONLY',
 'ending_child': 'STEPPED_ONLY',
 'asq_parent_m_5de6': 'STEPPED_ONLY',
 'srs_s_parent_m': 'STEPPED_ONLY',
 'orscors_child_m': 'STEPPED_ONLY',
 'wai_parent_m': 'STEPPED_ONLY',
 'csq4_parent_m': 'STEPPED_ONLY',
 'asq_parent_f_f16b': 'STEPPED_ONLY',
 'srs_s_parent_f': 'STEPPED_ONLY',
 'orscors_child_f': 'STEPPED_ONLY',
 'wai_parent_f_6e34': 'STEPPED_ONLY',
 'csq4_parent_f': 'STEPPED_ONLY',
 'opening_clinician': 'STEPPED_ONLY',
 'criteria_for_ipc': 'STEPPED_ONLY',
 'cssrs_clin_ssc': 'STEPPED_ONLY',
 'cgas_clin': 'STEPPED_ONLY',
 'ending_clin': 'STEPPED_ONLY',

}



# Questionnaires Renaming

q_names_step_to_redcap = {
    'opening_child': 'opening_child_pre',
    'sci_c': 'sciafca',
    'scared_sr': 'scared',
    'sas_c': 'sas',
    'wai_c': 'wai',
    'dass21_m': 'dass_m',
    'ending_m': 'ending_parent_m',
    'demographic_father': 'demographic_parents_f',
    'dass21_f_585e': 'dass_f',
    'sci_clin': "sci_c_clin",
    'cgi_s_i_clin': 'cgi_s_clin',
    'wai_clin': 'wai_immirisk_clin',
    'csq4_c': 'estimation_and_satisfaction'


}
q_names_redcap_to_step = {v: k for k, v in q_names_step_to_redcap.items()}

"""
not_sure_renames = {
    'cssrs_c_intake': 'cssrs_intake',
    'cssrs_c_measurs': 'cssrs_intake',
    'ending_child': 'ending',
    'criteria_for_ipc': 'screening_form',
    'cssrs_clin_ssc': 'cssrs_t_clin',
    'ending_clin': 'ending'
}

other
    [
 'csq4_parent_f',
 'csq4_parent_m',
 'ending_parent_f',
 ]
"""
