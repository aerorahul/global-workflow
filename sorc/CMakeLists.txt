set(BUILD_EXT_DIR ${CMAKE_CURRENT_BINARY_DIR}/_build)

if(BUILD_GFS_UTILS)
    message(STATUS "Enable ... gfs_utils")
    set(BUILD_DIR ${BUILD_EXT_DIR}/gfsutils)
    set(INSTALL_PREFIX ${PROJECT_BINARY_DIR}/install)
    add_custom_target(gfsutils ALL
        COMMAND
            BUILD_TYPE=${CMAKE_BUILD_TYPE};
            BUILD_DIR=${BUILD_DIR};
            INSTALL_PREFIX=${INSTALL_PREFIX};
            ush/build.sh
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/gfs_utils.fd
    )
endif()

if(BUILD_UFS_UTILS)
    message(STATUS "Enable ... ufs_utils")
    set(BUILD_DIR ${BUILD_EXT_DIR}/ufs_utils)
    set(INSTALL_PREFIX ${PROJECT_BINARY_DIR}/install)
    add_custom_target(gsimon ALL
        COMMAND
            BUILD_TYPE=${CMAKE_BUILD_TYPE};
            BUILD_DIR=${BUILD_DIR};
            INSTALL_PREFIX=${INSTALL_PREFIX};
            ush/build.sh
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/ufs_utils.fd
    )
endif()

if(BUILD_UFS_MODEL)
    message(STATUS "Enable ... ufs_model")
endif()

if(BUILD_GSI_MONITOR)
    message(STATUS "Enable ... gsi_monitor")
    set(BUILD_DIR ${BUILD_EXT_DIR}/gsi_monitor)
    set(INSTALL_PREFIX ${PROJECT_BINARY_DIR}/install)
    add_custom_target(gsimon ALL
        COMMAND
            BUILD_TYPE=${CMAKE_BUILD_TYPE};
            BUILD_DIR=${BUILD_DIR};
            INSTALL_PREFIX=${INSTALL_PREFIX};
            ush/build.sh
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/gsi_monitor.fd
    )
endif()
