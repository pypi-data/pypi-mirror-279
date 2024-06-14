from .impl.api.attachment import (
    delete_attachment_id,
    get_attachment_company_picture_id_company,
    get_attachment_data_by_id_id,
    get_attachment_event_images_id_event,
    get_attachment_info_by_foreign_id_mode_id,
    get_attachment_info_by_id_id,
    get_attachment_producing_place_images_id_producing_place,
    post_attachment,
    put_attachment_is_visible_in_uni_and_co_id_is_visible,
)
from .impl.api.auth import (
    delete_auth_id,
    delete_auth_user_id,
    get_auth,
    get_auth_current_user_info,
    get_auth_device_login,
    post_auth_change_client,
    post_auth_device_register_device,
    post_auth_login,
    post_auth_register,
    post_auth_reset_password,
    put_auth_by_id_id,
    put_auth_change_password,
)
from .impl.api.back_office import (
    get_back_office_event_definition_email_subscription_all,
    post_back_office_event_definition_email_subscription,
)
from .impl.api.bsd import (
    get_bsd_client_dasri_allow_taken_producing_place_id,
    get_bsd_client_siret,
    get_bsd_dasri_by_producer_id,
    get_bsd_dasri_id,
    get_bsd_download_link_direct_id,
    get_bsd_download_link_id,
    get_bsd_update_destination_data_rr_id,
    post_bsd_create,
    post_bsd_sign_many,
)
from .impl.api.calendar import get_calendar_calendar_occurrences, put_calendar_settings
from .impl.api.cartography import get_cartography_map_corrections
from .impl.api.check_in_submit import get_check_in_submit_id
from .impl.api.client import (
    get_client,
    get_client_default_speed_on_segment_km_h,
    get_client_filling_rate_setting,
    get_client_show_deadheading,
    post_client_filling_rate_setting,
    put_client_color_color,
    put_client_default_speed_on_segment_km_h,
    put_client_mapbox,
    put_client_show_deadheading,
)
from .impl.api.comment import (
    delete_comment_by_id_id,
    get_comment_by_event_id_id_event,
    post_comment_new,
    put_comment_by_id_id,
)
from .impl.api.company import (
    get_company_by_id_company_id,
    get_company_children_parent_company_id,
    get_company_cities,
    get_company_company_definitions,
    get_company_filter_options,
    get_company_id_history,
    get_company_legal_status,
    post_company,
    post_company_company_definition,
    post_company_delete_many,
    post_company_link_producing_places,
    put_company_children_companies_parent_company_id,
    put_company_company_definition_id,
    put_company_company_id,
    put_company_linked_contacts,
    put_company_unlink_child_company_id_child_company,
    put_company_unlink_parent_company_id_company,
    put_company_unlink_producing_place_id_producing_place,
)
from .impl.api.constraint import get_constraint_id, put_constraint
from .impl.api.contact_definition import (
    get_contact_definition,
    post_contact_definition,
    put_contact_definition_id,
)
from .impl.api.container import (
    delete_container_by_id_id,
    get_container,
    get_container_all_definitions,
    get_container_all_serial_numbers,
    get_container_by_id_id,
    get_container_by_id_producing_place_id_producing_place,
    get_container_by_serial_number_serial_number,
    get_container_containers_with_active_event,
    get_container_custom_fields_id,
    get_container_filter_options,
    get_container_filtered,
    get_container_history_by_id_id,
    get_container_id_history_report,
    post_container_delete_many,
    post_container_in_ids,
    post_container_new,
    post_container_new_many,
    put_container_by_id_id,
    put_container_update_state_by_id_id,
)
from .impl.api.container_definition import (
    get_container_definition,
    post_container_definition_new,
    put_container_definition_by_id_id,
)
from .impl.api.custom_field import (
    delete_custom_field_id,
    delete_custom_field_option_id_option,
    get_custom_field_many_target,
    post_custom_field,
    post_custom_field_option_id_custom_field,
)
from .impl.api.dashboard import get_dashboard_stats
from .impl.api.depot import (
    get_depot,
    get_depot_as_route_part_by_id_id,
    get_depot_as_route_part_label,
    get_depot_by_id_id,
    get_depot_details_id,
    get_depot_id_containers,
    get_depot_labels,
    post_depot,
    put_depot_by_id_id,
)
from .impl.api.device import (
    delete_device_event_id,
    get_device_all_devices,
    get_device_check_in_form,
    get_device_client,
    get_device_client_dasri_allow_taken_producing_place_id,
    get_device_container_by_serial_number_serial_number,
    get_device_container_definitions,
    get_device_containers_by_producing_place_id_id,
    get_device_depots,
    get_device_drivers,
    get_device_event_definitions,
    get_device_event_definitions_categories,
    get_device_itinerary_id,
    get_device_map_corrections,
    get_device_near_by_producing_place,
    get_device_outlets,
    get_device_poi_definitions,
    get_device_pois_id_poi_definition,
    get_device_round_id_itinerary,
    get_device_rounds_meta,
    get_device_search_producing_place,
    get_device_streams,
    get_device_update_change_log,
    get_device_v2_itinerary_id,
    get_device_v_2_near_by_producing_place,
    get_device_vehicles,
    post_device_bsd_sign_many,
    post_device_dasri_sign_many,
    post_device_live_data_update,
    post_device_map_corrections,
    post_device_submit_check_in,
    post_device_v2_bsd_create,
)
from .impl.api.driver import get_driver
from .impl.api.employee import (
    get_employee,
    get_employee_by_id_id,
    get_employee_employee_id_schedule,
    get_employee_filter_options,
    get_employee_id_constraint,
    post_employee_new,
    put_employee_archive_id,
    put_employee_archive_many,
    put_employee_by_id_id,
    put_employee_employee_id_schedule,
    put_employee_id_constraint,
    put_employee_sectors_id,
)
from .impl.api.error_report import post_error_report_device_crash_report
from .impl.api.event import (
    get_event_active,
    get_event_all_active,
    get_event_all_unique_authors,
    get_event_by_id_id,
    get_event_count_by_id_round_realisation_id_round_realisation,
    get_event_count_by_type,
    get_event_def_all,
    get_event_def_by_type_type,
    get_event_detailed_by_id_id,
    get_event_displayable_events,
    get_event_filter_options,
    get_event_filtered,
    get_event_to_planify,
    post_event_delete_many,
    post_event_new,
    put_event_update_by_id_id,
    put_event_update_state_id_state,
)
from .impl.api.event_definition import (
    get_event_definition,
    post_event_definition_new,
    put_event_definition_by_id_id,
)
from .impl.api.event_definition_category import (
    get_event_definition_category,
    post_event_definition_category_new,
    put_event_definition_category_by_id_id,
)
from .impl.api.export_client import get_export_client_reference_type
from .impl.api.external import (
    post_external_alpes_mesure_filling_rate,
    post_external_create_ifm_itinerary_id_realisation,
    post_external_elise_work_orders_id_franchise,
    post_external_live_vehicle_data,
    post_external_v2_live_vehicle_data,
)
from .impl.api.icons import get_icons
from .impl.api.intervention import (
    get_intervention_id,
    get_intervention_to_planify,
    put_intervention_id_planned_date,
)
from .impl.api.itinerary import (
    delete_itinerary_id,
    get_itinerary_catalog,
    get_itinerary_planified,
    get_itinerary_planified_id,
    get_itinerary_realised_id,
    get_itinerary_select_options,
    post_itinerary_new,
    put_itinerary_id,
)
from .impl.api.logistic import (
    post_logistic_as_pois,
    post_logistic_by_batch,
    post_logistic_export,
    post_logistic_total_count,
)
from .impl.api.mapbox import get_mapbox
from .impl.api.message import post_message_new
from .impl.api.metrics import get_metrics_db_status, get_metrics_ping
from .impl.api.occurrence import (
    get_occurrence_export_collect_points,
    get_occurrence_in_interval,
    get_occurrence_team_by_id,
)
from .impl.api.operational import (
    get_operational_filter_options,
    post_operational_layers_data_source,
)
from .impl.api.operator import get_operator, get_operator_by_id_ids, get_operator_history_by_id_id
from .impl.api.outlet import (
    get_outlet,
    get_outlet_all_as_route_parts,
    get_outlet_as_route_part_by_id_id,
    get_outlet_as_route_part_label,
    get_outlet_by_id_id,
    get_outlet_details_id,
    get_outlet_id_realisations,
    get_outlet_labels,
    post_outlet,
    put_outlet_by_id_id,
    put_outlet_id,
)
from .impl.api.pdf import (
    get_pdf_commercial_support_document_response_type,
    get_pdf_intervention_delivery_notice_response_type,
    get_pdf_intervention_destruction_certificates_response_type,
    get_pdf_intervention_elise_commercial_support_documents_response_type,
    get_pdf_intervention_mission_orders_response_type,
    get_pdf_roadmap_response_type,
)
from .impl.api.place import (
    get_place_by_id_id,
    get_place_close_place,
    get_place_operational_places,
    get_place_with_displayable_producing_places,
)
from .impl.api.poi import (
    get_poi,
    get_poi_as_route_part_by_id_poi_id,
    get_poi_by_definition_id_definition_id,
    get_poi_by_id_id,
    get_poi_filter_options,
    get_poi_point_of_interest_definitions,
    get_poi_points_of_interest_grouped_by_definitions,
    post_poi,
    post_poi_point_of_interest_definition,
    put_poi_id,
    put_poi_point_of_interest_definition_id,
)
from .impl.api.producer import (
    delete_producer_unlink_producer_with_producing_place_id_producer_id_producing_place,
    get_producer_all,
    get_producer_by_id_id,
    get_producer_by_producing_place_id_id,
    get_producer_filter_options,
    get_producer_history_by_id_id,
    get_producer_with_active_event,
    post_producer_delete_many,
    post_producer_id_uni_and_co_user,
    post_producer_new,
    put_producer_by_id_id,
)
from .impl.api.producing_place import (
    delete_producing_place_anomaly_id,
    get_producing_place_by_id_producer_id,
    get_producing_place_collectable_element_rounds_in_interval,
    get_producing_place_collection_planning_excel_by_id_producing_place_id,
    get_producing_place_custom_fields_id,
    get_producing_place_filter_options,
    get_producing_place_filtered,
    get_producing_place_id_details,
    get_producing_place_id_history,
    get_producing_place_id_trackdechets_info_company,
    get_producing_place_producing_place_id_schedule,
    get_producing_place_producing_place_id_waste_register,
    get_producing_place_with_active_event,
    post_producing_place_by_serial_numbers,
    post_producing_place_delete_many,
    post_producing_place_distinct_by_containers_ids,
    post_producing_place_distinct_ids_by_containers_ids,
    post_producing_place_new,
    post_producing_place_unique_stream_containers_total_by_ids,
    put_producing_place_id_update_trackdechets_info,
    put_producing_place_info_id,
    put_producing_place_linked_producers,
    put_producing_place_place_id,
    put_producing_place_producing_place_id_schedule,
    put_producing_place_sectors_id,
)
from .impl.api.producing_place_definition import (
    delete_producing_place_definition_id,
    get_producing_place_definition,
    get_producing_place_definition_id,
    post_producing_place_definition,
    put_producing_place_definition_id,
)
from .impl.api.public import get_public_containers
from .impl.api.realisation_round import (
    delete_realisation_round_outlet_realised_id,
    get_realisation_round_by_id_id,
    get_realisation_round_collect_report_by_id,
    get_realisation_round_container_collect_by_id_id,
    get_realisation_round_external_history_id_realisation,
    get_realisation_round_external_itinerary_id_realisation,
    get_realisation_round_filter_options,
    get_realisation_round_history_id,
    get_realisation_round_outlet_realised_id,
    get_realisation_round_planned_vs_realised_id,
    get_realisation_round_proof_of_passage_by_id_id,
    get_realisation_round_related_external_realisation_vehicle_id_realisation_date,
    get_realisation_round_stats,
    post_realisation_round_delete_many,
    post_realisation_round_outlet_realised,
    put_realisation_round_outlet_realised_id,
    put_realisation_round_proof_of_passage_id_ppra,
    put_realisation_round_update_container_collect_by_id_id,
)
from .impl.api.rotation_history import get_rotation_history
from .impl.api.round_ import (
    delete_round_id_round,
    delete_round_occurrence,
    get_round_itinerary_availability_id_itinerary_date,
    get_round_itinerary_planified_id_itinerary,
    get_round_itinerary_realised_id_itinerary,
    get_round_itinerary_track_id_geo_json_vehicle_profile,
    get_round_itinerary_track_id_shp_vehicle_profile,
    get_round_occurrence_by_id,
    get_round_occurrence_details_by_id,
    get_round_route_parts_itinerary_id_geo_json,
    get_round_route_parts_itinerary_id_shp,
    get_round_team,
    post_round_itineraries_route_parts_type,
    post_round_itineraries_type,
    post_round_new,
    post_round_tracks,
    put_round,
    put_round_occurrence,
    put_round_round_slots_id_round,
)
from .impl.api.route_parts import (
    get_route_parts_event_id,
    get_route_parts_producing_place_id,
    get_route_parts_segment_id,
    post_route_parts_availabilities,
    post_route_parts_producing_place_in_polygon,
)
from .impl.api.sector import delete_sector_by_id_id, get_sector_all, post_sector_new
from .impl.api.segment import (
    get_segment_by_id_id,
    get_segment_filter_options,
    post_segment_all,
    post_segment_territory_vehicle_profiles,
)
from .impl.api.stream import get_stream, get_stream_labels, post_stream_new, put_stream_by_id_id
from .impl.api.street_service import (
    post_street_service_compute_itinerary,
    put_street_service_transpose_realisation_id_realisation,
)
from .impl.api.track_dechet_waste_stream import (
    delete_track_dechet_waste_stream_id,
    get_track_dechet_waste_stream,
    post_track_dechet_waste_stream,
    put_track_dechet_waste_stream_id,
)
from .impl.api.unibac import (
    get_unibac_current_user_info,
    post_unibac_login,
    post_unibac_reset_password,
    post_unibac_scan,
    put_unibac_change_password,
)
from .impl.api.user_preferences import (
    get_user_preferences_container_sheet_params,
    get_user_preferences_logistic_params,
    get_user_preferences_operational_tabs_params,
    get_user_preferences_pdf_export_params,
    put_user_preferences_container_sheet_param,
    put_user_preferences_logistic_params_column,
    put_user_preferences_logistic_params_tab,
    put_user_preferences_operational_tabs_params,
    put_user_preferences_pdf_export_params,
)
from .impl.api.vehicle import (
    get_vehicle,
    get_vehicle_environmental_criteria,
    get_vehicle_filter_options,
    get_vehicle_history_by_id_vehicle_id,
    get_vehicle_info_by_id_vehicle_id,
    get_vehicle_labels,
    get_vehicle_labels_profile,
    get_vehicle_loading_types,
    get_vehicle_vehicle_profile_labels,
    get_vehicle_vehicle_profiles,
    post_vehicle_environmental_criterion_new,
    post_vehicle_loading_type_new,
    post_vehicle_new,
    post_vehicle_vehicle_profile_new,
    put_vehicle_archive_many,
    put_vehicle_archive_vehicle_id,
    put_vehicle_by_id_vehicle_id,
    put_vehicle_environmental_criterion_update,
    put_vehicle_loading_type_update,
    put_vehicle_sectors_sector_id,
    put_vehicle_vehicle_profile_update,
)
from .impl.client import Client
from .impl.models.change_client_payload import ChangeClientPayload
from .impl.models.change_client_response import ChangeClientResponse
from .impl.models.changelog_response import ChangelogResponse
from .impl.models.client_response import ClientResponse
from .impl.models.current_user_response import CurrentUserResponse
from .impl.models.device_response import DeviceResponse
from .impl.models.get_depots_response_item import GetDepotsResponseItem
from .impl.models.get_outlets_response_item import GetOutletsResponseItem
from .impl.models.get_pois_response_item import GetPoisResponseItem
from .impl.models.get_pois_response_item_place import GetPoisResponseItemPlace
from .impl.models.get_pois_response_item_poi_definition import GetPoisResponseItemPoiDefinition
from .impl.models.itinerary_creation_data import ItineraryCreationData
from .impl.models.login_choose_response import LoginChooseResponse
from .impl.models.login_choose_response_clients_item import LoginChooseResponseClientsItem
from .impl.models.login_choose_response_type import LoginChooseResponseType
from .impl.models.login_payload import LoginPayload
from .impl.models.login_token_response import LoginTokenResponse
from .impl.models.login_token_response_type import LoginTokenResponseType
from .impl.models.poi_route_part import PoiRoutePart
from .impl.models.poi_route_part_producing_place import PoiRoutePartProducingPlace
from .impl.models.poi_route_part_state import PoiRoutePartState
from .impl.models.poi_route_part_type import PoiRoutePartType
from .impl.models.post_attachment_body import PostAttachmentBody
from .impl.models.post_auth_register_body import PostAuthRegisterBody
from .impl.models.post_auth_reset_password_body import PostAuthResetPasswordBody
from .impl.models.post_back_office_event_definition_email_subscription_body import (
    PostBackOfficeEventDefinitionEmailSubscriptionBody,
)
from .impl.models.post_comment_new_body import PostCommentNewBody
from .impl.models.post_company_company_definition_body import PostCompanyCompanyDefinitionBody
from .impl.models.post_company_link_producing_places_body import PostCompanyLinkProducingPlacesBody
from .impl.models.post_container_delete_many_body import PostContainerDeleteManyBody
from .impl.models.post_container_new_many_body import PostContainerNewManyBody
from .impl.models.post_custom_field_body import PostCustomFieldBody
from .impl.models.post_custom_field_option_id_custom_field_body import (
    PostCustomFieldOptionIdCustomFieldBody,
)
from .impl.models.post_device_live_data_update_body import PostDeviceLiveDataUpdateBody
from .impl.models.post_device_map_corrections_body import PostDeviceMapCorrectionsBody
from .impl.models.post_device_submit_check_in_body import PostDeviceSubmitCheckInBody
from .impl.models.post_error_report_device_crash_report_body import (
    PostErrorReportDeviceCrashReportBody,
)
from .impl.models.post_event_definition_category_new_body import PostEventDefinitionCategoryNewBody
from .impl.models.post_event_definition_new_body import PostEventDefinitionNewBody
from .impl.models.post_event_delete_many_body import PostEventDeleteManyBody
from .impl.models.post_external_create_ifm_itinerary_id_realisation_body import (
    PostExternalCreateIFMItineraryIdRealisationBody,
)
from .impl.models.post_external_live_vehicle_data_body import PostExternalLiveVehicleDataBody
from .impl.models.post_itinerary_new_body import PostItineraryNewBody
from .impl.models.post_operational_layers_data_source_body import (
    PostOperationalLayersDataSourceBody,
)
from .impl.models.post_poi_point_of_interest_definition_body import (
    PostPoiPointOfInterestDefinitionBody,
)
from .impl.models.post_producer_delete_many_body import PostProducerDeleteManyBody
from .impl.models.post_producer_id_uni_and_co_user_body import PostProducerIdUniAndCoUserBody
from .impl.models.post_producing_place_by_serial_numbers_body import (
    PostProducingPlaceBySerialNumbersBody,
)
from .impl.models.post_producing_place_delete_many_body import PostProducingPlaceDeleteManyBody
from .impl.models.post_producing_place_distinct_by_containers_ids_body import (
    PostProducingPlaceDistinctByContainersIdsBody,
)
from .impl.models.post_producing_place_unique_stream_containers_total_by_ids_body import (
    PostProducingPlaceUniqueStreamContainersTotalByIdsBody,
)
from .impl.models.post_realisation_round_delete_many_body import PostRealisationRoundDeleteManyBody
from .impl.models.post_realisation_round_outlet_realised_body import (
    PostRealisationRoundOutletRealisedBody,
)
from .impl.models.post_round_tracks_body import PostRoundTracksBody
from .impl.models.post_route_parts_availabilities_body import PostRoutePartsAvailabilitiesBody
from .impl.models.post_route_parts_producing_place_in_polygon_body import (
    PostRoutePartsProducingPlaceInPolygonBody,
)
from .impl.models.post_sector_new_body import PostSectorNewBody
from .impl.models.post_stream_new_body import PostStreamNewBody
from .impl.models.post_unibac_login_body import PostUnibacLoginBody
from .impl.models.post_unibac_reset_password_body import PostUnibacResetPasswordBody
from .impl.models.post_unibac_scan_body import PostUnibacScanBody
from .impl.models.post_vehicle_environmental_criterion_new_body import (
    PostVehicleEnvironmentalCriterionNewBody,
)
from .impl.models.post_vehicle_loading_type_new_body import PostVehicleLoadingTypeNewBody
from .impl.models.post_vehicle_vehicle_profile_new_body import PostVehicleVehicleProfileNewBody
from .impl.models.put_auth_by_id_id_body import PutAuthByIdIdBody
from .impl.models.put_auth_change_password_body import PutAuthChangePasswordBody
from .impl.models.put_calendar_settings_body import PutCalendarSettingsBody
from .impl.models.put_client_default_speed_on_segment_km_h_body import (
    PutClientDefaultSpeedOnSegmentKmHBody,
)
from .impl.models.put_client_mapbox_body import PutClientMapboxBody
from .impl.models.put_client_show_deadheading_body import PutClientShowDeadheadingBody
from .impl.models.put_comment_by_id_id_body import PutCommentByIdIdBody
from .impl.models.put_company_company_definition_id_body import PutCompanyCompanyDefinitionIdBody
from .impl.models.put_company_linked_contacts_body import PutCompanyLinkedContactsBody
from .impl.models.put_constraint_body import PutConstraintBody
from .impl.models.put_container_update_state_by_id_id_body import PutContainerUpdateStateByIdIdBody
from .impl.models.put_employee_archive_id_body import PutEmployeeArchiveIdBody
from .impl.models.put_employee_archive_many_body import PutEmployeeArchiveManyBody
from .impl.models.put_employee_id_constraint_body import PutEmployeeIdConstraintBody
from .impl.models.put_employee_sectors_id_body import PutEmployeeSectorsIdBody
from .impl.models.put_event_definition_by_id_id_body import PutEventDefinitionByIdIdBody
from .impl.models.put_event_definition_category_by_id_id_body import (
    PutEventDefinitionCategoryByIdIdBody,
)
from .impl.models.put_intervention_id_planned_date_body import PutInterventionIdPlannedDateBody
from .impl.models.put_itinerary_id_body import PutItineraryIdBody
from .impl.models.put_outlet_id_body import PutOutletIdBody
from .impl.models.put_poi_point_of_interest_definition_id_body import (
    PutPoiPointOfInterestDefinitionIdBody,
)
from .impl.models.put_producing_place_id_update_trackdechets_info_body import (
    PutProducingPlaceIdUpdateTrackdechetsInfoBody,
)
from .impl.models.put_producing_place_linked_producers_body import (
    PutProducingPlaceLinkedProducersBody,
)
from .impl.models.put_producing_place_sectors_id_body import PutProducingPlaceSectorsIdBody
from .impl.models.put_realisation_round_proof_of_passage_id_ppra_body import (
    PutRealisationRoundProofOfPassageIdPpraBody,
)
from .impl.models.put_round_body import PutRoundBody
from .impl.models.put_round_occurrence_body import PutRoundOccurrenceBody
from .impl.models.put_round_round_slots_id_round_body import PutRoundRoundSlotsIdRoundBody
from .impl.models.put_stream_by_id_id_body import PutStreamByIdIdBody
from .impl.models.put_street_service_transpose_realisation_id_realisation_body import (
    PutStreetServiceTransposeRealisationIdRealisationBody,
)
from .impl.models.put_unibac_change_password_body import PutUnibacChangePasswordBody
from .impl.models.put_user_preferences_logistic_params_column_body import (
    PutUserPreferencesLogisticParamsColumnBody,
)
from .impl.models.put_user_preferences_operational_tabs_params_body import (
    PutUserPreferencesOperationalTabsParamsBody,
)
from .impl.models.put_user_preferences_pdf_export_params_body import (
    PutUserPreferencesPdfExportParamsBody,
)
from .impl.models.put_vehicle_archive_many_body import PutVehicleArchiveManyBody
from .impl.models.put_vehicle_archive_vehicle_id_body import PutVehicleArchiveVehicleIdBody
from .impl.models.put_vehicle_environmental_criterion_update_body import (
    PutVehicleEnvironmentalCriterionUpdateBody,
)
from .impl.models.put_vehicle_loading_type_update_body import PutVehicleLoadingTypeUpdateBody
from .impl.models.put_vehicle_sectors_sector_id_body import PutVehicleSectorsSectorIdBody
from .impl.models.put_vehicle_vehicle_profile_update_body import PutVehicleVehicleProfileUpdateBody
from .impl.models.register_device_payload import RegisterDevicePayload
from .impl.models.register_device_response import RegisterDeviceResponse
from .impl.models.round_creation_data import RoundCreationData
from .impl.models.round_creation_data_type import RoundCreationDataType
from .impl.models.round_slot_data import RoundSlotData
from .impl.models.round_slot_data_recurrence_type import RoundSlotDataRecurrenceType
from .impl.models.segment_route_part import SegmentRoutePart
from .impl.models.segment_route_part_direction import SegmentRoutePartDirection
from .impl.models.segment_route_part_intervention_mode import SegmentRoutePartInterventionMode
from .impl.models.segment_route_part_side import SegmentRoutePartSide
from .impl.models.segment_route_part_state import SegmentRoutePartState
from .impl.models.segment_route_part_type import SegmentRoutePartType

