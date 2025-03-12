if(SB_CONFIG_SOC_NRF5340_CPUNET)
  ExternalZephyrProject_Add(
    APPLICATION rf_test_app_core
    SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/rf_test_app_core/
    BOARD nrf5340dk/nrf5340/cpuapp
  )
endif()