__all__ = [
    'post_logistic_export',
    'post_logistic_as_pois',
    'post_logistic_total_count',
    'post_logistic_by_batch',
    'get_metrics_ping',
    'get_metrics_db_status',
    'get_intervention_id',
    'put_intervention_id_planned_date',
    'get_intervention_to_planify',
    'put_street_service_transpose_realisation_id_realisation',
    'post_street_service_compute_itinerary',
    'post_custom_field',
    'delete_custom_field_option_id_option',
    'post_custom_field_option_id_custom_field',
    'get_custom_field_many_target',
    'delete_custom_field_id',
    'post_producer_new',
    'get_producer_with_active_event',
    'get_producer_history_by_id_id',
    'post_producer_id_uni_and_co_user',
    'get_producer_filter_options',
    'get_producer_by_id_id',
    'put_producer_by_id_id',
    'get_producer_all',
    'delete_producer_unlink_producer_with_producing_place_id_producer_id_producing_place',
    'get_producer_by_producing_place_id_id',
    'post_producer_delete_many',
    'get_depot_as_route_part_label',
    'post_depot',
    'get_depot_labels',
    'get_depot_by_id_id',
    'get_depot',
    'get_depot_as_route_part_by_id_id',
    'get_depot_id_containers',
    'put_depot_by_id_id',
    'get_depot_details_id',
    'put_contact_definition_id',
    'get_contact_definition',
    'post_contact_definition',
    'put_calendar_settings',
    'get_calendar_calendar_occurrences',
    'get_occurrence_team_by_id',
    'get_occurrence_export_collect_points',
    'get_occurrence_in_interval',
    'delete_producing_place_definition_id',
    'get_producing_place_definition',
    'get_producing_place_definition_id',
    'post_producing_place_definition',
    'put_producing_place_definition_id',
    'put_vehicle_by_id_vehicle_id',
    'post_vehicle_vehicle_profile_new',
    'get_vehicle_loading_types',
    'put_vehicle_vehicle_profile_update',
    'get_vehicle_vehicle_profiles',
    'get_vehicle_filter_options',
    'get_vehicle_vehicle_profile_labels',
    'get_vehicle_environmental_criteria',
    'get_vehicle_labels',
    'post_vehicle_new',
    'get_vehicle_labels_profile',
    'post_vehicle_loading_type_new',
    'get_vehicle',
    'get_vehicle_history_by_id_vehicle_id',
    'put_vehicle_environmental_criterion_update',
    'put_vehicle_loading_type_update',
    'put_vehicle_archive_many',
    'put_vehicle_archive_vehicle_id',
    'get_vehicle_info_by_id_vehicle_id',
    'put_vehicle_sectors_sector_id',
    'post_vehicle_environmental_criterion_new',
    'put_producing_place_id_update_trackdechets_info',
    'get_producing_place_producing_place_id_waste_register',
    'post_producing_place_new',
    'get_producing_place_id_trackdechets_info_company',
    'get_producing_place_filtered',
    'post_producing_place_distinct_by_containers_ids',
    'put_producing_place_place_id',
    'get_producing_place_filter_options',
    'delete_producing_place_anomaly_id',
    'get_producing_place_custom_fields_id',
    'get_producing_place_by_id_producer_id',
    'get_producing_place_collection_planning_excel_by_id_producing_place_id',
    'post_producing_place_distinct_ids_by_containers_ids',
    'get_producing_place_producing_place_id_schedule',
    'get_producing_place_with_active_event',
    'get_producing_place_id_history',
    'post_producing_place_by_serial_numbers',
    'get_producing_place_collectable_element_rounds_in_interval',
    'put_producing_place_info_id',
    'put_producing_place_linked_producers',
    'put_producing_place_sectors_id',
    'post_producing_place_delete_many',
    'put_producing_place_producing_place_id_schedule',
    'post_producing_place_unique_stream_containers_total_by_ids',
    'get_producing_place_id_details',
    'get_check_in_submit_id',
    'put_auth_change_password',
    'post_auth_login',
    'delete_auth_id',
    'get_auth',
    'post_auth_device_register_device',
    'post_auth_register',
    'post_auth_reset_password',
    'post_auth_change_client',
    'delete_auth_user_id',
    'get_auth_device_login',
    'get_auth_current_user_info',
    'put_auth_by_id_id',
    'get_driver',
    'delete_sector_by_id_id',
    'get_sector_all',
    'post_sector_new',
    'put_comment_by_id_id',
    'delete_comment_by_id_id',
    'get_comment_by_event_id_id_event',
    'post_comment_new',
    'post_unibac_login',
    'post_unibac_scan',
    'post_unibac_reset_password',
    'put_unibac_change_password',
    'get_unibac_current_user_info',
    'put_track_dechet_waste_stream_id',
    'delete_track_dechet_waste_stream_id',
    'post_track_dechet_waste_stream',
    'get_track_dechet_waste_stream',
    'get_route_parts_segment_id',
    'get_route_parts_event_id',
    'post_route_parts_producing_place_in_polygon',
    'post_route_parts_availabilities',
    'get_route_parts_producing_place_id',
    'get_attachment_info_by_id_id',
    'delete_attachment_id',
    'get_attachment_data_by_id_id',
    'post_attachment',
    'get_attachment_company_picture_id_company',
    'get_attachment_info_by_foreign_id_mode_id',
    'get_attachment_producing_place_images_id_producing_place',
    'put_attachment_is_visible_in_uni_and_co_id_is_visible',
    'get_attachment_event_images_id_event',
    'get_realisation_round_collect_report_by_id',
    'get_realisation_round_external_history_id_realisation',
    'get_realisation_round_proof_of_passage_by_id_id',
    'post_realisation_round_delete_many',
    'get_realisation_round_planned_vs_realised_id',
    'get_realisation_round_history_id',
    'get_realisation_round_filter_options',
    'get_realisation_round_related_external_realisation_vehicle_id_realisation_date',
    'delete_realisation_round_outlet_realised_id',
    'put_realisation_round_update_container_collect_by_id_id',
    'get_realisation_round_by_id_id',
    'get_realisation_round_external_itinerary_id_realisation',
    'get_realisation_round_container_collect_by_id_id',
    'put_realisation_round_outlet_realised_id',
    'get_realisation_round_stats',
    'put_realisation_round_proof_of_passage_id_ppra',
    'get_realisation_round_outlet_realised_id',
    'post_realisation_round_outlet_realised',
    'get_stream_labels',
    'get_stream',
    'put_stream_by_id_id',
    'post_stream_new',
    'post_back_office_event_definition_email_subscription',
    'get_back_office_event_definition_email_subscription_all',
    'get_segment_by_id_id',
    'get_segment_filter_options',
    'post_segment_territory_vehicle_profiles',
    'post_segment_all',
    'get_pdf_intervention_mission_orders_response_type',
    'get_pdf_roadmap_response_type',
    'get_pdf_intervention_destruction_certificates_response_type',
    'get_pdf_intervention_elise_commercial_support_documents_response_type',
    'get_pdf_intervention_delivery_notice_response_type',
    'get_pdf_commercial_support_document_response_type',
    'post_message_new',
    'get_bsd_client_siret',
    'get_bsd_client_dasri_allow_taken_producing_place_id',
    'post_bsd_create',
    'get_bsd_dasri_by_producer_id',
    'get_bsd_update_destination_data_rr_id',
    'get_bsd_download_link_id',
    'post_bsd_sign_many',
    'get_bsd_download_link_direct_id',
    'get_bsd_dasri_id',
    'post_error_report_device_crash_report',
    'get_dashboard_stats',
    'put_poi_point_of_interest_definition_id',
    'post_poi',
    'get_poi_points_of_interest_grouped_by_definitions',
    'put_poi_id',
    'get_poi_by_definition_id_definition_id',
    'get_poi',
    'post_poi_point_of_interest_definition',
    'get_poi_point_of_interest_definitions',
    'get_poi_as_route_part_by_id_poi_id',
    'get_poi_filter_options',
    'get_poi_by_id_id',
    'get_container_filter_options',
    'get_container_history_by_id_id',
    'put_container_by_id_id',
    'get_container_custom_fields_id',
    'get_container_by_id_id',
    'delete_container_by_id_id',
    'get_container_all_serial_numbers',
    'get_container',
    'post_container_in_ids',
    'post_container_new_many',
    'get_container_by_id_producing_place_id_producing_place',
    'get_container_all_definitions',
    'get_container_containers_with_active_event',
    'put_container_update_state_by_id_id',
    'get_container_by_serial_number_serial_number',
    'post_container_new',
    'get_container_id_history_report',
    'get_container_filtered',
    'post_container_delete_many',
    'get_outlet_by_id_id',
    'post_outlet',
    'get_outlet_details_id',
    'get_outlet_labels',
    'get_outlet_as_route_part_label',
    'get_outlet',
    'put_outlet_id',
    'get_outlet_as_route_part_by_id_id',
    'put_outlet_by_id_id',
    'get_outlet_all_as_route_parts',
    'get_outlet_id_realisations',
    'get_public_containers',
    'get_user_preferences_container_sheet_params',
    'put_user_preferences_pdf_export_params',
    'put_user_preferences_container_sheet_param',
    'get_user_preferences_logistic_params',
    'get_user_preferences_pdf_export_params',
    'put_user_preferences_operational_tabs_params',
    'put_user_preferences_logistic_params_column',
    'put_user_preferences_logistic_params_tab',
    'get_user_preferences_operational_tabs_params',
    'post_event_definition_new',
    'get_event_definition',
    'put_event_definition_by_id_id',
    'get_icons',
    'post_round_itineraries_route_parts_type',
    'get_round_itinerary_planified_id_itinerary',
    'put_round_occurrence',
    'delete_round_id_round',
    'post_round_itineraries_type',
    'get_round_occurrence_by_id',
    'delete_round_occurrence',
    'get_round_itinerary_availability_id_itinerary_date',
    'get_round_route_parts_itinerary_id_shp',
    'get_round_itinerary_realised_id_itinerary',
    'post_round_tracks',
    'get_round_route_parts_itinerary_id_geo_json',
    'get_round_itinerary_track_id_shp_vehicle_profile',
    'post_round_new',
    'put_round',
    'get_round_occurrence_details_by_id',
    'put_round_round_slots_id_round',
    'get_round_team',
    'get_round_itinerary_track_id_geo_json_vehicle_profile',
    'get_rotation_history',
    'put_container_definition_by_id_id',
    'get_container_definition',
    'post_container_definition_new',
    'get_device_v2_itinerary_id',
    'get_device_search_producing_place',
    'get_device_v_2_near_by_producing_place',
    'get_device_all_devices',
    'get_device_poi_definitions',
    'post_device_map_corrections',
    'post_device_submit_check_in',
    'get_device_drivers',
    'get_device_outlets',
    'get_device_streams',
    'post_device_bsd_sign_many',
    'get_device_client_dasri_allow_taken_producing_place_id',
    'get_device_event_definitions_categories',
    'get_device_near_by_producing_place',
    'post_device_live_data_update',
    'post_device_v2_bsd_create',
    'get_device_containers_by_producing_place_id_id',
    'get_device_container_by_serial_number_serial_number',
    'get_device_vehicles',
    'get_device_event_definitions',
    'get_device_round_id_itinerary',
    'get_device_check_in_form',
    'get_device_itinerary_id',
    'get_device_client',
    'get_device_pois_id_poi_definition',
    'get_device_container_definitions',
    'post_device_dasri_sign_many',
    'get_device_update_change_log',
    'delete_device_event_id',
    'get_device_depots',
    'get_device_rounds_meta',
    'get_device_map_corrections',
    'get_mapbox',
    'post_external_v2_live_vehicle_data',
    'post_external_create_ifm_itinerary_id_realisation',
    'post_external_elise_work_orders_id_franchise',
    'post_external_live_vehicle_data',
    'post_external_alpes_mesure_filling_rate',
    'post_operational_layers_data_source',
    'get_operational_filter_options',
    'get_place_operational_places',
    'get_place_by_id_id',
    'get_place_with_displayable_producing_places',
    'get_place_close_place',
    'put_employee_employee_id_schedule',
    'put_employee_sectors_id',
    'get_employee',
    'put_employee_id_constraint',
    'get_employee_id_constraint',
    'get_employee_employee_id_schedule',
    'get_employee_filter_options',
    'put_employee_by_id_id',
    'get_employee_by_id_id',
    'put_employee_archive_many',
    'put_employee_archive_id',
    'post_employee_new',
    'put_itinerary_id',
    'get_itinerary_realised_id',
    'get_itinerary_planified',
    'get_itinerary_planified_id',
    'post_itinerary_new',
    'delete_itinerary_id',
    'get_itinerary_catalog',
    'get_itinerary_select_options',
    'put_event_update_state_id_state',
    'get_event_filtered',
    'get_event_def_all',
    'put_event_update_by_id_id',
    'get_event_def_by_type_type',
    'post_event_delete_many',
    'get_event_filter_options',
    'get_event_by_id_id',
    'get_event_count_by_type',
    'get_event_detailed_by_id_id',
    'get_event_to_planify',
    'get_event_active',
    'get_event_count_by_id_round_realisation_id_round_realisation',
    'get_event_all_active',
    'get_event_displayable_events',
    'get_event_all_unique_authors',
    'post_event_new',
    'get_client_default_speed_on_segment_km_h',
    'put_client_default_speed_on_segment_km_h',
    'get_client_show_deadheading',
    'put_client_mapbox',
    'get_client',
    'put_client_show_deadheading',
    'post_client_filling_rate_setting',
    'put_client_color_color',
    'get_client_filling_rate_setting',
    'get_operator_by_id_ids',
    'get_operator_history_by_id_id',
    'get_operator',
    'get_cartography_map_corrections',
    'get_constraint_id',
    'put_constraint',
    'get_event_definition_category',
    'put_event_definition_category_by_id_id',
    'post_event_definition_category_new',
    'get_export_client_reference_type',
    'get_company_id_history',
    'post_company_link_producing_places',
    'put_company_unlink_producing_place_id_producing_place',
    'put_company_company_definition_id',
    'put_company_unlink_parent_company_id_company',
    'get_company_by_id_company_id',
    'post_company',
    'post_company_company_definition',
    'put_company_linked_contacts',
    'get_company_filter_options',
    'post_company_delete_many',
    'get_company_cities',
    'put_company_children_companies_parent_company_id',
    'get_company_legal_status',
    'put_company_unlink_child_company_id_child_company',
    'get_company_company_definitions',
    'put_company_company_id',
    'get_company_children_parent_company_id',
    'ChangeClientPayload',
    'ChangeClientResponse',
    'ChangelogResponse',
    'ClientResponse',
    'CurrentUserResponse',
    'DeviceResponse',
    'GetDepotsResponseItem',
    'GetOutletsResponseItem',
    'GetPoisResponseItem',
    'GetPoisResponseItemPlace',
    'GetPoisResponseItemPoiDefinition',
    'ItineraryCreationData',
    'LoginChooseResponse',
    'LoginChooseResponseClientsItem',
    'LoginChooseResponseType',
    'LoginPayload',
    'LoginTokenResponse',
    'LoginTokenResponseType',
    'PoiRoutePart',
    'PoiRoutePartProducingPlace',
    'PoiRoutePartState',
    'PoiRoutePartType',
    'PostAttachmentBody',
    'PostAuthRegisterBody',
    'PostAuthResetPasswordBody',
    'PostBackOfficeEventDefinitionEmailSubscriptionBody',
    'PostCommentNewBody',
    'PostCompanyCompanyDefinitionBody',
    'PostCompanyLinkProducingPlacesBody',
    'PostContainerDeleteManyBody',
    'PostContainerNewManyBody',
    'PostCustomFieldBody',
    'PostCustomFieldOptionIdCustomFieldBody',
    'PostDeviceLiveDataUpdateBody',
    'PostDeviceMapCorrectionsBody',
    'PostDeviceSubmitCheckInBody',
    'PostErrorReportDeviceCrashReportBody',
    'PostEventDefinitionCategoryNewBody',
    'PostEventDefinitionNewBody',
    'PostEventDeleteManyBody',
    'PostExternalCreateIFMItineraryIdRealisationBody',
    'PostExternalLiveVehicleDataBody',
    'PostItineraryNewBody',
    'PostOperationalLayersDataSourceBody',
    'PostPoiPointOfInterestDefinitionBody',
    'PostProducerDeleteManyBody',
    'PostProducerIdUniAndCoUserBody',
    'PostProducingPlaceBySerialNumbersBody',
    'PostProducingPlaceDeleteManyBody',
    'PostProducingPlaceDistinctByContainersIdsBody',
    'PostProducingPlaceUniqueStreamContainersTotalByIdsBody',
    'PostRealisationRoundDeleteManyBody',
    'PostRealisationRoundOutletRealisedBody',
    'PostRoundTracksBody',
    'PostRoutePartsAvailabilitiesBody',
    'PostRoutePartsProducingPlaceInPolygonBody',
    'PostSectorNewBody',
    'PostStreamNewBody',
    'PostUnibacLoginBody',
    'PostUnibacResetPasswordBody',
    'PostUnibacScanBody',
    'PostVehicleEnvironmentalCriterionNewBody',
    'PostVehicleLoadingTypeNewBody',
    'PostVehicleVehicleProfileNewBody',
    'PutAuthByIdIdBody',
    'PutAuthChangePasswordBody',
    'PutCalendarSettingsBody',
    'PutClientDefaultSpeedOnSegmentKmHBody',
    'PutClientMapboxBody',
    'PutClientShowDeadheadingBody',
    'PutCommentByIdIdBody',
    'PutCompanyCompanyDefinitionIdBody',
    'PutCompanyLinkedContactsBody',
    'PutConstraintBody',
    'PutContainerUpdateStateByIdIdBody',
    'PutEmployeeArchiveIdBody',
    'PutEmployeeArchiveManyBody',
    'PutEmployeeIdConstraintBody',
    'PutEmployeeSectorsIdBody',
    'PutEventDefinitionByIdIdBody',
    'PutEventDefinitionCategoryByIdIdBody',
    'PutInterventionIdPlannedDateBody',
    'PutItineraryIdBody',
    'PutOutletIdBody',
    'PutPoiPointOfInterestDefinitionIdBody',
    'PutProducingPlaceIdUpdateTrackdechetsInfoBody',
    'PutProducingPlaceLinkedProducersBody',
    'PutProducingPlaceSectorsIdBody',
    'PutRealisationRoundProofOfPassageIdPpraBody',
    'PutRoundBody',
    'PutRoundOccurrenceBody',
    'PutRoundRoundSlotsIdRoundBody',
    'PutStreamByIdIdBody',
    'PutStreetServiceTransposeRealisationIdRealisationBody',
    'PutUnibacChangePasswordBody',
    'PutUserPreferencesLogisticParamsColumnBody',
    'PutUserPreferencesOperationalTabsParamsBody',
    'PutUserPreferencesPdfExportParamsBody',
    'PutVehicleArchiveManyBody',
    'PutVehicleArchiveVehicleIdBody',
    'PutVehicleEnvironmentalCriterionUpdateBody',
    'PutVehicleLoadingTypeUpdateBody',
    'PutVehicleSectorsSectorIdBody',
    'PutVehicleVehicleProfileUpdateBody',
    'RegisterDevicePayload',
    'RegisterDeviceResponse',
    'RoundCreationData',
    'RoundCreationDataType',
    'RoundSlotData',
    'RoundSlotDataRecurrenceType',
    'SegmentRoutePart',
    'SegmentRoutePartDirection',
    'SegmentRoutePartInterventionMode',
    'SegmentRoutePartSide',
    'SegmentRoutePartState',
    'SegmentRoutePartType',
    'Client',
]
